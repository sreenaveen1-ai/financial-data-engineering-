import json
import glob

import psycopg2


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "market_data",
    "user": "financial",
    "password": "financial",
}


def load_gold_data():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    files = glob.glob("data/gold/market-summary/part-*.json")

    inserted = 0

    for file in files:
        with open(file, "r") as f:
            for line in f:
                if not line.strip():
                    continue

                record = json.loads(line)

                window = record["window"]

                cursor.execute(
                    """
                   INSERT INTO market_summary (
    window_start,
    window_end,
    symbol,
    avg_price,
    min_price,
    max_price,
    total_volume,
    tick_count
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (window_start, window_end, symbol)
DO NOTHING
                    """,
                    (
                        window["start"],
                        window["end"],
                        record["symbol"],
                        record["avg_price"],
                        record["min_price"],
                        record["max_price"],
                        record["total_volume"],
                        record["tick_count"],
                    ),
                )

                inserted += 1

    conn.commit()

    cursor.close()
    conn.close()

    print(f"Inserted {inserted} records into PostgreSQL.")


if __name__ == "__main__":
    load_gold_data()
