#!/usr/bin/env python3
"""
MAC 5000 Rev. C — Phase 1 Diagnostic Plots (complete set)
---------------------------------------------------------
1. P_Cu vs J
2. Copper volume vs P_Cu
3. P_Cu vs turns (separated by parallel-path count)
4. Minimum P_Cu vs B
5. Survivor count vs maximum winding-window area   ← key transition plot

Requires matplotlib. Run after the corresponding CSV files exist.
Gracefully skips plots that have no data.
"""

from __future__ import annotations
import csv
from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Any

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("matplotlib is required. Install with: pip install matplotlib")
    raise


def load_csv(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    with path.open() as f:
        return list(csv.DictReader(f))


def _f(row: Dict[str, Any], key: str, default=None):
    try:
        return float(row[key])
    except (KeyError, ValueError, TypeError):
        return default


def plot_Pcu_vs_J(all_csv: Path, out: Path) -> None:
    rows = [r for r in load_csv(all_csv) if r.get("status") == "PASS"]
    if not rows:
        print("No PASS designs — skipping P_Cu vs J")
        return

    plt.figure(figsize=(8, 5))
    scenarios = sorted(set(r["scenario"] for r in rows))
    for scen in scenarios:
        subset = [r for r in rows if r["scenario"] == scen]
        J = [_f(r, "J_A_per_mm2") for r in subset]
        P = [_f(r, "P_cu_W") / 1e3 for r in subset]  # kW
        plt.scatter(J, P, s=18, alpha=0.7, label=scen)

    plt.xlabel("Current density J (A/mm²)")
    plt.ylabel("Copper loss P_Cu (kW)")
    plt.title("P_Cu vs Current Density (PASS designs)")
    plt.grid(True, ls="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"Wrote {out}")


def plot_volume_vs_Pcu(all_csv: Path, out: Path) -> None:
    rows = [r for r in load_csv(all_csv) if r.get("status") == "PASS"]
    if not rows:
        print("No PASS designs — skipping copper volume vs P_Cu")
        return

    plt.figure(figsize=(8, 5))
    scenarios = sorted(set(r["scenario"] for r in rows))
    for scen in scenarios:
        subset = [r for r in rows if r["scenario"] == scen]
        V = [_f(r, "copper_volume_L") for r in subset]
        P = [_f(r, "P_cu_W") / 1e3 for r in subset]
        plt.scatter(V, P, s=18, alpha=0.7, label=scen)

    plt.xlabel("Copper volume (L)")
    plt.ylabel("Copper loss P_Cu (kW)")
    plt.title("Copper Volume vs P_Cu (PASS designs)")
    plt.grid(True, ls="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"Wrote {out}")


def plot_Pcu_vs_turns(all_csv: Path, out: Path) -> None:
    rows = [r for r in load_csv(all_csv) if r.get("status") == "PASS"]
    if not rows:
        print("No PASS designs — skipping P_Cu vs turns")
        return

    plt.figure(figsize=(9, 5))
    # group by parallel paths
    paths = sorted(set(int(float(r["parallel_paths"])) for r in rows))
    for p in paths:
        subset = [r for r in rows if int(float(r["parallel_paths"])) == p]
        N = [int(float(r["N"])) for r in subset]
        P = [_f(r, "P_cu_W") / 1e3 for r in subset]
        plt.scatter(N, P, s=18, alpha=0.7, label=f"P={p}")

    plt.xlabel("Number of turns N")
    plt.ylabel("Copper loss P_Cu (kW)")
    plt.title("P_Cu vs Turns (colored by parallel-path count)")
    plt.grid(True, ls="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"Wrote {out}")


def plot_min_Pcu_vs_B(pass_csv: Path, out: Path) -> None:
    rows = load_csv(pass_csv)
    if not rows:
        print("No PASS designs — skipping min P_Cu vs B")
        return

    plt.figure(figsize=(8, 5))
    scenarios = sorted(set(r["scenario"] for r in rows))
    for scen in scenarios:
        subset = [r for r in rows if r["scenario"] == scen]
        best = defaultdict(lambda: float("inf"))
        for r in subset:
            B = _f(r, "B_T")
            P = _f(r, "P_cu_W")
            if B is not None and P is not None and P < best[B]:
                best[B] = P
        Bs = sorted(best.keys())
        Ps = [best[b] / 1e3 for b in Bs]
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


def plot_survivors_vs_window(window_csv: Path, out: Path) -> None:
    """Key geometric sensitivity plot."""
    rows = load_csv(window_csv)
    if not rows:
        print(f"{window_csv} empty or missing — skipping survivors vs window")
        return

    plt.figure(figsize=(9, 5))
    scenarios = sorted(set(r["scenario"] for r in rows))
    for scen in scenarios:
        subset = [r for r in rows if r["scenario"] == scen]
        x = [_f(r, "window_max_m2") for r in subset]
        y = [int(float(r["n_survivors"])) for r in subset]
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


def main() -> None:
    root = Path(__file__).parent
    all_csv = root / "results_all.csv"
    pass_csv = root / "results_pass.csv"
    window_csv = root / "window_sweep_results.csv"

    print("MAC 5000 Phase 1 Diagnostic Plots")
    print("=" * 40)

    plot_Pcu_vs_J(all_csv, root / "plot_Pcu_vs_J.png")
    plot_volume_vs_Pcu(all_csv, root / "plot_volume_vs_Pcu.png")
    plot_Pcu_vs_turns(all_csv, root / "plot_Pcu_vs_turns.png")
    plot_min_Pcu_vs_B(pass_csv, root / "plot_min_Pcu_vs_B.png")
    plot_survivors_vs_window(window_csv, root / "plot_survivors_vs_window.png")

    print("\nDone. Plots that lack data were skipped cleanly.")


if __name__ == "__main__":
    main()
