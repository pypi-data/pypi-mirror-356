from __future__ import annotations

from pathlib import Path
from safetensors.torch import load_file
import torch
from torch import nn

from .sr_layer import SimilarityRedistributor


def load_wrapped_model(
    model_path: str,
    similarity_path: str,
    alpha: float = 0.0,
) -> nn.Module:
    """Load a HuggingFace model and attach a ``SimilarityRedistributor``.

    Parameters
    ----------
    model_path:
        Either a Hugging Face model identifier or a local directory path
        understood by ``AutoModelForCausalLM.from_pretrained``.
    similarity_path:
        File containing the sparse similarity matrix under the key ``"similarity"``.
        ``.safetensors`` and PyTorch ``.pt`` files are supported.
    alpha:
        Strength of demotion for the original logits.
    """

    from transformers import AutoModelForCausalLM  # type: ignore

    model = AutoModelForCausalLM.from_pretrained(model_path)

    path = Path(similarity_path)
    if path.suffix == ".safetensors":
        tensor = load_file(str(path))["similarity"]
    else:
        tensor = torch.load(str(path))["similarity"]
    if not tensor.is_sparse:
        tensor = tensor.to_sparse()

    layer = SimilarityRedistributor(tensor, alpha=alpha)
    if isinstance(model.lm_head, nn.Sequential):
        model.lm_head = nn.Sequential(*model.lm_head, layer)
    else:
        model.lm_head = nn.Sequential(model.lm_head, layer)
    return model
