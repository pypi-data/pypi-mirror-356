from __future__ import annotations

from torch import nn
import torch


class SimilarityRedistributor(nn.Module):
    """Redistribute token logits using a sparse similarity matrix."""

    def __init__(self, sparse_S: torch.Tensor, alpha: float = 0.0) -> None:
        """Create a new layer.

        Parameters
        ----------
        sparse_S:
            Sparse similarity matrix of shape ``(V, V)``.
        alpha:
            Strength of demotion for the original logits. ``0`` disables demotion.
        """
        super().__init__()
        if not sparse_S.is_sparse:
            raise ValueError("S must be a sparse tensor")
        self.register_buffer("S", sparse_S)
        self.alpha = float(alpha)

    def forward(self, logits: torch.Tensor) -> torch.Tensor:  # type: ignore[override]
        """Apply redistribution to ``logits``."""
        redistributed = torch.sparse.mm(self.S, logits.unsqueeze(-1)).squeeze(-1)
        if self.alpha > 0:
            redistributed = redistributed - self.alpha * logits
        return redistributed
