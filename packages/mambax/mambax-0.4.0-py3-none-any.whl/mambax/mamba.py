import math
import torch
import torch.nn.functional as F
from torch import nn
from einops import rearrange
from mambax.pscan import pscan


import math
import torch
import torch.nn as nn
import torch.nn.functional as F


class Mamba(nn.Module):
    def __init__(
        self,
        d_model,
        d_inner,
        d_conv=4,
        d_state=16,
        dt_rank=64,
        bias=False,
        conv_bias=False,
        use_cuda=False,
        use_fast_path=False
    ):
        super().__init__()
        self.d_model = d_model
        self.d_inner = d_inner
        self.d_conv = d_conv
        self.d_state = d_state
        self.dt_rank = dt_rank
        self.act = nn.SiLU()

        # Projections
        self.in_proj = nn.Linear(d_model, 2 * d_inner, bias=bias)
        self.conv1d = nn.Conv1d(
            d_inner,
            d_inner,
            kernel_size=d_conv,
            bias=conv_bias,
            groups=d_inner,
            padding=d_conv - 1
        )
        self.x_proj = nn.Linear(d_inner, dt_rank + 2 * d_state, bias=False)
        self.dt_proj = nn.Linear(dt_rank, d_inner, bias=True)
        
        # Initialize dt_proj
        dt_std = dt_rank ** -0.5
        nn.init.uniform_(self.dt_proj.weight, -dt_std, dt_std)

        # Initialize dt bias
        dt = torch.exp(
            torch.rand(d_inner) * (math.log(0.1) - math.log(1e-3)) + math.log(1e-3)
        )
        inv_dt = dt + torch.log(-torch.expm1(-dt))
        with torch.no_grad():
            self.dt_proj.bias.copy_(inv_dt)

        # State parameters
        A = torch.arange(1, d_state + 1).repeat(d_inner, 1).float()
        self.A_log = nn.Parameter(torch.log(A))
        self.A_log._no_weight_decay = True

        self.D = nn.Parameter(torch.ones(d_inner))
        self.D._no_weight_decay = True

        # Output projections
        self.out_proj = nn.Linear(d_inner, d_model, bias=bias)
        self.drop = nn.Dropout(0.1)
        if use_cuda:
            if use_fast_path:
                try:
                    from mamba_ssm.ops.selective_scan_interface import mamba_inner_fn
                    self.mamba_inner_fn = mamba_inner_fn
                    self.use_cuda = True
                    self.use_fast_path = True
                except ImportError:
                    self.mamba_inner_fn = None
                    self.use_cuda = False
                    self.use_fast_path = False
            else:
                try:
                    from mamba_ssm.ops.selective_scan_interface import selective_scan_fn
                    from causal_conv1d import causal_conv1d_fn
                    self.selective_scan_fn_cuda = selective_scan_fn
                    self.causal_conv1d_fn = causal_conv1d_fn
                    self.use_cuda = True
                except ImportError:
                    self.selective_scan_fn_cuda = None
                    self.causal_conv1d_fn = None
                    self.use_cuda = False
                self.use_fast_path = False


    def forward(self, x, h0=None, conv_cache=None, onnx_export=True):
        """Forward pass of Mamba block.
        
        Args:
            x: Input tensor of shape (B, L, D)
            h0: Initial hidden state of shape (B, ED, N)
            conv_cache: Convolution cache of shape (B, ED, d_conv-1)
            onnx_export: Whether to export to ONNX format
        """
        if h0 is None:
            return self._forward_full(x)
        else:
            return self._forward_cumprod(x, h0, conv_cache, onnx_export)
        



    def _forward_cumprod(self, x, h0=None, conv_cache=None, onnx_export=True):
      
        xz = self.in_proj(x)  # (B, Lc, 2*ED)
        x_part, z_part = xz.chunk(2, dim=-1)  # (B, Lc, ED)

        x_cat = torch.cat([conv_cache, x_part.transpose(1, 2)], dim=2)  # (B, ED, d_conv-1+Lc)
        x_conv = F.conv1d(
            x_cat, self.conv1d.weight, bias=self.conv1d.bias, groups=self.d_inner
        )  # (B, ED, Lc)
        x_conv = self.act(x_conv.transpose(1, 2))  # (B, Lc, ED)

        A = -torch.exp(self.A_log.float())
        D = self.D
        deltaBC = self.x_proj(x_conv)  # (B, Lc, dt_rank+2N)
        delta, B_, C_ = torch.split(
            deltaBC,
            [self.dt_rank, self.d_state, self.d_state],
            dim=-1
        )
        
        delta = self.dt_proj.weight @ delta.transpose(1, 2)  # (B, Lc, ED)
        delta = delta.transpose(1, 2)
        delta = F.softplus(delta + self.dt_proj.bias)
      
        deltaA = torch.exp(delta.unsqueeze(-1) * A)  # (B, Lc, ED, N)
        deltaB = delta.unsqueeze(-1) * B_.unsqueeze(2)  # (B, Lc, ED, N)
        BX = deltaB * x_conv.unsqueeze(-1)  # (B, Lc, ED, N)

        if onnx_export:
            P = torch.exp(torch.cumsum(torch.log(deltaA + 1e-8), dim=1))
        else:
            P = torch.cumprod(deltaA, dim=1) + 1e-8

        invP = 1.0 / P
        S = torch.cumsum(BX * invP, dim=1)  
        h_all = P * (h0.unsqueeze(1) + S)  # (B, Lc, ED, N)
        h_new = h_all[:, -1]  # (B, ED, N) — в cache

        y = (h_all @ C_.unsqueeze(-1)).squeeze(-1) + D * x_conv  # (B, Lc, ED)
        z_part = self.act(z_part)
        out = self.out_proj(y * z_part)  # (B, Lc, D)

        new_inputs = torch.cat([conv_cache, x_part.transpose(1, 2)], dim=2)
        new_inputs = new_inputs[:, :, -(self.d_conv - 1):]

        return out, h_new, new_inputs

    def _forward_full(self, x):
        _, L, _ = x.shape
        
        xz = self.in_proj(x)

        if self.cuda and self.use_fast_path:
            xz = xz.permute(0, 2, 1)

            A = -torch.exp(self.A_log.float())
            out = self.mamba_inner_fn(
                xz,
                self.conv1d.weight,
                self.conv1d.bias,
                self.x_proj.weight,
                self.dt_proj.weight,
                self.out_proj.weight,
                self.out_proj.bias,
                A,
                None,  
                None,  
                self.D.float(),
                delta_bias=self.dt_proj.bias.float(),
                delta_softplus=True,
            )
        else:
            x, z = xz.chunk(2, dim=-1)

            x = x.transpose(1, 2)

            if self.use_cuda:
                True
                x = self.causal_conv1d_fn(
                    x=x,
                    weight=self.conv1d.weight.squeeze(1),
                    bias=self.conv1d.bias,
                    activation='silu')                      
            else:
                x = self.conv1d(x)[:, :, :L]

            x = x.transpose(1, 2)
            x = self.act(x)
            
            y = self.ssm(x, z)

            if self.use_cuda:
                out = self.out_proj(y)
            else:
                z = self.act(z)
                out = self.out_proj(y * z)

            if self.training:
                out = self.drop(out)

        return out

    def ssm(self, x, z):
        A = -torch.exp(self.A_log.float())
        D = self.D
        
        deltaBC = self.x_proj(x)
        delta, B, C = torch.split(
            deltaBC,
            [self.dt_rank, self.d_state, self.d_state],
            dim=-1
        )
        
        delta = self.dt_proj.weight @ delta.transpose(1, 2)


        if self.use_cuda:

            x = x.transpose(1, 2)
            B = B.transpose(1, 2)
            C = C.transpose(1, 2)
            z = z.transpose(1, 2)
            y = self.selective_scan_fn_cuda(x, delta, A, B, C, D, z=z, delta_softplus=True, delta_bias=self.dt_proj.bias.float())
            y = y.transpose(1, 2) 
        else:

            delta = delta.transpose(1, 2)
            delta = F.softplus(delta + self.dt_proj.bias)
            y = self.selective_scan(x, delta, A, B, C, D)

        return y

    def selective_scan(self, x, delta, A, B, C, D):
        deltaA = torch.exp(delta.unsqueeze(-1) * A)  # (B, L, ED, N)
        deltaB = delta.unsqueeze(-1) * B.unsqueeze(2)  # (B, L, ED, N)
        BX = deltaB * x.unsqueeze(-1)

        hs = pscan(deltaA, BX)
        y = (hs @ C.unsqueeze(-1)).squeeze(3)
        return y + D * x
