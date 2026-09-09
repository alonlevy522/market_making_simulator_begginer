from price_simulator import generate_price_path,maybe_generate_incoming_order
from market_maker import MarketMaker
import random
def simulate_day(
        base_spread: float = 0.0,
        risk_factor: float = 0.1,
        seed: int | None = None,
        num_ticks: int = 2500,
        step_size: float = 0.1,
        start_price: float = 100.0,
) -> dict:
    """

    base_spread = 0  -> Avellaneda-Stoikov quoting (inventory-aware)
    base_spread > 0  -> naive fixed-spread quoting (no skew)
"""

    if seed is not None:
        random.seed(seed)

    prices = generate_price_path(start_price, num_ticks, step_size)
    mm = MarketMaker(
        base_spread=base_spread,
        risk_factor=risk_factor,
        sigma=step_size,
    )

    max_abs_inventory = 0
    bid_fills = 0
    ask_fills = 0

    for tick, fair_value in enumerate(prices):
        bid, ask = mm.get_quotes(fair_value, (tick + 1) / num_ticks)

        incoming = maybe_generate_incoming_order(fair_value, bid, ask, "BUY")
        if incoming is not None:
            mm.record_fill(incoming[0], incoming[1], 1)
            ask_fills += 1

        incoming = maybe_generate_incoming_order(fair_value, bid, ask, "SELL")
        if incoming is not None:
            mm.record_fill(incoming[0], incoming[1], 1)
            bid_fills += 1

        max_abs_inventory = max(max_abs_inventory, abs(mm.inventory))

    return {
        "pnl": mm.cash + mm.inventory * prices[-1],
        "cash": mm.cash,
        "final_inventory": mm.inventory,
        "max_abs_inventory": max_abs_inventory,
        "bid_fills": bid_fills,
        "ask_fills": ask_fills,
        "trades": bid_fills + ask_fills,
    }


if __name__ == "__main__":
    r = simulate_day(seed=0)
    print(f"P&L: {r['pnl']:.2f}")
    print(f"Final inventory: {r['final_inventory']}")
    print(f"Max inventory held: {r['max_abs_inventory']}")
    print(f"Trades: {r['trades']} ({r['bid_fills']} bid / {r['ask_fills']} ask)")


