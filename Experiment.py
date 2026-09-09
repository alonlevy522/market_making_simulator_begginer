
import math
import statistics as st

from simulate import simulate_day
from price_simulator import k
"""
 does inventory-aware (Avellaneda-Stoikov) quoting beat naive
fixed-spread quoting, and at what risk_factor?

Method
------
Paired seeds:  every configuration runs on seeds 0..N-1, so each strategy
               faces the identical price paths. Differences come from the
               strategy, not from one drawing a calmer day.

Matched spread: each AS configuration is compared against a naive baseline
               quoting the SAME spread width. Without this, "AS vs naive"
               would confound skew-vs-no-skew with wide-vs-narrow, and any
               result would be uninterpretable.
"""





N_TRIALS = 200
STEP_SIZE = 0.1


def as_spread(risk_factor: float, step_size: float = STEP_SIZE, time: float = 0.0) -> float:
    """
    The spread the AS strategy quotes, for a given risk_factor.

    Mirrors the optimal_spread expression in MarketMaker.get_quotes.
    Evaluated at time=0 (start of day), where the risk term is largest.
    """
    return risk_factor * (step_size ** 2) * (1 - time) + \
        (2 * math.log(1 + risk_factor / k)) / risk_factor


def run_many(base_spread: float, risk_factor: float, n_trials: int = N_TRIALS) -> dict:
    """Run n_trials days of one configuration on seeds 0..n-1 and summarise."""
    runs = [
        simulate_day(base_spread=base_spread, risk_factor=risk_factor,
                     seed=seed, step_size=STEP_SIZE)
        for seed in range(n_trials)
    ]
    pnls = sorted(r["pnl"] for r in runs)
    return {
        "pnl_mean": st.mean(pnls),
        "pnl_std": st.stdev(pnls),
        "worst": pnls[0],
        "var5": pnls[int(0.05 * len(pnls))],       # 5th-percentile day
        "max_inv": st.mean(r["max_abs_inventory"] for r in runs),
        "trades": st.mean(r["trades"] for r in runs),
    }


def main():
    gammas = [0.1, 0.5, 1, 2, 5, 10, 25]

    hdr = f"{'config':>18} {'spread':>7} {'mean':>8} {'std':>8} {'5th pct':>9} {'worst':>8} {'maxInv':>7} {'trades':>7}"
    print(hdr)
    print("-" * len(hdr))

    for gamma in gammas:
        spread = as_spread(gamma)

        smart = run_many(base_spread=0, risk_factor=gamma)
        naive = run_many(base_spread=spread, risk_factor=0.0)

        for label, r in (("naive", naive), (f"AS g={gamma}", smart)):
            print(f"{label:>18} {spread:>7.3f} {r['pnl_mean']:>8.2f} {r['pnl_std']:>8.2f} "
                  f"{r['var5']:>9.2f} {r['worst']:>8.2f} {r['max_inv']:>7.1f} {r['trades']:>7.1f}")
        print()


if __name__ == "__main__":
    main()