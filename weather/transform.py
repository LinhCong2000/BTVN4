"""Lọc các trường thông tin cần lấy và dựng DataFrame."""

import logging

import pandas as pd
from datetime import datetime

logger = logging.getLogger(__name__)

def format_time(time_str: str) -> str:
    """Lưu theo múi giờ Việt Nam, đưa về định dạng Y-m-d H:M:S"""
    dt = datetime.fromisoformat(time_str)

    return dt.strftime("%Y-%m-%d %H:%M:%S")

def extract_weather_data(draws: list[dict]) -> list[dict]:
    """Lọc các trường thông tin cần lấy và dựng DataFrame."""
    rows = []
    for draw in draws:
        current = draw.get("current")
        if current: #nếu có thông tin thời tiết trả về thì lấy các trường cần lấy
            rows.append(
                {
                    "Thành phố": draw["city_name"],
                    "Thời điểm": format_time(current["time"]),
                    "Nhiệt độ không khí": current.get("temperature_2m"),
                    "Độ ẩm tương đối": current.get("relative_humidity_2m"),
                    "Tốc độ gió": current.get("wind_speed_10m"),
                }
        )
    return rows


def to_dataframe(weather_data: list[dict]) -> pd.DataFrame:
    """Dựng DataFrame"""
    return pd.DataFrame(weather_data)


def export_csv(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False, encoding="utf-8-sig")
