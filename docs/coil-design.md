# Coil / Magnetic System Design — MAC 5000 Rev. C

**Status:** Scaffold only. Numerical results pending proper conductor, topology, and thermal inputs.

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

## Three distinct quantities that must not be conflated

1. **Ampere-turn requirement** \(NI\) — sets the field.
2. **Copper loss** \(P_{\rm Cu} = I^2 R\) — depends on conductor cross-section, mean turn length, and temperature.
3. **Magnetic-field drive power** \(P_{\rm field}\) — for steady DC is primarily the copper + core losses; for any AC/ramped/pulsed excitation additional reactive, switching, and core-loss terms appear.

Until conductor size, winding topology, cooling, and excitation mode are specified, \(P_{\rm field}\) remains unknown.

## Planned calculation artifacts

```
calculations/coil-design/
├── toroidal_field.py
├── coil_sweep.py
└── results.csv
```

## Next inputs required before numerical claims

- Conductor type and cross-section
- Mean turn length / winding geometry
- Operating temperature (affects resistivity)
- Core / yoke presence and material
- Excitation mode (steady DC vs. pulsed / AC)
- Cooling method and thermal limits
