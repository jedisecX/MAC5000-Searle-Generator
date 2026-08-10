#!/usr/bin/env python3
"""
MAC 5000 Rev. C — Phase 1 Compliant Coil Sweep
----------------------------------------------
Implements the locked Phase 1 specification:

- B is independently swept
- Three explicitly labeled scenarios (CONSERVATIVE / BASELINE / AGGRESSIVE)
- Analytical thermal fixed-point + runaway detection
- Voltage evaluation
- Full provenance in every CSV row
- Constraint-first evaluation with clear status flags

No hidden defaults that affect feasibility.
"""

from __future__ import annotations
import csv
import math
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any

from toroidal_field import CoilInputs, calculate
from thermal import ThermalInputs, solve as thermal_solve

MODEL_VERSION = "phase1-2026-08-09"

# ---------------------------------------------------------------------------
# Explicit scenario definitions (assumptions, not standards)
# ---------------------------------------------------------------------------

SCENARIOS = {
    "CONSERVATIVE": {
        "J_max": 2.0e6,          # A/m²
        "T_max": 60.0,           # °C
        "T_coolant": 25.0,       # °C
        "R_theta": 0.15,         # K/W  (placeholder — must be justified)
        "V_max": 1000.0,         # V
        "I_path_max": 1500.0,    # A
        "window_max": 0.25,      # m²
        "copper_vol_max": 0.080, # m³
        "note": "passive / low-flow cooling assumption",
    },
    "BASELINE": {
        "J_max": 4.0e6,
        "T_max": 80.0,
        "T_coolant": 30.0,
        "R_theta": 0.08,
        "V_max": 1500.0,
        "I_path_max": 2500.0,
        "window_max": 0.30,
        "copper_vol_max": 0.100,
        "note": "forced liquid/air cooling assumption",
    },
    "AGGRESSIVE": {
        "J_max": 8.0e6,
        "T_max": 120.0,
        "T_coolant": 40.0,
        "R_theta": 0.04,
        "V_max": 2500.0,
        "I_path_max": 4000.0,
        "window_max": 0.40,
        "copper_vol_max": 0.150,
        "note": "engineered forced cooling assumption",
    },
}

B_VALUES = [0.10, 0.20, 0.30, 0.40, 0.48, 0.60, 0.80, 1.00]  # T
MEAN_R = 0.8  # m


@dataclass
class Candidate:
    B: float
    N: int
    parallel: int
    A_cu_mm2: float
    packing: float
    k_core: float


@dataclass
class Evaluated:
    # Provenance
    model_version: str
    timestamp: str
    scenario: str
    # Inputs
    B_T: float
    r_m: float
    N: int
    parallel_paths: int
    A_cu_mm2: float
    packing_factor: float
    k_core: float
    T_coolant_C: float
    R_theta_K_per_W: float
    J_max_A_per_mm2: float
    T_max_C: float
    V_max_V: float
    I_path_max_A: float
    # Derived
    NI: float
    I_total_A: float
    I_path_A: float
    J_A_per_mm2: float
    R_ohm: float
    V_coil_V: float
    P_cu_W: float
    T_cu_C: float
    window_area_m2: float
    copper_volume_L: float
    copper_mass_kg: float
    thermal_stable: bool
    status: str
    notes: str = ""


def evaluate(cand: Candidate, scenario_name: str, scen: Dict[str, Any]) -> Evaluated:
    # Electromagnetic
    inputs = CoilInputs(
        B=cand.B,
        r=MEAN_R,
        N=cand.N,
        A_cu=cand.A_cu_mm2 * 1e-6,
        parallel_paths=cand.parallel,
        T_cu=20.0,               # only used for R20 reference
        k_core=cand.k_core,
        packing_factor=cand.packing,
    )
    em = calculate(inputs)

    # R at 20 °C for the thermal model
    R20 = em.R

    # Thermal fixed-point
    th_inp = ThermalInputs(
        I_total=em.I_total,
        R20=R20,
        T_coolant=scen["T_coolant"],
        R_theta=scen["R_theta"],
    )
    th = thermal_solve(th_inp, method="analytical")

    # Voltage at the solved temperature
    if th.stable and math.isfinite(th.T_cu):
        R_hot = R20 * (1.0 + 0.00393 * (th.T_cu - 20.0))
        V_coil = em.I_total * R_hot
        P_cu = th.P_cu
        T_cu = th.T_cu
    else:
        R_hot = R20
        V_coil = float("inf")
        P_cu = float("inf")
        T_cu = float("inf")

    copper_mass = em.copper_volume * 8960.0

    # Constraint checks
    fails = []
    if not th.stable:
        fails.append("THERMAL_UNSTABLE")
    if em.J > scen["J_max"]:
        fails.append("CURRENT_DENSITY_FAIL")
    if T_cu > scen["T_max"]:
        fails.append("THERMAL_FAIL")
    if em.I_per_path > scen["I_path_max"]:
        fails.append("CONDUCTOR_CURRENT_FAIL")
    if em.A_window_min > scen["window_max"]:
        fails.append("WINDOW_FAIL")
    if em.copper_volume > scen["copper_vol_max"]:
        fails.append("VOLUME_FAIL")
    if V_coil > scen["V_max"]:
        fails.append("VOLTAGE_FAIL")

    if not fails:
        status = "PASS"
    elif len(fails) == 1:
        status = fails[0]
    else:
        status = "MULTI_FAIL"

    return Evaluated(
        model_version=MODEL_VERSION,
        timestamp=datetime.now(timezone.utc).isoformat(),
        scenario=scenario_name,
        B_T=cand.B,
        r_m=MEAN_R,
        N=cand.N,
        parallel_paths=cand.parallel,
        A_cu_mm2=cand.A_cu_mm2,
        packing_factor=cand.packing,
        k_core=cand.k_core,
        T_coolant_C=scen["T_coolant"],
        R_theta_K_per_W=scen["R_theta"],
        J_max_A_per_mm2=scen["J_max"] / 1e6,
        T_max_C=scen["T_max"],
        V_max_V=scen["V_max"],
        I_path_max_A=scen["I_path_max"],
        NI=em.NI,
        I_total_A=em.I_total,
        I_path_A=em.I_per_path,
        J_A_per_mm2=em.J / 1e6,
        R_ohm=R_hot,
        V_coil_V=V_coil,
        P_cu_W=P_cu,
        T_cu_C=T_cu,
        window_area_m2=em.A_window_min,
        copper_volume_L=em.copper_volume * 1e3,
        copper_mass_kg=copper_mass,
        thermal_stable=th.stable,
        status=status,
        notes=";".join(fails) if fails else scen["note"],
    )


def generate_candidates() -> List[Candidate]:
    cands = []
    for B in B_VALUES:
        for N in [250, 500, 1000, 2000, 4000]:
            for P in [1, 2, 4, 8]:
                for A in [50, 100, 200, 400, 800]:
                    for kfill in [0.55, 0.70]:
                        for kcore in [1.0, 1.5]:
                            cands.append(Candidate(
                                B=B, N=N, parallel=P, A_cu_mm2=A,
                                packing=kfill, k_core=kcore
                            ))
    return cands


def write_csv(path: Path, rows: List[Evaluated]) -> None:
    if not rows:
        return
    fieldnames = list(asdict(rows[0]).keys())
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(asdict(r))


def main() -> None:
    print(f"MAC 5000 Phase 1 Coil Sweep  |  model {MODEL_VERSION}")
    print("=" * 60)

    cands = generate_candidates()
    print(f"Candidates generated : {len(cands)}")

    all_results: List[Evaluated] = []
    for sname, scen in SCENARIOS.items():
        print(f"\nScenario: {sname}")
        for c in cands:
            all_results.append(evaluate(c, sname, scen))

    passed = [r for r in all_results if r.status == "PASS"]
    passed.sort(key=lambda r: (r.P_cu_W, r.copper_volume_L, r.I_path_A))

    out = Path(__file__).parent
    write_csv(out / "results_all.csv", all_results)
    write_csv(out / "results_pass.csv", passed)

    print("\n" + "=" * 60)
    print(f"Total evaluated     : {len(all_results)}")
    print(f"PASS designs        : {len(passed)}")
    print("\nTop 8 PASS designs (lowest copper loss):")
    print(f"{'Scen':<12} {'B':>4} {'N':>5} {'P':>3} {'A':>5} {'J':>5} {'Pcu_kW':>8} {'Tcu':>6} {'V':>7}")
    for r in passed[:8]:
        print(f"{r.scenario:<12} {r.B_T:4.2f} {r.N:5d} {r.parallel_paths:3d} "
              f"{r.A_cu_mm2:5.0f} {r.J_A_per_mm2:5.2f} {r.P_cu_W/1e3:8.1f} "
              f"{r.T_cu_C:6.1f} {r.V_coil_V:7.0f}")

    print("\nFiles written: results_all.csv, results_pass.csv")
    print("All assumptions are recorded in every row (full provenance).")


if __name__ == "__main__":
    main()
