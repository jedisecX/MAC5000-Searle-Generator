#!/usr/bin/env python3
"""
MAC 5000 Rev. C — Transparent Toroidal Field & Copper Loss Calculator
---------------------------------------------------------------------
First-order model only. Every number is driven by explicit inputs.
Do NOT treat results as final design values.

Key modeling rules (Rev. C corrected):
- Current density uses the physical copper cross-section of the conductor:
      J = I_path / A_Cu
- Packing / fill factor belongs in the winding-window constraint, not in J:
      A_window >= (N * A_Cu) / k_fill
- k_core is only a first-order effective field factor, not a real magnetic-circuit model.
"""

from __future__ import annotations
import math
from dataclasses import dataclass

MU0 = 4 * math.pi * 1e-7  # H/m
RHO_CU_20C = 1.724e-8     # Ω·m at 20 °C
ALPHA_CU = 0.00393        # temperature coefficient of resistivity (1/K)


@dataclass
class CoilInputs:
    B: float                  # target field [T]
    r: float                  # mean radius [m]
    N: int                    # turns
    A_cu: float               # physical copper cross-section of one conductor [m²]
    parallel_paths: int = 1   # number of parallel conductors
    T_cu: float = 20.0        # copper temperature [°C]
    k_core: float = 1.0       # first-order effective field factor (1.0 = air-core)
    packing_factor: float = 0.7  # fill factor for winding-window constraint only


@dataclass
class CoilResults:
    NI: float
    I_total: float
    I_per_path: float
    J: float                  # current density in the copper [A/m²]
    length_per_turn: float
    total_length: float
    rho: float
    R: float
    P_cu: float               # copper loss [W]
    copper_volume: float
    A_window_min: float       # minimum winding window area required by packing


def resistivity(T_celsius: float) -> float:
    """Temperature-dependent copper resistivity."""
    return RHO_CU_20C * (1.0 + ALPHA_CU * (T_celsius - 20.0))


def calculate(inputs: CoilInputs) -> CoilResults:
    # Ampere-turns required (idealized toroidal + first-order core factor)
    # Note: k_core is a sensitivity parameter only, not a full magnetic circuit.
    NI = (inputs.B * 2 * math.pi * inputs.r) / (MU0 * inputs.k_core)

    I_total = NI / inputs.N
    I_per_path = I_total / inputs.parallel_paths

    # Current density uses the physical copper area of the conductor.
    # Packing factor does NOT shrink A_cu here.
    J = I_per_path / inputs.A_cu if inputs.A_cu > 0 else float("inf")

    length_per_turn = 2 * math.pi * inputs.r
    total_length = length_per_turn * inputs.N

    rho = resistivity(inputs.T_cu)

    # Resistance of the whole winding (parallel paths reduce effective R)
    R_single = rho * total_length / inputs.A_cu if inputs.A_cu > 0 else float("inf")
    R = R_single / inputs.parallel_paths

    P_cu = I_total ** 2 * R
    copper_volume = inputs.A_cu * total_length

    # Packing factor belongs in the winding-window constraint
    A_window_min = (inputs.N * inputs.A_cu) / inputs.packing_factor if inputs.packing_factor > 0 else float("inf")

    return CoilResults(
        NI=NI,
        I_total=I_total,
        I_per_path=I_per_path,
        J=J,
        length_per_turn=length_per_turn,
        total_length=total_length,
        rho=rho,
        R=R,
        P_cu=P_cu,
        copper_volume=copper_volume,
        A_window_min=A_window_min,
    )


def pretty_print(inputs: CoilInputs, res: CoilResults) -> None:
    print("=== MAC 5000 Coil Calculator (transparent, corrected) ===")
    print(f"Target B          : {inputs.B:.3f} T")
    print(f"Mean radius       : {inputs.r:.3f} m")
    print(f"Turns             : {inputs.N}")
    print(f"Parallel paths    : {inputs.parallel_paths}")
    print(f"Cu area / path    : {inputs.A_cu*1e6:.1f} mm²")
    print(f"Packing factor    : {inputs.packing_factor:.2f}  (window constraint only)")
    print(f"Copper temp       : {inputs.T_cu:.1f} °C")
    print(f"Core factor       : {inputs.k_core:.2f}  (first-order sensitivity)")
    print("-" * 45)
    print(f"Required NI       : {res.NI/1e6:.3f} MA-turns")
    print(f"Total current     : {res.I_total:.1f} A")
    print(f"Current / path    : {res.I_per_path:.1f} A")
    print(f"Current density J : {res.J/1e6:.2f} A/mm²")
    print(f"Resistance        : {res.R*1e3:.3f} mΩ")
    print(f"Copper loss       : {res.P_cu/1e6:.3f} MW")
    print(f"Copper volume     : {res.copper_volume*1e3:.2f} L")
    print(f"Min. window area  : {res.A_window_min*1e4:.1f} cm²")
    print("=" * 45)


if __name__ == "__main__":
    # Reproduce the earlier constant-current-density illustration
    # (packing factor no longer affects J)
    demo = CoilInputs(
        B=0.48,
        r=0.8,
        N=1000,
        A_cu=100e-6,          # 100 mm² physical copper
        parallel_paths=1,
        T_cu=20.0,
        k_core=1.0,
        packing_factor=0.7,
    )
    results = calculate(demo)
    pretty_print(demo, results)
