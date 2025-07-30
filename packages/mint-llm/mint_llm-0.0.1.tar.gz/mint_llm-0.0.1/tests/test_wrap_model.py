import types
import sys

import torch
from torch import nn
from safetensors.torch import save_file

from mint.sr_layer import SimilarityRedistributor
from mint.wrap_model import load_wrapped_model


class DummyModel(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.lm_head = nn.Identity()


class DummyModelLinear(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.lm_head = nn.Linear(2, 2)


class DummyModelSequential(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.lm_head = nn.Sequential(nn.Linear(2, 2), nn.ReLU())


class DummyAuto:
    model_cls: type[nn.Module] = DummyModel

    @classmethod
    def from_pretrained(cls, path: str) -> nn.Module:  # type: ignore[override]
        return cls.model_cls()


def install_dummy_transformers(monkeypatch, model_cls: type[nn.Module] = DummyModel):
    DummyAuto.model_cls = model_cls
    module = types.ModuleType("transformers")
    module.AutoModelForCausalLM = DummyAuto  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "transformers", module)


def test_load_wrapped_model_pt(monkeypatch, tmp_path):
    install_dummy_transformers(monkeypatch)
    S = torch.eye(2).to_sparse()
    sim_path = tmp_path / "sim.pt"
    torch.save({"similarity": S}, sim_path)

    model = load_wrapped_model("dummy", str(sim_path), alpha=0.5)
    assert isinstance(model.lm_head, nn.Sequential)
    assert isinstance(model.lm_head[1], SimilarityRedistributor)
    assert model.lm_head[1].alpha == 0.5
    assert torch.equal(model.lm_head[1].S.to_dense(), torch.eye(2))  # type: ignore[operator]


def test_load_wrapped_model_safetensors(monkeypatch, tmp_path):
    install_dummy_transformers(monkeypatch)
    S = torch.tensor([[0.0, 1.0], [1.0, 0.0]]).to_sparse()
    sim_path = tmp_path / "sim.safetensors"
    save_file({"similarity": S.to_dense()}, str(sim_path))

    model = load_wrapped_model("dummy", str(sim_path))
    assert isinstance(model.lm_head, nn.Sequential)
    layer = model.lm_head[1]
    assert isinstance(layer, SimilarityRedistributor)
    assert torch.equal(layer.S.to_dense(), S.to_dense())  # type: ignore[operator]


def test_wrap_single_module(monkeypatch, tmp_path):
    install_dummy_transformers(monkeypatch, DummyModelLinear)
    S = torch.eye(2).to_sparse()
    sim_path = tmp_path / "sim.pt"
    torch.save({"similarity": S}, sim_path)

    model = load_wrapped_model("dummy", str(sim_path))
    assert isinstance(model.lm_head, nn.Sequential)
    assert len(model.lm_head) == 2
    assert isinstance(model.lm_head[0], nn.Linear)
    assert isinstance(model.lm_head[1], SimilarityRedistributor)


def test_wrap_existing_sequential(monkeypatch, tmp_path):
    install_dummy_transformers(monkeypatch, DummyModelSequential)
    S = torch.eye(2).to_sparse()
    sim_path = tmp_path / "sim.pt"
    torch.save({"similarity": S}, sim_path)

    model = load_wrapped_model("dummy", str(sim_path))
    assert isinstance(model.lm_head, nn.Sequential)
    assert len(model.lm_head) == 3
    assert isinstance(model.lm_head[-1], SimilarityRedistributor)
    assert isinstance(model.lm_head[0], nn.Linear)
    assert isinstance(model.lm_head[1], nn.ReLU)
