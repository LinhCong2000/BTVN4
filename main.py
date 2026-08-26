"""CLI: lấy kết quả xổ số Miền Bắc từ API, lưu JSON + CSV.

Ví dụ:
    python main.py --pages 3 --limit 100
"""

import argparse
import logging

from weather.api_client import geocode, get_weather_cities
from weather.config import setup_logging
from weather.storage import save_json
from weather.transform import extract_weather_data, to_dataframe, export_csv

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lấy thông tin thời tiết của các thành phố")
    parser.add_argument("--cities", type=str, default="Da nang", help="Thành phố cần lấy thông tin thời tiết (mặc định: Đà nẵng)")
    parser.add_argument("--output-json", default="full_draws.json", help="File JSON đầu ra")
    parser.add_argument("--output-csv", default="weather_results.csv", help="File CSV đầu ra")
    parser.add_argument(
        "--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"]
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    setup_logging(args.log_level)

    locations = []
    """
        Duyệt từng thành phố , gọi hàm geocode để lấy latitude, longitude tương ứng của thành phố đó
        latitude, longitude sẽ là param đầu vào của hàm get_weather_cities
    """
    cities = [city.strip() for city in args.cities.split(",")] # tách các thành phố đưa về list. vidu: "Da nang, hanoi, Hue" -> ['Da Nang', 'Hanoi', 'Hue']
    for city in cities:
        try:
            city_name, latitude, longitude = geocode(city)
            locations.append({
                "city_name": city_name,
                "latitude": latitude,
                "longitude": longitude
            })

        except ValueError as err:
            logger.warning(err)
            continue

    logger.info("Bắt đầu lấy thông tin thời tiết của thành phố %s", args.cities)
    all_draws = get_weather_cities(locations)
    logger.info("Tổng cộng lấy được %d bản ghi", len(all_draws))

    save_json(all_draws, args.output_json)
    logger.info("Đã lưu dữ liệu thô vào %s", args.output_json)

    weather_data = extract_weather_data(all_draws)
    df = to_dataframe(weather_data)
    export_csv(df, args.output_csv)
    logger.info("Đã lưu thông tin thời tiết của thành phố %s vào %s", args.cities, args.output_csv)


if __name__ == "__main__":
    main()
