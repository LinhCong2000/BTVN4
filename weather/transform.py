"""Lọc dữ liệu theo khu vực và dựng DataFrame kết quả xổ số."""

import logging

import pandas as pd
from datetime import datetime

logger = logging.getLogger(__name__)

def format_time(time_str: str) -> str:
    dt = datetime.fromisoformat(time_str)

    return dt.strftime("%Y-%m-%d %H:%M:%S")

def extract_weather_data(draws: list[dict]) -> list[dict]:
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
    """Dựng DataFrame với cột ngày và 3 giải đầu (Đặc Biệt, Nhất, Nhì)."""
    return pd.DataFrame(weather_data)


def export_csv(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False, encoding="utf-8-sig")
