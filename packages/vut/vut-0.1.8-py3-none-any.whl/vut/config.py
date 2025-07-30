from dataclasses import dataclass, field
from typing import Any, Self


@dataclass
class BaseConfig:
    @classmethod
    def from_dict(cls, config_dict: dict[str, Any]) -> Self:
        field_types = {f.name: f.type for f in cls.__dataclass_fields__.values()}
        init_args = {}
        for key, value in config_dict.items():
            if key in field_types:
                field_type = field_types[key]
                if hasattr(field_type, "__dataclass_fields__"):
                    init_args[key] = field_type.from_dict(value)
                else:
                    init_args[key] = value
            else:
                raise ValueError(f"Unexpected field '{key}' in '{cls.__name__}'.")
        return cls(**init_args)


@dataclass
class ModelConfig(BaseConfig):
    name: str


@dataclass
class DatasetConfig(BaseConfig):
    name: str
    num_classes: int = 0
    num_actions: int = 0
    backgrounds: list[str] = field(default_factory=list)
    input_dim: int = 0

    split_dir: str = None
    split_file_name: str = None
    gt_dir: str = None
    feature_dir: str = None
    video_dir: str = None
    class_mapping_path: str = None
    class_mapping_has_header: bool = False
    class_mapping_separator: str = ","
    action_mapping_path: str = None
    action_mapping_has_header: bool = False
    action_mapping_action_separator: str = ","
    action_mapping_step_separator: str = " "
    video_action_mapping_path: str = None
    video_action_mapping_has_header: bool = False
    video_action_mapping_separator: str = ","
    video_boundary_dir_path: str = None
    video_boundary_has_header: bool = False
    video_boundary_separator: str = ","


@dataclass
class TrainingConfig(BaseConfig):
    epochs: int = 100
    split: int = 0
    num_fold: int = 0
    lr: float = 0.001
    batch_size: int = 32
    sampling_rate: int = 1
    shuffle: bool = True


@dataclass
class VisualizationConfig(BaseConfig):
    legend_ncols: int = 3


@dataclass
class Config(BaseConfig):
    seed: int = 42
    device: str = "cuda"
    result_dir: str = "results"
    val_skip: bool = False
    model_dir: str = "models"
    model_file_name: str = "model.pth"

    model: ModelConfig = field(default_factory=lambda: ModelConfig(name="none"))
    dataset: DatasetConfig = field(default_factory=lambda: DatasetConfig(name="none"))
    training: TrainingConfig = field(default_factory=lambda: TrainingConfig())
    visualization: VisualizationConfig = field(
        default_factory=lambda: VisualizationConfig()
    )
