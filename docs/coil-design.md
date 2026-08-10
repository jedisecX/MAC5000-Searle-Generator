# Coil / Magnetic System Design — MAC 5000 Rev. C

**Status:** Phase 1 implementation is now compliant with the locked specification.

## Purpose

Quantify the power required to produce and sustain the magnetic field so we can close:

\[
P_{\rm net} = 500\,{\rm kW} - P_{\rm field} - P_{\rm pump} - P_{\rm cooling} - P_{\rm electronics} - \cdots
\]

## Phase 1 Deliverables (live)

```
calculations/coil-design/
├── toroidal_field.py   # transparent EM calculator (corrected packing factor)
├── thermal.py          # analytical temperature + runaway detection
├── coil_sweep.py       # Phase 1 compliant sweep
├── results_all.csv     # every candidate with full provenance
└── results_pass.csv    # survivors only
```

## What the sweep now does

- Independently sweeps **B** from 0.10 T to 1.00 T
- Runs three explicitly labeled scenarios (assumptions, not standards):

| Scenario     | Continuous J_max | T_max | Cooling assumption          |
|--------------|------------------|-------|-----------------------------|
| CONSERVATIVE | 2 A/mm²          | 60 °C | passive / low-flow          |
| BASELINE     | 4 A/mm²          | 80 °C | forced liquid/air           |
| AGGRESSIVE   | 8 A/mm²          | 120 °C| engineered forced cooling   |

- Uses the analytical thermal fixed-point:

\[
T = \frac{T_c + I^2 R_{20} R_\theta (1-20\alpha)}{1 - I^2 R_{20} R_\theta \alpha}
\]

with explicit thermal-runaway detection when the denominator ≤ 0.

- Evaluates voltage \(V = IR\)
- Applies constraint-first filtering (current density, temperature, window, volume, conductor current, voltage, thermal stability)
- Writes full provenance on every CSV row (model version, timestamp, scenario, all inputs and limits)

## Important boundary

A `PASS` design only means it survived the Phase 1 coil constraints under the stated assumptions.  
It is **not** yet a viable MAC 5000 field system. Magnetic geometry, pump power, cooling plant, MHD extraction losses, and system-level \(P_{\rm net}\) still have to be coupled afterward.

## Next steps after Phase 1 data exists

1. Inspect the feasible region (especially \(B\) vs \(P_{\rm Cu}\))
2. Replace placeholder thermal-resistance and window values with measured or justified numbers
3. Add the diagnostic plots
4. Only then fold surviving \(P_{\rm field}\) candidates into the MHD energy balance
