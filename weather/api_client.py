"""Gọi API open-meteo.com: lấy thông tin thời tiết của 1 hoặc nhiều thành phố."""

import logging

import requests

from .config import GEOCODE_URL, WEATHER_URL

logger = logging.getLogger(__name__)


def geocode(city: str) -> tuple[float, float]:
    """Gọi api search để lấy lat, lng của thành phố. lat, lng sẽ là đầu vào của hàm get_weather_city """
    params = {"name": city, "count": 1}
    response = requests.get(GEOCODE_URL, params=params)
    response.raise_for_status()
    data = response.json()
    results = data.get("results")
    if not results:
        raise ValueError(
            f"Không tìm thấy thành phố: {city}"
        )
    
    location = results[0]
    return (
        location["name"],
        location["latitude"],
        location["longitude"]
    )

def get_weather_city(latitude: float, longitude: float) -> list[dict]:
    """
        Lấy thông tin thời tiết của 1 thành phố dựa vào lat, lng.
        temperature_2m: Nhiệt độ không khí ở độ cao 2m so với mặt đất
        relative_humidity_2m: Độ ẩm tương đối ở độ cao 2m
        wind_speed_10m: Tốc độ gió ở độ cao 2m
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "timezone": "Asia/Bangkok"
        }
    response = requests.get(WEATHER_URL, params=params)
    response.raise_for_status()
    return response.json()

def get_weather_cities(locations: list[tuple[str, float, float]]) -> list[dict]:
    """
    Lặp qua danh sách thành phố, gọi API weather cho từng thành phố và gộp kết quả thành một list phẳng.

    Nếu một thành phố bị lỗi HTTP,  bỏ qua thành phố đó và chạy tiếp.
    """
    all_draw: list[dict] = []

    for location in locations:
        city_name = location["city_name"]
        latitude = location["latitude"]
        longitude = location["longitude"]
        try:
            payload = get_weather_city(latitude, longitude)
            payload["city_name"] = city_name
            all_draw.append(payload)
            logger.info("Đã lấy thông tin thời tiết của thành phố %s ", city_name)
        except requests.exceptions.HTTPError as http_err:
            logger.warning("Bỏ qua thành phố %s do lỗi HTTP: %s", city_name, http_err)

    return all_draw

