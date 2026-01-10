from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class Texts:
    data: dict

    def get(self, key: str, **kwargs) -> str:
        if key not in self.data:
            return key

        template = self.data[key]

        try:
            return template.format(**kwargs)
        except Exception:
            return template


def load_texts(lang: str) -> Texts:
    path = Path("texts") / f"{lang}.yml"

    if not path.exists():
        raise RuntimeError(f"Texts file does not exist: {path}")

    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if data is None:
        data = {}

    return Texts(data=data)
