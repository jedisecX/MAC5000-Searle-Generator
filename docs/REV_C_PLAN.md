# MAC 5000 — Revision C Plan

**Audit & Restructuring Recommendations**  
Source: Green (internal technical review)  
Date: 2026-08-09

---

## Executive Summary

Rev. B mixed two distinct design lineages:

1. **Searl Effect / magnetic roller** experimental generator (original schematics branch)
2. **Liquid-metal MHD** generator using Galinstan + phased fields (main branch evolution)

These are different machines with different physical assumptions. Rev. C must separate them cleanly so each can be evaluated on its own merits.

The MHD path is grounded in established physics. The Searl path is not presently an established energy-generation mechanism and must be treated as a testable hypothesis with proper controls.

---

## Key Findings from the Audit

### 1. Dual Design Problem
- Schematics branch: magnetic rollers, flywheel, motor-assisted startup, Searl-effect claims, 120/240 VAC + 12 VDC
- Main branch: 500 kW liquid-metal MHD, Galinstan, phased toroidal/poloidal coils, pickup coils, power electronics

**Rev. C solution — Modular Core Platform**
```
MAC5000 Core Platform
├── A — Searle / Rotor Experimental Module
├── B — MHD / Liquid-Metal Experimental Module
└── C — Conventional Electromagnetic Reference Generator
```

### 2. Galinstan Temperature Range (Critical Correction)
Rev. B specified **450–650 °C**.

- Galinstan conductivity is excellent (~3–3.5 × 10⁶ S/m)
- Boiling point is high (~1300 °C)
- However, oxidation becomes problematic at elevated temperature. Commercial guidance typically recommends staying near or below ~500 °C.

**Rev. C rule**: Temperature is a **variable experimental parameter**, not a fixed design claim. Actual alloy composition and measured properties must be entered into the model.

### 3. MHD Physics is Legitimate
The underlying interaction is real:

\[
\mathbf{J} = \sigma(\mathbf{E} + \mathbf{v} \times \mathbf{B})
\]

\[
\mathbf{f} = \mathbf{J} \times \mathbf{B}
\]

Galinstan has been used in laboratory MHD research (including Alfvén-wave studies). The phenomenon is not invented. The open question is whether *this specific geometry and energy balance* can support the claimed output.

### 4. 500 kW Claim Requires a Full Energy Audit
For 500 kW electrical output at 95 % efficiency the input must be ~526 kW.  
At 92 % the input must be ~543.5 kW.

Loss budget (~26–44 kW at full power) must explicitly account for:

- Magnetic field drive power
- Coil I²R losses
- Inverter / power electronics losses
- Pump / mechanical losses
- Liquid-metal viscous losses
- Magnetic hysteresis / eddy currents
- Cooling system consumption
- Bearing losses
- Control electronics
- Parasitic currents
- Thermal losses

If the magnetic drive alone consumes a large fraction of that budget, the net generator claim collapses regardless of pickup-coil output.

### 5. Flow Velocity Must Be Derived, Not Asserted
The 48.6 m/s peak velocity figure is useful only when it is the *output* of a calculation chain:

B-field → velocity → conductivity → channel geometry → current density → Lorentz force → mechanical power → electrical extraction

Jumping from “48.6 m/s” to “500 kW” is not engineering.

### 6. Metric Language Must Become Acceptance Criteria
Claims such as:

- MHD stability ≥ 100 %
- Energy efficiency ≥ 98.7 %
- Flow symmetry ≥ 99.4 %

…are not meaningful engineering statements in that form.

Rev. C replaces them with measurable criteria, e.g.:

- Velocity-profile deviation ≤ X %
- Temperature deviation ≤ X K
- Magnetic-field deviation ≤ X %
- Pressure oscillation ≤ X %
- Electrical-output ripple ≤ X %
- Efficiency ≥ experimentally measured threshold

### 7. Searl Component Requires Controlled Experiments
Historical claims exist, but reproducible anomalous energy production has not been established to a high confidence level.

**Required test protocol**:
Measure \( P_{electrical,out} \) against \( P_{mechanical,in} + P_{electrical,in} \) with calibrated instrumentation under these conditions:

1. Rollers installed
2. Rollers removed
3. Magnets demagnetized / reference configuration
4. Different rotational speeds
5. Different magnetic-field strengths
6. Different loads

Only if an anomalous effect survives these controls does the hypothesis become interesting.

---

## Recommended Repository Structure (Rev. C)

```
MAC5000-Searle-Generator/
│
├── README.md                          # Updated modular overview
│
├── docs/
│   ├── system-architecture.md
│   ├── energy-budget.md               # Full loss accounting
│   ├── mhd-model.md                   # First-principles calculation chain
│   ├── seg-hypothesis.md              # Controlled test protocol for Searl
│   ├── test-protocol.md
│   └── REV_C_PLAN.md                  # This document
│
├── schematics/
│   ├── mechanical/
│   ├── magnetic/
│   ├── electrical/
│   ├── mhd/
│   └── instrumentation/
│
├── calculations/
│   ├── coil-design/
│   ├── mhd-flow/
│   ├── thermal/
│   ├── structural/
│   └── energy-balance/
│
├── simulation/
│   ├── electromagnetic/
│   ├── fluid/
│   ├── coupled-mhd/
│   └── system-model/
│
├── experiments/
│   ├── calibration/
│   ├── baseline/
│   ├── seg/
│   └── mhd/
│
├── data/
│   └── README.md
│
└── images/
    ├── MAC5000_RevC_Cutaway.png
    └── MAC5000_RevC_SystemDiagram.png
```

---

## Immediate Next Engineering Step

Build the first-principles model for the MHD module:

1. Start with the existing 1.60 m × 0.85 m geometry
2. Define fluid cross-section
3. Calculate required mass flow from the target velocity
4. Establish realistic B-field values
5. Compute J, Lorentz force density, electrical extraction, and all loss terms
6. Determine what net output the geometry can actually support

- If the math supports ~500 kW → proceed with detailed design
- If it supports ~80 kW → redesign the channel / field
- If it supports multi-MW → that becomes a high-priority investigation

Rev. C is driven by equations and measured quantities, not by unexamined claims.

---

**Status**: Audit complete. Modular separation and energy-audit discipline are now the governing principles for further development.
