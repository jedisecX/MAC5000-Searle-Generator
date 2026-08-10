# Coil / Magnetic System Design — MAC 5000 Rev. C

**Status:** Transparent calculator is live and corrected. Numerical results remain preliminary and assumption-driven.

## Purpose

Quantify the power required to produce and sustain the magnetic field so we can close:

\[
P_{\rm net} = 500\,{\rm kW} - P_{\rm field} - P_{\rm pump} - P_{\rm cooling} - P_{\rm electronics} - \cdots
\]

## Ampere-turn requirement (idealized toroidal estimate)

At the preliminary design point:

- Target \(B \approx 0.48\,{\rm T}\)
- Mean radius \(r = 0.8\,{\rm m}\)

\[
NI = \frac{B \cdot 2\pi r}{\mu_0} \approx 1.93 \times 10^6\ {\rm A\!-\!turns}
\]

### Rough current / turn trade-off (model points only)

| Turns | Approx. Current |
|-------|-----------------|
| 100   | ~19.3 kA        |
| 250   | ~7.71 kA        |
| 500   | ~3.85 kA        |
| 1 000 | ~1.93 kA        |
| 2 000 | ~964 A          |

These are **not** fabrication recommendations.

## Critical modeling correction

**Packing / fill factor must not be applied to the conductor cross-section when calculating current density.**

Correct physics:

\[
J = \frac{I_{\rm path}}{A_{\rm Cu}}
\]

Packing factor belongs only in the winding-window constraint:

\[
A_{\rm window} \ge \frac{N \, A_{\rm Cu}}{k_{\rm fill}}
\]

The previous version incorrectly reduced the effective copper area for \(J\). That has been fixed.

## Three distinct quantities that must not be conflated

1. **Ampere-turn requirement** \(NI\) — sets the field.
2. **Copper loss** \(P_{\rm Cu} = I^2 R\) — depends on physical conductor area, length, temperature, and parallelization.
3. **Magnetic-field drive power** \(P_{\rm field}\) — for steady DC is primarily copper + core losses; for AC/ramped excitation additional terms appear.

\(k_{\rm core}\) is exposed only as a first-order sensitivity parameter. It is **not** a real magnetic-circuit model (geometry, reluctance, permeability, saturation, and leakage are still missing).

## Live calculator

```
calculations/coil-design/toroidal_field.py
```

Transparent first-order model with the corrected current-density / packing-factor separation.

## Next calculation

Build `coil_sweep.py` over the joint space:

\[
(N,\; P,\; A_{Cu},\; J,\; T,\; B,\; r,\; k_{core},\; k_{fill})
\]

Reject configurations that violate:

- chosen current-density limit
- cooling capacity
- winding-window fit
- conductor current limit
- unreasonable copper volume

Then rank surviving designs by copper loss (and later by full \(P_{\rm field}\)).

## Required before any firm claims

- Conductor type and realistic cross-section
- Winding topology and packing factor
- Operating temperature and cooling method
- Core / yoke decision (real magnetic circuit, not just \(k_{\rm core}\))
- Excitation mode (steady DC vs pulsed/AC)
