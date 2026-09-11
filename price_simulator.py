import random
import math
k=2.4 # order book liquidity parameter
def generate_price_path(start_price: float, num_ticks: int, step_size: float) -> list[float]:

    prices = [start_price]
    for i in range (1,num_ticks):
        direction = 1 if random.randint(0,1) else -1
        prices.append(prices[-1]+direction*step_size)
    return prices
def maybe_generate_incoming_order(fair_price:float,bid_price: float, ask_price: float, act: str ) -> tuple[str, float] | None:
    x=random.random()
    if act=="BUY":
        if x< 0.05*(math.e**(-k*(ask_price-fair_price))):
            return act, ask_price
    if act == "SELL":
        if x < 0.05 * (math.e ** (-k * (fair_price-bid_price))):
            return act, bid_price


