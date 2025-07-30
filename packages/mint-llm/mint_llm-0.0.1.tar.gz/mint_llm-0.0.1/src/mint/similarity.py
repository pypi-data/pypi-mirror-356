from __future__ import annotations

from pathlib import Path
import sys
from safetensors.torch import load_file, save_file
import torch  # type: ignore
from tqdm import tqdm


def build_similarity(
    embedding_path: str | None = None,
    existing_path: str | None = None,
    output_path: str | None = None,
    device: str | torch.device | None = None,
    tau: float = 1e-4,
) -> torch.Tensor:
    """Compute or reuse a similarity matrix.

    Parameters
    ----------
    embedding_path: str | None, optional
        Path to embedding weights file in ``.safetensors`` format.
    existing_path: str | None, optional
        Precomputed matrix file. If supplied, it is loaded instead of
        computing a new matrix.
    output_path: str | None, optional
        Where to save the resulting matrix when computed.
    device: str | torch.device | None, optional
        Device used for computation. ``None`` selects ``"cuda"`` when
        available and otherwise uses ``"cpu"``.
    tau: float, optional
        Sparsity threshold. Values with absolute magnitude below ``tau`` are
        pruned. Default is ``1e-4``.
    """

    path: Path | None = None
    use_existing: bool = False
    if existing_path is not None:
        path = Path(existing_path)
        use_existing = True
    elif embedding_path is not None:
        path = Path(embedding_path)
    if path is None:
        raise Exception(
            "`build_similarity` requires `existing_path` or `embedding_path` to be supplied."
        )

    matrix: torch.Tensor | None = None

    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    if use_existing:
        if path.suffix == ".safetensors":
            matrix = load_file(str(path))["similarity"].to(device)
        else:
            matrix = torch.load(str(path))["similarity"].to(device)
    else:
        embedding = load_file(str(embedding_path))["embedding"].to(device)
        n = embedding.size(0)
        dense = torch.empty((n, n), device=device)
        iterable = range(n)
        if sys.stderr.isatty():
            iterable = tqdm(iterable)
        for i in iterable:
            dense[i] = embedding[i] @ embedding.t()
        matrix = dense
        if tau > 0:
            mask = matrix.abs() < tau
            matrix[mask] = 0
        matrix = matrix.to_sparse()
        matrix = matrix.to(device)
    output = Path(output_path) if output_path is not None else None
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        if output.suffix == ".safetensors":
            save_file({"similarity": matrix.to_dense().cpu()}, str(output))
        else:
            torch.save({"similarity": matrix.cpu()}, str(output))
    return matrix
