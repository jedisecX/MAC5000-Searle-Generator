# Coil / Magnetic System Design — MAC 5000 Rev. C

**Status:** Phase 1 geometric sensitivity complete. Copper-volume sensitivity experiment added.

## Purpose

Quantify the power required to produce and sustain the magnetic field so we can close:

\[
P_{\rm net} = 500\,{\rm kW} - P_{\rm field} - P_{\rm pump} - P_{\rm cooling} - P_{\rm electronics} - \cdots
\]

## Formal Finding — Geometric Sensitivity Study

> **Phase 1 geometric sensitivity finding:**  
> Under the current single-winding toroidal approximation and the stated Phase 1 constraints, increasing available winding-window area to 10 m² produces **no feasible candidate**. Copper volume becomes the binding constraint.

The attractive low-field example (~270 W copper loss at 0.10 T) requires approximately **16.1 m³ / ~144 tonnes of copper**. Low loss purchased by extreme copper volume is not a viable optimization target.

## Live tools

```
calculations/coil-design/
├── toroidal_field.py
├── thermal.py
├── coil_sweep.py
├── window_sweep.py          # geometric sensitivity (window area)
├── volume_sweep.py          # copper-volume sensitivity (this experiment)
├── plots.py
└── *.csv
```

## Next controlled experiment: copper-volume sensitivity

`volume_sweep.py` freezes every Phase 1 constraint except maximum copper volume and sweeps:

\[
V_{\rm Cu,max} = 0.05,\; 0.10,\; 0.25,\; 0.5,\; 1,\; 2,\; 5,\; 10,\; 20\; {\rm m^3}
\]

Primary recorded output:

- minimum copper volume that produces the first PASS
- corresponding B, turns, parallel paths, conductor area, J, P_Cu, temperature, voltage, window requirement

This establishes the quantitative copper-volume feasibility boundary under the present single-winding topology.

## Architectural implication (to be earned from data)

If the required copper volume remains extreme even after this sweep, the correct response is **not** to loosen the volume limit.  
It is to change the magnetic topology — e.g. to a distributed multi-coil system in which the long single-winding path length \(2\pi r \times N\) is no longer forced.

That architectural change must be justified by the measured copper-volume boundary, not by preference.

## Important boundary

All results remain model-based under the stated assumptions (idealized toroidal field, effective \(k_{\rm core}\), copper properties, thermal resistance, current-density limits). They are not experimental validation of a physical coil.
