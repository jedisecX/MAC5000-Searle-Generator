# MAC 5000 — Modular Experimental Platform

**Rev. C**  
JediSec / QEMIT

> Separate the hypotheses. Measure everything. Let the data decide.

---

## Current Status

This repository previously mixed two distinct concepts:

- An early **Searl-effect / magnetic-roller** experimental generator
- A later **liquid-metal MHD** generator using Galinstan and phased magnetic fields

**Rev. C explicitly separates them.**

```
MAC5000 Core Platform
├── Module A — Searle / Rotor Experimental Path
├── Module B — MHD / Liquid-Metal Experimental Path
└── Module C — Conventional Electromagnetic Reference (future)
```

Each module is evaluated on its own physical assumptions and measured performance.

---

## Module B — MHD / Liquid Metal (Primary Current Focus)

A conducting liquid metal (Galinstan) moving in a magnetic field experiences the classic MHD interaction:

\[
\mathbf{J}=\sigma(\mathbf{E}+\mathbf{v}\times\mathbf{B})
\]
\[
\mathbf{f}=\mathbf{J}\times\mathbf{B}
\]

This physics is real and has laboratory precedent.  
Whether *this particular geometry* can deliver hundreds of kilowatts of **net** electrical power is an open engineering question answered only by a closed energy balance.

### Preliminary Design Envelope (2026-08-09)

A first-principles parameter sweep has been completed. Key findings:

- 500 kW is **not** impossible from electromagnetic power-density considerations.
- The binding constraints are electromagnetic pressure drop, liquid-metal mass flow, and (still unquantified) magnetic-field drive power.
- A *preliminary* operating region exists around **~10 MPa** EM pressure drop → \(B \approx 0.48\) T at 50 m/s → active volume ~5.3 L → mass flow ~339 kg/s.
- Single homogeneous toroidal volume is suboptimal; a **segmented parallel-channel** architecture is recommended.

Full tables, assumptions, and the baseline geometry warning are in:

→ **[docs/design-envelope.md](docs/design-envelope.md)**

### Coil / Magnetic System (in progress)

The idealized ampere-turn requirement at the preliminary point is approximately:

\[
NI \approx 1.93 \times 10^6\ {\rm A\!-\!turns}
\]

Work to quantify real copper loss and true drive power has started:

→ **[docs/coil-design.md](docs/coil-design.md)**  
→ `calculations/coil-design/` (scaffold)

**Important:** Until conductor cross-section, winding topology, temperature, cooling, and excitation mode are specified, \(P_{\rm field}\) remains unknown. Do not treat any current numbers as final.

### Supporting Documents
- [docs/REV_C_PLAN.md](docs/REV_C_PLAN.md) — original audit and restructuring rationale
- [docs/energy-budget.md](docs/energy-budget.md) — required loss categories
- [docs/mhd-model.md](docs/mhd-model.md) — calculation chain
- [docs/seg-hypothesis.md](docs/seg-hypothesis.md) — controlled test protocol for Module A

---

## Module A — Searle / Rotor Path

Treated strictly as a **testable hypothesis**.  
No anomalous energy production is assumed. See the controlled protocol in `docs/seg-hypothesis.md`.

---

## Immediate Engineering Priority

1. **Quantify \(P_{\text{field}}\)** — finish the coil model with real conductor, thermal, and excitation inputs.
2. Close the net-power equation:

\[
P_{\text{net}} = P_{\text{electrical,out}} - (P_{\text{field}} + P_{\text{pump}} + P_{\text{coil}} + P_{\text{cooling}} + P_{\text{electronics}} + \cdots)
\]

3. Explore segmented channel layouts that trade pressure, flow rate, and electrode area more gracefully.

Until \(P_{\text{field}}\) is known, 500 kW remains a target, not a prediction.

---

**Maintained by JediSec / QEMIT**  
https://github.com/jedisecX

*Possibility is interesting. Measurement is mandatory.*
