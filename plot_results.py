"""
Generate the P&L distribution histogram for the README.

Compares naive fixed-spread quoting against inventory-aware (AS) quoting
at gamma=2, both quoting the SAME spread width, both run on the same 200
price paths (paired seeds).
"""

import matplotlib
matplotlib.use("Agg")          # write to file, no display needed
import matplotlib.pyplot as plt
import statistics as st

from simulate import simulate_day
from Experiment import as_spread, N_TRIALS, STEP_SIZE

GAMMA = 2.0


def collect(base_spread: float, risk_factor: float) -> list[float]:
    return [
        simulate_day(base_spread=base_spread, risk_factor=risk_factor,
                     seed=seed, step_size=STEP_SIZE)["pnl"]
        for seed in range(N_TRIALS)
    ]


def main():
    spread = as_spread(GAMMA)
    naive = collect(base_spread=spread, risk_factor=0.0)
    smart = collect(base_spread=0.0, risk_factor=GAMMA)

    fig, ax = plt.subplots(figsize=(9, 5))
    bins = 30

    ax.hist(naive, bins=bins, alpha=0.55, label=
            f"Naive fixed spread  (mean {st.mean(naive):.1f}, sd {st.stdev(naive):.1f})")
    ax.hist(smart, bins=bins, alpha=0.55, label=
            f"Inventory-aware, γ={GAMMA:g}  (mean {st.mean(smart):.1f}, sd {st.stdev(smart):.1f})")

    ax.axvline(0, color="black", linewidth=1, linestyle="--", alpha=0.6)

    ax.set_xlabel("Daily P&L")
    ax.set_ylabel("Number of days")
    ax.set_title(f"Daily P&L over {N_TRIALS} simulated days (spread matched at {spread:.3f})")
    ax.legend()
    ax.spines[["top", "right"]].set_visible(False)

    fig.tight_layout()
    fig.savefig("pnl_distribution.png", dpi=150)
    print(f"wrote pnl_distribution.png")
    print(f"naive: mean {st.mean(naive):.2f}  sd {st.stdev(naive):.2f}")
    print(f"AS   : mean {st.mean(smart):.2f}  sd {st.stdev(smart):.2f}")


if __name__ == "__main__":
    main()
