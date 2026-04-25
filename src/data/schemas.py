import json
from pathlib import Path


def save_schema(schema: dict, path: str):
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2)


def load_schema(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)