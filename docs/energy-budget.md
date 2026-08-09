# Energy Budget Requirements — MAC 5000 Rev. C

## Why This Document Exists

Rev. B claimed 500 kW continuous at 92–95 % efficiency without a complete loss accounting.  
That is insufficient for an engineering design.

## Required Accounting

For any claimed electrical output \(P_{out}\):

\[
P_{in} = \frac{P_{out}}{\eta}
\]

At 500 kW and 95 %:

\[
P_{in} \approx 526.3\,\text{kW}
\]

At 92 %:

\[
P_{in} \approx 543.5\,\text{kW}
\]

The difference (26–44 kW) is the maximum allowable total loss at full power. Every loss mechanism must be quantified and summed.

## Loss Categories That Must Be Budgeted

| Category                        | Notes                                      | Status in Rev. B |
|---------------------------------|--------------------------------------------|------------------|
| Magnetic field drive power      | Power to sustain the toroidal/poloidal coils | Not quantified  |
| Coil I²R losses                 | Ohmic heating in drive + pickup windings   | Not quantified  |
| Power electronics / inverter    | Rectifier, MPPT, DC link, inversion        | Not quantified  |
| Liquid-metal viscous dissipation| \(\mu \nabla^2 v\) term integrated over volume | Not quantified |
| Pump / circulation power        | If any external pumping is used            | Not quantified  |
| Magnetic hysteresis & eddy currents | Core and structural materials           | Not quantified  |
| Cooling system parasitic load   | Pumps, fans, chillers                      | Not quantified  |
| Bearing / mechanical losses     | If any rotating elements remain            | Not quantified  |
| Control & instrumentation       | Sensors, processors, actuators             | Minor but required |
| Parasitic currents / leakage    | Induced currents in structure, shields     | Not quantified  |
| Thermal radiation / conduction  | Heat rejection path                        | Not quantified  |

## Acceptance Criterion for Rev. C

A claimed operating point is only accepted when:

1. Every term above has a calculated or measured value.
2. The sum of losses is consistent with the stated efficiency.
3. Sensitivity to the dominant loss terms is shown (e.g., ±20 % change in drive power).

Until that closed energy balance exists, power and efficiency numbers remain design *targets*, not demonstrated performance.
