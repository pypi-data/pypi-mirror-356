from typer.testing import CliRunner
import torch
from safetensors.torch import save_file
from torch import load as torch_load

from mint.cli import app


def test_cli_build_computes_similarity(tmp_path):
    runner = CliRunner()
    emb = torch.eye(3)
    emb_file = tmp_path / "emb.safetensors"
    save_file({"embedding": emb}, str(emb_file))

    out_file = tmp_path / "sim.pt"
    result = runner.invoke(app, ["blend", str(emb_file), str(out_file)])
    assert result.exit_code == 0
    saved = torch_load(str(out_file))["similarity"]
    assert saved.is_sparse
    assert torch.equal(saved.to_dense(), emb @ emb.t())


def test_cli_build_cpu_option(tmp_path):
    runner = CliRunner()
    emb = torch.eye(2)
    emb_file = tmp_path / "emb_cpu.safetensors"
    save_file({"embedding": emb}, str(emb_file))

    out_file = tmp_path / "sim_cpu.pt"
    result = runner.invoke(app, ["blend", str(emb_file), str(out_file), "--cpu"])
    assert result.exit_code == 0
    saved = torch_load(str(out_file))["similarity"]
    assert saved.is_sparse
    assert torch.equal(saved.to_dense(), emb @ emb.t())


def test_cli_build_reuses_existing(tmp_path):
    runner = CliRunner()
    emb1 = torch.tensor([[1.0, 0.0], [0.0, 1.0]])
    emb1_file = tmp_path / "emb1.safetensors"
    save_file({"embedding": emb1}, str(emb1_file))

    existing = tmp_path / "precomputed.pt"
    sim = emb1 @ emb1.t() + 1
    torch.save({"similarity": sim.to_sparse()}, str(existing))

    emb2 = torch.zeros_like(emb1)
    emb2_file = tmp_path / "emb2.safetensors"
    save_file({"embedding": emb2}, str(emb2_file))

    out_file = tmp_path / "out.pt"
    result = runner.invoke(
        app,
        ["blend", str(emb2_file), str(out_file), "--similarity", str(existing)],
    )
    assert result.exit_code == 0
    loaded = torch_load(str(out_file))["similarity"]
    assert loaded.is_sparse
    assert torch.equal(loaded.to_dense(), sim)


def test_cli_build_creates_subdirs(tmp_path):
    runner = CliRunner()
    emb = torch.eye(2)
    emb_file = tmp_path / "emb.safetensors"
    save_file({"embedding": emb}, str(emb_file))

    out_file = tmp_path / "nested" / "sim.pt"
    result = runner.invoke(app, ["blend", str(emb_file), str(out_file)])
    assert result.exit_code == 0
    assert out_file.exists()
    saved = torch_load(str(out_file))["similarity"]
    assert saved.is_sparse
    assert torch.equal(saved.to_dense(), emb @ emb.t())


def test_cli_build_tau_option(tmp_path):
    runner = CliRunner()
    emb = torch.tensor([[1.0, 0.2], [0.2, 1.0]])
    emb_file = tmp_path / "emb.safetensors"
    save_file({"embedding": emb}, str(emb_file))

    out_file = tmp_path / "sim.pt"
    result = runner.invoke(app, ["blend", str(emb_file), str(out_file), "--tau", "0.3"])
    assert result.exit_code == 0
    saved = torch_load(str(out_file))["similarity"]
    expected = emb @ emb.t()
    expected[expected.abs() < 0.3] = 0
    assert torch.equal(saved.to_dense(), expected)
