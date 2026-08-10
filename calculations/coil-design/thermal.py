#!/usr/bin/env python3
"""
MAC 5000 Rev. C — Analytical Thermal Model (Phase 1)
----------------------------------------------------
Primary calculation uses the closed-form solution for the linear copper model.

    T = (T_c + I² R20 Rθ (1 - 20α)) / (1 - I² R20 Rθ α)

Thermal runaway is declared when the denominator ≤ 0.
An iterative path is retained for verification.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Tuple

ALPHA_CU = 0.00393          # 1/K
RHO_CU_20C = 1.724e-8       # Ω·m


@dataclass
class ThermalInputs:
    I_total: float          # A
    R20: float              # resistance at 20 °C [Ω]
    T_coolant: float        # °C
    R_theta: float          # K/W  (thermal resistance)


@dataclass
class ThermalResult:
    T_cu: float             # steady-state copper temperature [°C]
    stable: bool
    P_cu: float             # W (at the solved temperature)
    note: str = ""


def resistivity(T_celsius: float) -> float:
    return RHO_CU_20C * (1.0 + ALPHA_CU * (T_celsius - 20.0))


def analytical_temperature(inp: ThermalInputs) -> ThermalResult:
    """Closed-form solution for the linear copper model."""
    I2 = inp.I_total ** 2
    denom = 1.0 - I2 * inp.R20 * inp.R_theta * ALPHA_CU

    if denom <= 0.0:
        return ThermalResult(
            T_cu=float("inf"),
            stable=False,
            P_cu=float("inf"),
            note="THERMAL_RUNAWAY (denominator ≤ 0)"
        )

    numer = inp.T_coolant + I2 * inp.R20 * inp.R_theta * (1.0 - 20.0 * ALPHA_CU)
    T = numer / denom
    R_T = inp.R20 * (1.0 + ALPHA_CU * (T - 20.0))
    P = I2 * R_T

    return ThermalResult(T_cu=T, stable=True, P_cu=P, note="analytical")


def iterative_temperature(inp: ThermalInputs, tol: float = 0.01, max_iter: int = 50) -> ThermalResult:
    """Simple fixed-point iteration for verification."""
    T = inp.T_coolant
    for i in range(max_iter):
        R = inp.R20 * (1.0 + ALPHA_CU * (T - 20.0))
        P = inp.I_total ** 2 * R
        T_new = inp.T_coolant + P * inp.R_theta
        if abs(T_new - T) < tol:
            return ThermalResult(T_cu=T_new, stable=True, P_cu=P, note=f"iterative ({i+1})")
        T = T_new
        if T > 1000:          # practical runaway guard
            return ThermalResult(T_cu=T, stable=False, P_cu=P, note="THERMAL_RUNAWAY (iter)")
    return ThermalResult(T_cu=T, stable=False, P_cu=P, note="NO_CONVERGENCE")


def solve(inp: ThermalInputs, method: str = "analytical") -> ThermalResult:
    if method == "analytical":
        return analytical_temperature(inp)
    return iterative_temperature(inp)
