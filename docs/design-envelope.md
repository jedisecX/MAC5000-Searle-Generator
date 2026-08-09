# MAC 5000 Rev. C — Preliminary MHD Design Envelope

**First-principles parameter sweep**  
Source: Green (2026-08-09)

---

## Model Assumptions (explicit)

| Parameter              | Value                          | Notes |
|------------------------|--------------------------------|-------|
| Flow path length       | 5.0265 m (π × 1.60 m)         | Mean toroidal path |
| Galinstan conductivity | 3.46 × 10⁶ S/m                | Assumed; must be measured for actual alloy + T |
| Density                | 6 440 kg/m³                   | Assumed |
| Viscosity              | 2.4 mPa·s                     | Assumed |
| Target \(P_{out}\)     | 500 kW                        | Design target |
| Target conversion η    | 95 %                          | Idealized MHD conversion efficiency |
| Sweep ranges           | \(B = 0.05\)–\(1.0\) T<br>\(v = 10\)–\(50\) m/s | |

Material properties remain assumptions until the actual alloy composition and operating temperature are fixed.

---

## Key Result: Power Density vs Pressure

At the high end of the sweep (\(B = 1.0\) T, \(v = 50\) m/s):

- Ideal electrical power density ≈ **411 MW/m³**
- Active MHD volume for 500 kW ≈ **0.00122 m³** (1.22 L)
- Equivalent channel area over 5.03 m path ≈ **2.42 cm²**
- Mass flow ≈ **78 kg/s**
- Electromagnetic pressure drop ≈ **43.5 MPa**
- Magnetic Reynolds number \(Rm\) ≈ **21.7**

**Conclusion**: 500 kW is *not* impossible from pure electromagnetic power-density considerations. The limiting factor is the associated electromagnetic pressure (and everything required to contain and circulate against it).

---

## Constrained Design Envelope

Limiting electromagnetic pressure drop produces a clear trade-off surface:

| Max EM ΔP | \(B\) @ 50 m/s | Active Volume | Channel Area* | Mass Flow |
|-----------|----------------|---------------|---------------|-----------|
| 5 MPa     | 0.339 T        | 10.6 L        | 21.1 cm²      | 678 kg/s  |
| 10 MPa    | 0.480 T        | 5.29 L        | 10.5 cm²      | 339 kg/s  |
| 20 MPa    | 0.678 T        | 2.65 L        | 5.26 cm²      | 169 kg/s  |
| 50 MPa    | 1.07 T         | 1.06 L        | 2.11 cm²      | 67.8 kg/s |
| 100 MPa   | 1.52 T         | 0.529 L       | 1.05 cm²      | 33.9 kg/s |

\*Equivalent active cross-sectional area over the assumed 5.03 m path.

**Design insight**:  
Higher \(B\) → smaller machine / lower mass flow → dramatically higher pressure.  
Lower \(B\) → larger active volume / much higher mass flow → lower pressure.  

There is no single “easy” point. Every design point is a compromise among magnetic field generation, pressure containment, circulation power, and heat rejection.

---

## Baseline Geometry Warning (100 mm × 100 mm channel)

When the original schematic envelope is populated with a naïve 0.10 m × 0.10 m channel at 48.6 m/s and 1 T:

- Mass flow ≈ **3 130 kg/s** (extreme)
- \(Re \approx 1.3 \times 10^7\) (highly turbulent)
- \(Rm \approx 21\) (magnetic advection significant; frozen-in effects matter)
- \(Ha \approx 47\) (strong magnetic influence on the flow)
- Ideal matched-load power density ≈ 2.04 GW/m³ → only ~245 cm³ of active volume theoretically needed for 500 kW
- Corresponding EM pressure drop over the path ≈ **423 MPa** (structurally prohibitive)

This demonstrates that the original 1.60 m × 0.85 m outer envelope is **not** the limiting factor. The channel geometry, field strength, and pressure containment are.

---

## Frequency Consistency Note

The schematic cites a “heartbeat” frequency of 7.83 Hz.  
For a 1.60 m mean diameter:

\[
f = \frac{v}{\pi D}
\]

- At 48.6 m/s → \(f \approx 9.67\) Hz  
- At 7.83 Hz → \(v \approx 39.4\) m/s  

Rev. C must explicitly decide whether 7.83 Hz is an electromagnetic excitation / oscillation frequency independent of the bulk flow velocity, or correct one of the two values.

---

## Architectural Recommendation

Abandon the single homogeneous toroidal volume.

Adopt a **segmented parallel-channel MHD architecture**:

```
          MAGNETIC FIELD
               ↓↓↓
     ┌────────────────────┐
     │   MHD CHANNEL A    │ →→→ liquid metal
     ├────────────────────┤
     │   MHD CHANNEL B    │ →→→ liquid metal
     ├────────────────────┤
     │   MHD CHANNEL C    │ →→→ liquid metal
     └────────────────────┘
               ↓
           COLLECTOR → DC LINK
```

Benefits:
- Independent trade of velocity ↔ flow rate ↔ pressure ↔ electrode area ↔ local \(B\)
- Individual channel instrumentation and control
- Far more experimentally useful than a single extreme channel

---

## System-Level Reality Check

At 95 % conversion efficiency the electromagnetic stage itself requires:

\[
P_{\text{mechanical}} \approx 526.3\,\text{kW}
\]

to deliver 500 kW electrical, i.e. ~26.3 kW of conversion loss inside the MHD interaction.

The **net** system output remains:

\[
P_{\text{net}} = 500\,\text{kW} - \bigl(P_{\text{field}} + P_{\text{pump}} + P_{\text{coil}} + P_{\text{cooling}} + P_{\text{electronics}} + \cdots\bigr)
\]

\(P_{\text{field}}\) (power to establish and sustain the magnetic field) is still unquantified and is the single largest open term.

---

## Immediate Next Calculation Priority

Design the actual coil / magnetic system for the 1.60 m geometry:

\[
N,\ I,\ R,\ L,\ B,\ P_{\text{copper}},\ P_{\text{core}},\ P_{\text{drive}}
\]

Once \(P_{\text{field}}\) is known, it can be combined with the design envelope above to produce the first credible net-power prediction.
