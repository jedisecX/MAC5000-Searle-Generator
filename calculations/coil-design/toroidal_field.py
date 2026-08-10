#!/usr/bin/env python3
"""
MAC 5000 Rev. C — Transparent Toroidal Field & Copper Loss Calculator
---------------------------------------------------------------------
First-order model only. Every number is driven by explicit inputs.
Do NOT treat results as final design values.

Key insight from the constant-current-density study:
Parallel paths alone do not reduce copper loss if total copper volume
and current density remain equivalent. Topology, packing, temperature,
and cooling must be optimized together.
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
    A_cu: float               # total copper cross-section per turn [m²]
    parallel_paths: int = 1   # number of parallel conductors
    T_cu: float = 20.0        # copper temperature [°C]
    k_core: float = 1.0       # core factor (1.0 = air-core, >1 if yoke helps)
    packing_factor: float = 0.7  # copper fill factor (0–1)


@dataclass
class CoilResults:
    NI: float
    I_total: float
    I_per_path: float
    J: float                  # current density [A/m²]
    length_per_turn: float
    total_length: float
    rho: float
    R: float
    P_cu: float               # copper loss [W]
    copper_volume: float


def resistivity(T_celsius: float) -> float:
    """Temperature-dependent copper resistivity."""
    return RHO_CU_20C * (1.0 + ALPHA_CU * (T_celsius - 20.0))


def calculate(inputs: CoilInputs) -> CoilResults:
    # Ampere-turns required (idealized toroidal, with optional core factor)
    NI = (inputs.B * 2 * math.pi * inputs.r) / (MU0 * inputs.k_core)

    I_total = NI / inputs.N
    I_per_path = I_total / inputs.parallel_paths

    # Effective copper area accounting for packing
    A_eff = inputs.A_cu * inputs.packing_factor
    J = I_per_path / A_eff if A_eff > 0 else float("inf")

    length_per_turn = 2 * math.pi * inputs.r
    total_length = length_per_turn * inputs.N

    rho = resistivity(inputs.T_cu)
    # Resistance of the whole winding (parallel paths reduce effective R)
    R_single = rho * total_length / inputs.A_cu if inputs.A_cu > 0 else float("inf")
    R = R_single / inputs.parallel_paths

    P_cu = I_total ** 2 * R
    copper_volume = inputs.A_cu * total_length

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
    )


def pretty_print(inputs: CoilInputs, res: CoilResults) -> None:
    print("=== MAC 5000 Coil Calculator (transparent) ===")
    print(f"Target B          : {inputs.B:.3f} T")
    print(f"Mean radius       : {inputs.r:.3f} m")
    print(f"Turns             : {inputs.N}")
    print(f"Parallel paths    : {inputs.parallel_paths}")
    print(f"Cu area / turn    : {inputs.A_cu*1e6:.1f} mm²")
    print(f"Packing factor    : {inputs.packing_factor:.2f}")
    print(f"Copper temp       : {inputs.T_cu:.1f} °C")
    print(f"Core factor       : {inputs.k_core:.2f}")
    print("-" * 40)
    print(f"Required NI       : {res.NI/1e6:.3f} MA-turns")
    print(f"Total current     : {res.I_total:.1f} A")
    print(f"Current / path    : {res.I_per_path:.1f} A")
    print(f"Current density   : {res.J/1e6:.2f} A/mm²")
    print(f"Resistance        : {res.R*1e3:.3f} mΩ")
    print(f"Copper loss       : {res.P_cu/1e6:.3f} MW")
    print(f"Copper volume     : {res.copper_volume*1e3:.2f} L")
    print("=" * 40)


if __name__ == "__main__":
    # Example: the constant-current-density case that produced ~3.19 MW
    demo = CoilInputs(
        B=0.48,
        r=0.8,
        N=1000,
        A_cu=100e-6,          # 100 mm²
        parallel_paths=1,
        T_cu=20.0,
        k_core=1.0,
        packing_factor=1.0,   # idealized for comparison with earlier sweep
    )
    results = calculate(demo)
    pretty_print(demo, results)
