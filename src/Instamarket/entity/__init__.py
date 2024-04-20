from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path

@dataclass(frozen=True)
class DataPreprocessingConfig:
    root_dir: Path
    data_path: Path
    clean_data_file: Path

@dataclass(frozen=True)
class DataPreparationConfig:
    root_dir: Path
    data_path: Path

@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_path: Path
    preprocessor_file: Path

