# Coil / Magnetic System Design — MAC 5000 Rev. C

**Status:** Transparent calculator is live. Numerical results are still preliminary and assumption-driven.

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

## Critical insight from the first copper-loss study

A constant-current-density sweep produced ~3.19 MW of copper loss for the required ampere-turns — more than six times the 500 kW target. That result is correct and useful: it shows that raw ampere-turns are expensive in copper.

**Parallel paths alone do not reduce copper loss** if total copper volume and current density are held equivalent. They only redistribute the current. Topology, packing factor, temperature, and cooling capacity must be optimized together.

## Three distinct quantities that must not be conflated

1. **Ampere-turn requirement** \(NI\) — sets the field.
2. **Copper loss** \(P_{\rm Cu} = I^2 R\) — depends on conductor cross-section, mean turn length, temperature, and parallelization.
3. **Magnetic-field drive power** \(P_{\rm field}\) — for steady DC is primarily the copper + core losses; for any AC/ramped/pulsed excitation additional reactive, switching, and core-loss terms appear.

## Live calculator

```
calculations/coil-design/toroidal_field.py
```

Transparent first-order model. Inputs:

- \(B\), mean radius, turns, copper area, parallel paths
- copper temperature, packing factor, core factor

Outputs:

- required \(NI\), currents, current density, resistance, copper loss, copper volume

Every number is driven by explicit assumptions. Run it and change the inputs; the losses change accordingly.

## Next calculation

Build `coil_sweep.py` over the joint space:

\[
(N,\; P,\; A_{Cu},\; J,\; T,\; B,\; r,\; k_{core})
\]

Then couple the resulting \(P_{\rm Cu}\) (and eventual \(P_{\rm field}\)) back to the MHD design envelope.

## Required before any firm claims

- Conductor type and realistic cross-section
- Winding topology and packing factor
- Operating temperature and cooling method
- Core / yoke decision
- Excitation mode (steady DC vs pulsed/AC)
