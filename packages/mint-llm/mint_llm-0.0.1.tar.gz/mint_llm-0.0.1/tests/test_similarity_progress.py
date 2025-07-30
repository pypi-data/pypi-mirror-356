import sys
import torch
from safetensors.torch import save_file

from mint.similarity import build_similarity


def test_build_similarity_uses_tqdm(monkeypatch, tmp_path):
    emb = torch.eye(2)
    emb_file = tmp_path / "emb.safetensors"
    save_file({"embedding": emb}, str(emb_file))

    calls = []

    def fake_tqdm(iterable):
        calls.append(True)
        return iterable

    monkeypatch.setattr(sys.stderr, "isatty", lambda: True)
    monkeypatch.setattr("mint.similarity.tqdm", fake_tqdm)

    build_similarity(str(emb_file))

    assert calls
