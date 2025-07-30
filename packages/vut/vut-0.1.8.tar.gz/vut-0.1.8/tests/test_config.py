from dataclasses import dataclass

import pytest

from vut.config import BaseConfig, Config


@dataclass
class SimpleConfig(BaseConfig):
    name: str
    value: int
    flag: bool = False


@dataclass
class NestedConfig(BaseConfig):
    inner_value: int


@dataclass
class ParentConfig(BaseConfig):
    name: str
    nested: NestedConfig


def test_config__from_dict_nested():
    config_dict = {
        "seed": 42,
        "device": "cuda",
        "model": {"name": "i3d"},
        "dataset": {
            "name": "50salads",
            "num_classes": 19,
            "num_actions": 10,
            "backgrounds": ["SIL"],
            "class_mapping_path": "/path/to/mapping.txt",
            "class_mapping_has_header": False,
            "action_mapping_path": "/path/to/actions.txt",
        },
        "training": {
            "split": 1,
            "num_fold": 5,
            "lr": 0.0005,
            "batch_size": 1,
            "sampling_rate": 1,
        },
        "visualization": {"legend_ncols": 4},
    }

    config = Config.from_dict(config_dict)

    assert config.seed == 42
    assert config.device == "cuda"

    assert config.model.name == "i3d"

    assert config.dataset.name == "50salads"
    assert config.dataset.num_classes == 19
    assert config.dataset.num_actions == 10
    assert config.dataset.backgrounds == ["SIL"]
    assert config.dataset.class_mapping_path == "/path/to/mapping.txt"
    assert config.dataset.class_mapping_has_header is False
    assert config.dataset.action_mapping_path == "/path/to/actions.txt"

    assert config.training.split == 1
    assert config.training.num_fold == 5
    assert config.training.lr == 0.0005
    assert config.training.batch_size == 1
    assert config.training.sampling_rate == 1

    assert config.visualization.legend_ncols == 4


def test_config__from_dict_unexpected_field():
    config_dict = {"name": "test", "unexpected_field": "value"}

    with pytest.raises(
        ValueError, match="Unexpected field 'unexpected_field' in 'SimpleConfig'"
    ):
        SimpleConfig.from_dict(config_dict)
