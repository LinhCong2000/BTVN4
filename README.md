# weather Project (bản logging)

Lấy thông tin thời tiết của các thành phố từ API `api.open-meteo.com`, lưu ra JSON và CSV.

Bản này dùng module `logging` chuẩn (như bản gốc) để log tiến trình, và gọi mỗi trang API 1 lần (không retry khi bị rate limit — nếu lỗi thì bỏ qua trang đó và chạy tiếp).

## Cài đặt

```bash
pip install -r requirements.txt
```

## Chạy

```bash
python main.py --cities "Da nang, Hanoi, Hue"
```

Tham số:

| Tham số | Mặc định | Ý nghĩa |
|---|---|---|
| `--cities` | `Da nang` | Thành phố cần lấy thông tin thời tiết |
| `--output-json` | `full_draws.json` | File JSON lưu dữ liệu thô |
| `--output-csv` | `weather_results.csv` | File CSV kết quả thời tiết |
| `--log-level` | `INFO` | Mức log: DEBUG/INFO/WARNING/ERROR |

## Cấu trúc project

```
weather_project/
├── requirements.txt
├── Test Connection/   # test api có chạy được chưa
├── main.py            # CLI entry point
└── weather/
    ├── config.py       # API URL, logging
    ├── api_client.py   # gọi API; lỗi thì bỏ qua trang, chạy tiếp
    ├── storage.py       # đọc/ghi JSON
    └── transform.py     # lọc các trường cần lấy, dựng DataFrame, xuất CSV
```
