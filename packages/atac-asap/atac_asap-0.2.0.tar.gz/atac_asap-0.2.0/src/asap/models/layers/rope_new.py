from typing import Callable, Optional
import torch
from torch import Tensor
import torch.nn as nn
from torch.nn import functional as F

import math

import torch

import numpy as np

def create_local_attention_mask(seq_length, window_size, dtype=None):
    # Initialize the attention mask with zeros
    attention_mask = torch.zeros((seq_length, seq_length), dtype=dtype)

    for i in range(seq_length):
        # Calculate the start and end of the window
        start = max(0, i - window_size)
        end = min(seq_length, i + window_size + 1)
        
        # Set the values within the window to 1
        attention_mask[i, start:end] = 1
    return attention_mask.to(bool)


class RoPEEncoderLayer(nn.TransformerEncoderLayer):
    def __init__(self, d_model: int, nhead: int, dim_feedforward: int = 2048, dropout: float = 0.1, activation: str | Callable[[Tensor], Tensor] = F.relu, layer_norm_eps: float = 0.00001, batch_first: bool = False, norm_first: bool = False, device=None, dtype=None) -> None:
        super().__init__(d_model=d_model, nhead=nhead, dim_feedforward=dim_feedforward, dropout=dropout, activation=activation, layer_norm_eps=layer_norm_eps, batch_first=batch_first, norm_first=norm_first, device=device, dtype=dtype)
        self.rotary_emb = RotaryEmbedding(d_model=d_model)
        self.local_attention_mask = create_local_attention_mask(512, 52)

    def forward(
            self,
            src: Tensor,
            src_mask: Optional[Tensor] = None,
            src_key_padding_mask: Optional[Tensor] = None,
            is_causal: bool = False) -> Tensor:
        r"""Pass the input through the encoder layer.

        Args:
            src: the sequence to the encoder layer (required).
            src_mask: the mask for the src sequence (optional).
            is_causal: If specified, applies a causal mask as src_mask.
            Default: ``False``.
            src_key_padding_mask: the mask for the src keys per batch (optional).

        Shape:
            see the docs in Transformer class.
        """
        src_key_padding_mask = F._canonical_mask(
            mask=src_key_padding_mask,
            mask_name="src_key_padding_mask",
            other_type=F._none_or_dtype(src_mask),
            other_name="src_mask",
            target_type=src.dtype
        )

        src_mask = F._canonical_mask(
            mask=src_mask,
            mask_name="src_mask",
            other_type=None,
            other_name="",
            target_type=src.dtype,
            check_other=False,
        )

        x = src
        if self.norm_first:
            x = x + self._sa_block(self.norm1(x), src_mask, src_key_padding_mask, is_causal=is_causal)
            x = x + self._ff_block(self.norm2(x))
        else:
            x = self.norm1(x + self._sa_block(x, src_mask, src_key_padding_mask, is_causal=is_causal))
            x = self.norm2(x + self._ff_block(x))

        return x


    def _sa_block(self, x: torch.Tensor, attn_mask: Optional[Tensor], key_padding_mask: Optional[Tensor], is_causal: bool = False) -> Tensor:
        x_rot = self.rotary_emb(x)
        if self.local_attention_mask.device != x.device:
            self.local_attention_mask = self.local_attention_mask.to(x.device)

        x = self.self_attn(x_rot, x_rot, x, # q k v
                           attn_mask=self.local_attention_mask,
                           key_padding_mask=key_padding_mask,
                           need_weights=False, is_causal=is_causal)[0]
        return self.dropout1(x)

# adapted from kaggle.com/code/aeryss/rotary-postional-encoding-rope-pytorch
class RotaryEmbedding(torch.nn.Module):
    def __init__(self, d_model, base=10000, seq_dim=-2):
        super().__init__()
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(base) / d_model))
        self.register_buffer('div_term', div_term)
        self.seq_dim = seq_dim
        self.seq_len_cached = None
        self.cos_cached = None
        self.sin_cached = None

    def get_sin_cos(self, x: torch.Tensor):
        seq_len = x.shape[self.seq_dim]
        if seq_len != self.seq_len_cached:
            self.seq_len_cached = seq_len
            t = torch.arange(x.shape[self.seq_dim], device=x.device).type_as(self.div_term)
            freqs = torch.einsum('i,j->ij', t, self.div_term)
            emb = torch.cat((freqs, freqs), dim=-1).to(x.device)
            self.cos_cached = emb.cos()
            self.sin_cached = emb.sin()
        return self.cos_cached, self.sin_cached
    
    @staticmethod
    def rotate_half(x):
        x1, x2 = x[..., :x.shape[-1] // 2], x[..., x.shape[-1] // 2:]
        return torch.cat((-x2, x1), dim=-1)

    def forward(self, t: torch.Tensor):
        cos, sin = self.get_sin_cos(t)
        return (t * cos) + (self.rotate_half(t) * sin)
