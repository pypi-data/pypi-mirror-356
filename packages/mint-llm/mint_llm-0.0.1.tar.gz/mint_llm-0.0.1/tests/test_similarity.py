import torch
from safetensors.torch import save_file

from torch import load as torch_load

from mint.similarity import build_similarity


def test_build_similarity_computes_and_saves(tmp_path):
    emb = torch.eye(3)
    emb_file = tmp_path / "emb.safetensors"
    save_file({"embedding": emb}, str(emb_file))

    out_file = tmp_path / "sim.pt"
    matrix = build_similarity(str(emb_file), output_path=str(out_file))

    assert matrix.is_sparse
    assert torch.equal(matrix.to_dense(), emb @ emb.t())
    saved = torch_load(str(out_file))["similarity"]
    assert saved.is_sparse
    assert torch.equal(saved.to_dense(), emb @ emb.t())


def test_build_similarity_tau_threshold(tmp_path):
    emb = torch.tensor([[1.0, 0.5], [0.5, 1.0]])
    emb_file = tmp_path / "emb.safetensors"
    save_file({"embedding": emb}, str(emb_file))

    out_file = tmp_path / "sim.pt"
    matrix = build_similarity(str(emb_file), output_path=str(out_file), tau=0.6)

    assert matrix.is_sparse
    expected = emb @ emb.t()
    expected[expected.abs() < 0.6] = 0
    assert torch.equal(matrix.to_dense(), expected)


def test_build_similarity_reuses_existing(tmp_path):
    emb = torch.zeros(2, 2)
    emb_file = tmp_path / "emb.safetensors"
    save_file({"embedding": emb}, str(emb_file))

    existing = tmp_path / "existing.pt"
    sim = torch.tensor([[2.0, 1.0], [1.0, 2.0]])
    torch.save({"similarity": sim.to_sparse()}, str(existing))

    out_file = tmp_path / "out.pt"
    matrix = build_similarity(str(emb_file), str(existing), str(out_file))
    assert matrix.is_sparse
    assert torch.equal(matrix.to_dense(), sim)
    loaded = torch_load(str(out_file))["similarity"]
    assert loaded.is_sparse
    assert torch.equal(loaded.to_dense(), sim)


def test_build_similarity_single_write(monkeypatch, tmp_path):
    emb = torch.eye(2)
    emb_file = tmp_path / "emb.safetensors"
    save_file({"embedding": emb}, str(emb_file))

    out_file = tmp_path / "exists.safetensors"
    # ensure file already exists so build_similarity should overwrite only once
    save_file({"similarity": torch.zeros(2, 2)}, str(out_file))

    calls: list[str] = []
    original = save_file

    def recording_save(obj, path):
        calls.append(path)
        original(obj, path)

    monkeypatch.setattr("mint.similarity.save_file", recording_save)

    build_similarity(str(emb_file), output_path=str(out_file))
    assert len(calls) == 1
