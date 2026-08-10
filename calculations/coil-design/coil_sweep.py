#!/usr/bin/env python3
"""
MAC 5000 Rev. C — Constraint-First Coil Sweep
---------------------------------------------
Evaluates candidate windings against hard limits first,
then ranks only the designs that survive.

Status flags:
    PASS
    THERMAL_FAIL
    CURRENT_DENSITY_FAIL
    WINDOW_FAIL
    CONDUCTOR_CURRENT_FAIL
    MULTI_FAIL

The baseline 1 000-turn / 100 mm² case is retained as a permanent
regression check (~3.19 MW copper loss at the preliminary point).
"""

from __future__ import annotations
import csv
import math
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional

from toroidal_field import CoilInputs, calculate, resistivity

# ---------------------------------------------------------------------------
# Hard limits (edit these to change the search space)
# ---------------------------------------------------------------------------

MAX_J           = 5.0e6      # A/m²  (5 A/mm²)
MAX_T_CU        = 90.0       # °C
MAX_I_PATH      = 2000.0     # A per parallel path
MAX_COPPER_VOL  = 0.050      # m³   (50 L)
MAX_WINDOW_AREA = 0.20       # m²   (placeholder — replace with real geometry)
COOLING_CAP_W   = 200e3      # W    (200 kW cooling capacity — placeholder)

# Preliminary design point
TARGET_B = 0.48              # T
MEAN_R   = 0.8               # m


@dataclass
class Candidate:
    N: int
    parallel: int
    A_cu_mm2: float
    T_cu: float
    packing: float
    k_core: float


@dataclass
class Evaluated:
    status: str
    N: int
    parallel: int
    A_cu_mm2: float
    T_cu: float
    packing: float
    k_core: float
    NI: float
    I_total: float
    I_path: float
    J_A_mm2: float
    P_cu_MW: float
    copper_vol_L: float
    window_cm2: float
    notes: str = ""


def evaluate(c: Candidate) -> Evaluated:
    inputs = CoilInputs(
        B=TARGET_B,
        r=MEAN_R,
        N=c.N,
        A_cu=c.A_cu_mm2 * 1e-6,
        parallel_paths=c.parallel,
        T_cu=c.T_cu,
        k_core=c.k_core,
        packing_factor=c.packing,
    )
    res = calculate(inputs)

    fails = []
    if res.J > MAX_J:
        fails.append("CURRENT_DENSITY_FAIL")
    if c.T_cu > MAX_T_CU:
        fails.append("THERMAL_FAIL")
    if res.I_per_path > MAX_I_PATH:
        fails.append("CONDUCTOR_CURRENT_FAIL")
    if res.A_window_min > MAX_WINDOW_AREA:
        fails.append("WINDOW_FAIL")
    if res.P_cu > COOLING_CAP_W:
        fails.append("THERMAL_FAIL")          # cooling capacity exceeded
    if res.copper_volume > MAX_COPPER_VOL:
        fails.append("WINDOW_FAIL")           # treat excessive volume as geometry fail for now

    if not fails:
        status = "PASS"
    elif len(fails) == 1:
        status = fails[0]
    else:
        status = "MULTI_FAIL"

    return Evaluated(
        status=status,
        N=c.N,
        parallel=c.parallel,
        A_cu_mm2=c.A_cu_mm2,
        T_cu=c.T_cu,
        packing=c.packing,
        k_core=c.k_core,
        NI=res.NI,
        I_total=res.I_total,
        I_path=res.I_per_path,
        J_A_mm2=res.J / 1e6,
        P_cu_MW=res.P_cu / 1e6,
        copper_vol_L=res.copper_volume * 1e3,
        window_cm2=res.A_window_min * 1e4,
        notes=";".join(fails) if fails else "",
    )


def baseline_regression() -> Evaluated:
    """Permanent regression case: 1000 turns, 100 mm², should give ~3.19 MW."""
    c = Candidate(N=1000, parallel=1, A_cu_mm2=100.0, T_cu=20.0, packing=0.7, k_core=1.0)
    return evaluate(c)


def generate_candidates() -> List[Candidate]:
    """Small, transparent search space for the first sweep."""
    candidates = []
    for N in [250, 500, 1000, 2000, 4000]:
        for P in [1, 2, 4, 8]:
            for A in [50, 100, 200, 400, 800]:          # mm²
                for T in [20, 40, 60, 80]:
                    for kfill in [0.5, 0.65, 0.8]:
                        for kcore in [1.0, 1.5, 2.0]:
                            candidates.append(
                                Candidate(N=N, parallel=P, A_cu_mm2=A,
                                          T_cu=T, packing=kfill, k_core=kcore)
                            )
    return candidates


def rank_pass(designs: List[Evaluated]) -> List[Evaluated]:
    """Rank only PASS designs by copper loss, then volume, then current/path."""
    passed = [d for d in designs if d.status == "PASS"]
    return sorted(passed, key=lambda d: (d.P_cu_MW, d.copper_vol_L, d.I_path))


def write_csv(path: Path, rows: List[Evaluated]) -> None:
    if not rows:
        return
    fieldnames = list(asdict(rows[0]).keys())
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(asdict(r))


def main() -> None:
    print("Running baseline regression …")
    base = baseline_regression()
    print(f"  Baseline status : {base.status}")
    print(f"  Baseline P_Cu   : {base.P_cu_MW:.3f} MW  (expected ~3.19 MW)")
    print()

    print("Generating candidates …")
    cands = generate_candidates()
    print(f"  {len(cands)} candidates")

    print("Evaluating …")
    results = [evaluate(c) for c in cands]

    passed = rank_pass(results)
    print(f"  PASS designs    : {len(passed)}")

    out_dir = Path(__file__).parent
    write_csv(out_dir / "results_all.csv", results)
    write_csv(out_dir / "results_pass.csv", passed)

    print("\nTop 10 PASS designs (lowest copper loss first):")
    print(f"{'N':>5} {'P':>3} {'A_mm2':>6} {'T':>3} {'kfill':>5} {'kcore':>5} "
          f"{'J':>6} {'Pcu_MW':>8} {'Vol_L':>7} {'Ipath':>7}")
    for d in passed[:10]:
        print(f"{d.N:5d} {d.parallel:3d} {d.A_cu_mm2:6.0f} {d.T_cu:3.0f} "
              f"{d.packing:5.2f} {d.k_core:5.1f} {d.J_A_mm2:6.2f} "
              f"{d.P_cu_MW:8.3f} {d.copper_vol_L:7.2f} {d.I_path:7.1f}")

    print("\nFiles written:")
    print("  results_all.csv   — every candidate with status")
    print("  results_pass.csv  — only PASS designs, ranked")


if __name__ == "__main__":
    main()
