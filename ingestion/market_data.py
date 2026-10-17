import json
import random
import time
from datetime import datetime, timezone


SYMBOLS = ["XAUUSD", "EURUSD", "USDINR"]


def generate_market_data():
    symbol = random.choice(SYMBOLS)

    base_prices = {
        "XAUUSD": 4350.0,
        "EURUSD": 1.17,
        "USDINR": 92.0,
    
    }

    price = base_prices[symbol]
    price += random.uniform(-price * 0.001, price * 0.001)

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

        print(json.dumps(market_data))

        time.sleep(1)