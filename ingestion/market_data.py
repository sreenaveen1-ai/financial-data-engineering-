import json
import random
import time
from datetime import datetime, timezone

from kafka import KafkaProducer


SYMBOLS = ["XAUUSD", "EURUSD", "USDINR", "BTCUSD"]

BASE_PRICES = {
    "XAUUSD": 4350.0,
    "EURUSD": 1.17,
    "USDINR": 92.0,
    "BTCUSD": 108000.0,
}


producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8"),
)


def generate_market_data():
    symbol = random.choice(SYMBOLS)

    base_price = BASE_PRICES[symbol]

    price = base_price + random.uniform(
        -base_price * 0.001,
        base_price * 0.001,
    )

    return {
        "symbol": symbol,
        "price": round(price, 5),
        "volume": random.randint(1, 1000),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    print("Market data producer started...")

    while True:
        market_data = generate_market_data()

        producer.send("market-data", value=market_data)

        producer.flush()

        print("Sent:", market_data)

        time.sleep(1)
