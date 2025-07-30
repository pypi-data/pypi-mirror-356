from __future__ import annotations

from pathlib import Path
from typing import Tuple

import torch
from safetensors.torch import load_file
from transformers import AutoModelForCausalLM, AutoTokenizer

from .sr_layer import SimilarityRedistributor


def _load_similarity(
    path: str, device: torch.device | str | None = None
) -> torch.Tensor:
    p = Path(path)
    if p.suffix == ".safetensors":
        tensor = load_file(str(p))["similarity"]
    else:
        tensor = torch.load(str(p))["similarity"]
    if device is not None:
        tensor = tensor.to(device)
    return tensor


def load_wrapped_model(
    model_name_or_path: str, similarity: str, alpha: float = 0.0
) -> Tuple[AutoModelForCausalLM, AutoTokenizer, SimilarityRedistributor]:
    """Load a model and attach the similarity redistribution layer.

    Parameters
    ----------
    model_name_or_path:
        Hugging Face model identifier or local path understood by
        ``AutoModelForCausalLM.from_pretrained``.
    similarity:
        File containing the sparse similarity matrix under the key
        ``"similarity"``.
    alpha:
        Strength of demotion for the original logits. ``0`` disables demotion.
    """

    model = AutoModelForCausalLM.from_pretrained(model_name_or_path)
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
    S = _load_similarity(similarity, model.device)
    layer = SimilarityRedistributor(S, alpha=alpha)
    return model, tokenizer, layer
