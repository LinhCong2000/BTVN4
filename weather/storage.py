"""Đọc/ghi dữ liệu ra file JSON."""

import json


def save_json(data, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
