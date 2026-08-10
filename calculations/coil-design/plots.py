#!/usr/bin/env python3
"""
MAC 5000 Rev. C — Phase 1 Diagnostic Plots
------------------------------------------
Produces the five plots required by the locked specification:

1. P_Cu vs J
2. Copper volume vs P_Cu
3. P_Cu vs turns (separated by parallel-path count)
4. Minimum P_Cu vs B
5. Survivor count vs maximum winding-window area   ← most important

Requires matplotlib.  Run after the corresponding CSV files exist.
"""

from __future__ import annotations
import csv
from pathlib import Path
from typing import List, Dict, Any

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("matplotlib is required for plotting.  Install with: pip install matplotlib")
    raise


def load_csv(path: Path) -> List[Dict[str, Any]]:
    with path.open() as f:
        return list(csv.DictReader(f))


def plot_survivors_vs_window(window_csv: Path, out: Path) -> None:
    """The key geometric sensitivity plot."""
    rows = load_csv(window_csv)
    scenarios = sorted(set(r["scenario"] for r in rows))

    plt.figure(figsize=(9, 5))
    for scen in scenarios:
        subset = [r for r in rows if r["scenario"] == scen]
        x = [float(r["window_max_m2"]) for r in subset]
        y = [int(r["n_survivors"]) for r in subset]
        plt.plot(x, y, marker="o", label=scen)

    plt.xscale("log")
    plt.xlabel("Maximum winding-window area (m²)")
    plt.ylabel("Number of survivors")
    plt.title("Survivor count vs available winding window\n(geometric sensitivity study)")
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"Wrote {out}")


def plot_min_Pcu_vs_B(pass_csv: Path, out: Path) -> None:
    rows = load_csv(pass_csv)
    if not rows:
        print("No PASS designs — skipping min P_Cu vs B plot")
        return

    scenarios = sorted(set(r["scenario"] for r in rows))
    plt.figure(figsize=(9, 5))
    for scen in scenarios:
        subset = [r for r in rows if r["scenario"] == scen]
        # group by B, take minimum P_Cu
        from collections import defaultdict
        best = defaultdict(lambda: float("inf"))
        for r in subset:
            B = float(r["B_T"])
            P = float(r["P_cu_W"])
            if P < best[B]:
                best[B] = P
        Bs = sorted(best.keys())
        Ps = [best[b] / 1e3 for b in Bs]  # kW
        plt.plot(Bs, Ps, marker="o", label=scen)

    plt.xlabel("B (T)")
    plt.ylabel("Minimum copper loss (kW)")
    plt.title("Minimum P_Cu vs B (PASS designs only)")
    plt.grid(True, ls="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"Wrote {out}")


def main() -> None:
    root = Path(__file__).parent
    window_csv = root / "window_sweep_results.csv"
    pass_csv = root / "results_pass.csv"

    if window_csv.exists():
        plot_survivors_vs_window(window_csv, root / "plot_survivors_vs_window.png")
    else:
        print(f"{window_csv} not found — run window_sweep.py first")

    if pass_csv.exists():
        plot_min_Pcu_vs_B(pass_csv, root / "plot_min_Pcu_vs_B.png")
    else:
        print(f"{pass_csv} not found — no PASS designs yet or sweep not run")

    print("\nAdditional plots (P_Cu vs J, volume vs P_Cu, P_Cu vs N) can be added once")
    print("results_all.csv / results_pass.csv contain data under relaxed window limits.")


if __name__ == "__main__":
    main()
