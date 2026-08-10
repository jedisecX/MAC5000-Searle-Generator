#!/usr/bin/env python3
"""
MAC 5000 Rev. C — Copper-Volume Sensitivity Study
-------------------------------------------------
Freezes the Phase 1 mathematical model and varies ONLY the
maximum allowed copper volume.  All other constraints remain
exactly as defined in the locked Phase 1 specification.

Volume limits swept:
    0.05, 0.10, 0.25, 0.5, 1, 2, 5, 10, 20 m³

Primary output:
    minimum copper volume that produces the first PASS,
    together with the corresponding design parameters.

This is a controlled sensitivity experiment, not a design change.
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

VOLUME_LIMITS = [0.05, 0.10, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0]  # m³


@dataclass
class VolumeResult:
    model_version: str
    timestamp: str
    scenario: str
    copper_vol_max_m3: float
    n_candidates: int
    n_survivors: int
    first_feasible_B: Optional[float]
    min_P_cu_W: Optional[float]
    min_copper_volume_L: Optional[float]
    min_copper_mass_kg: Optional[float]
    best_I_path_A: Optional[float]
    best_T_cu_C: Optional[float]
    best_V_coil_V: Optional[float]
    best_J_A_mm2: Optional[float]
    best_N: Optional[int]
    best_parallel: Optional[int]
    best_A_cu_mm2: Optional[float]
    best_window_m2: Optional[float]
    notes: str = ""


def run_volume_sweep() -> List[VolumeResult]:
    base_cands = generate_candidates()
    results: List[VolumeResult] = []

    for sname, scen in SCENARIOS.items():
        print(f"\n=== Scenario: {sname} ===")
        for vmax in VOLUME_LIMITS:
            scen_mod = dict(scen)
            scen_mod["copper_vol_max"] = vmax
            # Keep the original window limit (do not loosen it)
            # scen_mod["window_max"] stays as defined in SCENARIOS

            survivors = []
            for c in base_cands:
                ev = evaluate(c, sname, scen_mod)
                if ev.status == "PASS":
                    survivors.append(ev)

            if survivors:
                survivors.sort(key=lambda r: (r.copper_volume_L, r.P_cu_W))
                best = survivors[0]
                feasible_Bs = sorted(set(s.B_T for s in survivors))
                res = VolumeResult(
                    model_version=MODEL_VERSION,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    scenario=sname,
                    copper_vol_max_m3=vmax,
                    n_candidates=len(base_cands),
                    n_survivors=len(survivors),
                    first_feasible_B=feasible_Bs[0],
                    min_P_cu_W=best.P_cu_W,
                    min_copper_volume_L=best.copper_volume_L,
                    min_copper_mass_kg=best.copper_mass_kg,
                    best_I_path_A=best.I_path_A,
                    best_T_cu_C=best.T_cu_C,
                    best_V_coil_V=best.V_coil_V,
                    best_J_A_mm2=best.J_A_per_mm2,
                    best_N=best.N,
                    best_parallel=best.parallel_paths,
                    best_A_cu_mm2=best.A_cu_mm2,
                    best_window_m2=best.window_area_m2,
                    notes="volume sensitivity only; window limit unchanged",
                )
            else:
                res = VolumeResult(
                    model_version=MODEL_VERSION,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    scenario=sname,
                    copper_vol_max_m3=vmax,
                    n_candidates=len(base_cands),
                    n_survivors=0,
                    first_feasible_B=None,
                    min_P_cu_W=None,
                    min_copper_volume_L=None,
                    min_copper_mass_kg=None,
                    best_I_path_A=None,
                    best_T_cu_C=None,
                    best_V_coil_V=None,
                    best_J_A_mm2=None,
                    best_N=None,
                    best_parallel=None,
                    best_A_cu_mm2=None,
                    best_window_m2=None,
                    notes="no survivors",
                )

            results.append(res)
            print(f"  Vmax={vmax:5.2f} m³  →  survivors={res.n_survivors:4d}  "
                  f"first_B={res.first_feasible_B}  min_vol={res.min_copper_volume_L}")

    return results


def write_csv(path: Path, rows: List[VolumeResult]) -> None:
    if not rows:
        return
    fieldnames = list(asdict(rows[0]).keys())
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(asdict(r))


def main() -> None:
    print("MAC 5000 Copper-Volume Sensitivity Study")
    print(f"Model: {MODEL_VERSION}")
    print("Freezes all Phase 1 constraints except maximum copper volume.")
    print("=" * 60)

    results = run_volume_sweep()
    out = Path(__file__).parent / "volume_sweep_results.csv"
    write_csv(out, results)
    print(f"\nWrote {out}")

    # Summary: first appearance of a survivor for each scenario
    print("\n=== Minimum copper volume for first PASS ===")
    for sname in SCENARIOS:
        scen_rows = [r for r in results if r.scenario == sname and r.n_survivors > 0]
        if scen_rows:
            first = min(scen_rows, key=lambda r: r.copper_vol_max_m3)
            print(f"{sname:12s}  first PASS at Vmax={first.copper_vol_max_m3} m³  "
                  f"(actual vol={first.min_copper_volume_L:.1f} L, "
                  f"B={first.first_feasible_B} T, Pcu={first.min_P_cu_W:.0f} W)")
        else:
            print(f"{sname:12s}  no PASS even at 20 m³")


if __name__ == "__main__":
    main()
