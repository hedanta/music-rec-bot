from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import yaml


@dataclass
class Texts:
    path: str

    def __post_init__(self) -> None:
        data = yaml.safe_load(Path(self.path).read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Texts YAML must be a mapping")
        self._data = data

    def get(self, key: str, **kwargs) -> str:
        if key not in self._data:
            return f"[missing text: {key}]"
        value = self._data[key]
        if isinstance(value, str):
            return value.format(**kwargs)
        return str(value)
