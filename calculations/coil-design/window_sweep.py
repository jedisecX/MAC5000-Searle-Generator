#!/usr/bin/env python3
"""
MAC 5000 Rev. C — Winding-Window Geometric Sensitivity Study
-------------------------------------------------------------
Freezes the Phase 1 mathematical model and varies ONLY the
available winding-window area.  This is a geometric sensitivity
study, not a physical coil design.

Window areas swept:
    0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0 m²

For every scenario and every window limit we record:
    - number of survivors
    - first feasible B
    - minimum P_Cu among survivors
    - minimum copper mass
    - corresponding current and thermal margin
"""

from __future__ import annotations
import csv
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional

from coil_sweep import (
    SCENARIOS, B_VALUES, MEAN_R, MODEL_VERSION,
    Candidate, evaluate, generate_candidates
)

WINDOW_AREAS = [0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0]  # m²


@dataclass
class WindowResult:
    model_version: str
    timestamp: str
    scenario: str
    window_max_m2: float
    n_candidates: int
    n_survivors: int
    first_feasible_B: Optional[float]
    min_P_cu_W: Optional[float]
    min_copper_mass_kg: Optional[float]
    best_I_path_A: Optional[float]
    best_T_cu_C: Optional[float]
    best_N: Optional[int]
    best_parallel: Optional[int]
    best_A_cu_mm2: Optional[float]
    notes: str = ""


def run_window_sweep() -> List[WindowResult]:
    base_cands = generate_candidates()
    results: List[WindowResult] = []

    for sname, scen in SCENARIOS.items():
        print(f"\n=== Scenario: {sname} ===")
        for wmax in WINDOW_AREAS:
            # Override only the window limit
            scen_mod = dict(scen)
            scen_mod["window_max"] = wmax

            survivors = []
            for c in base_cands:
                ev = evaluate(c, sname, scen_mod)
                if ev.status == "PASS":
                    survivors.append(ev)

            if survivors:
                survivors.sort(key=lambda r: (r.P_cu_W, r.copper_mass_kg))
                best = survivors[0]
                # lowest B that produced at least one survivor
                feasible_Bs = sorted(set(s.B_T for s in survivors))
                first_B = feasible_Bs[0]
                res = WindowResult(
                    model_version=MODEL_VERSION,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    scenario=sname,
                    window_max_m2=wmax,
                    n_candidates=len(base_cands),
                    n_survivors=len(survivors),
                    first_feasible_B=first_B,
                    min_P_cu_W=best.P_cu_W,
                    min_copper_mass_kg=best.copper_mass_kg,
                    best_I_path_A=best.I_path_A,
                    best_T_cu_C=best.T_cu_C,
                    best_N=best.N,
                    best_parallel=best.parallel_paths,
                    best_A_cu_mm2=best.A_cu_mm2,
                    notes="geometric sensitivity only",
                )
            else:
                res = WindowResult(
                    model_version=MODEL_VERSION,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    scenario=sname,
                    window_max_m2=wmax,
                    n_candidates=len(base_cands),
                    n_survivors=0,
                    first_feasible_B=None,
                    min_P_cu_W=None,
                    min_copper_mass_kg=None,
                    best_I_path_A=None,
                    best_T_cu_C=None,
                    best_N=None,
                    best_parallel=None,
                    best_A_cu_mm2=None,
                    notes="no survivors",
                )

            results.append(res)
            print(f"  window={wmax:5.2f} m²  →  survivors={res.n_survivors:4d}  "
                  f"first_B={res.first_feasible_B}  min_Pcu={res.min_P_cu_W}")

    return results


def write_csv(path: Path, rows: List[WindowResult]) -> None:
    if not rows:
        return
    fieldnames = list(asdict(rows[0]).keys())
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(asdict(r))


def main() -> None:
    print(f"MAC 5000 Winding-Window Geometric Sensitivity Study")
    print(f"Model: {MODEL_VERSION}")
    print("This is a geometric sensitivity study, NOT a physical coil design.")
    print("=" * 60)

    results = run_window_sweep()
    out = Path(__file__).parent / "window_sweep_results.csv"
    write_csv(out, results)
    print(f"\nWrote {out}")
    print("Inspect the transition from 0 survivors to the first feasible region.")


if __name__ == "__main__":
    main()
