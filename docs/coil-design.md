# Coil / Magnetic System Design — MAC 5000 Rev. C

**Status:** Phase 1 computational sweep complete under current constraints. Geometric sensitivity study added.

## Purpose

Quantify the power required to produce and sustain the magnetic field so we can close:

\[
P_{\rm net} = 500\,{\rm kW} - P_{\rm field} - P_{\rm pump} - P_{\rm cooling} - P_{\rm electronics} - \cdots
\]

## Current computational result (preliminary)

Under the Phase 1 constraints as written:

- **0 / 9 600 candidates survived**
- Primary killer: assumed winding-window limit
- Secondary killer: thermal
- Lowest-loss near-survivors concentrate at **low field** (especially ~0.10 T), not at the inherited 0.48 T point

This is an informative negative result, not a project failure.

## Live tools

```
calculations/coil-design/
├── toroidal_field.py      # transparent EM calculator
├── thermal.py             # analytical temperature + runaway detection
├── coil_sweep.py          # Phase 1 constraint-first sweep
├── window_sweep.py        # geometric sensitivity study (window area only)
├── plots.py               # diagnostic plots
├── results_all.csv
├── results_pass.csv
└── window_sweep_results.csv
```

## Geometric sensitivity study

`window_sweep.py` freezes the mathematical model and varies **only** the available winding-window area:

\[
0.1,\; 0.25,\; 0.5,\; 1,\; 2,\; 5,\; 10\; m^2
\]

It records, for every scenario:

- number of survivors
- first feasible B
- minimum copper loss
- minimum copper mass
- corresponding current and temperature

This is explicitly a **geometric sensitivity study**, not a physical coil design. A 2 m² cross-sectional area does not automatically mean a physically realizable winding once radial/axial build, insulation, cooling passages, and clearances are considered.

## Diagnostic plots (`plots.py`)

1. Survivor count vs maximum winding-window area  ← key transition plot
2. Minimum P_Cu vs B (once survivors exist)
3. (Additional plots activated once a feasible region appears)

## Important boundary

A `PASS` design only means it survived the stated Phase 1 coil constraints under the stated assumptions.  
It is **not** yet a viable MAC 5000 field system.

## Next experiment

Run `window_sweep.py` and inspect the transition:

\[
\text{0 survivors} \;\rightarrow\; \text{first feasible region}
\]

That curve will show whether the original 1.60 m envelope can supply enough winding volume, or whether a radically different coil architecture is required.
