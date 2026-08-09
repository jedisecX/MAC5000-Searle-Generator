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
Whether *this particular geometry* can deliver hundreds of kilowatts of net electrical power is an open engineering question that must be answered by a closed energy balance and first-principles calculation (see `docs/`).

### Important Corrections from Rev. B Audit
- Operating temperature is now a **variable experimental parameter**, not a fixed 450–650 °C claim.
- Power and efficiency numbers are **design targets** until a full loss accounting exists.
- Metrics such as “stability ≥ 100 %” have been replaced by measurable acceptance criteria.

See:
- [docs/REV_C_PLAN.md](docs/REV_C_PLAN.md) — full audit and restructuring rationale
- [docs/energy-budget.md](docs/energy-budget.md) — required loss categories
- [docs/mhd-model.md](docs/mhd-model.md) — calculation chain that must be closed

---

## Module A — Searle / Rotor Path

Treated strictly as a **testable hypothesis**.

No anomalous energy production is assumed.  
A controlled experimental protocol is defined in [docs/seg-hypothesis.md](docs/seg-hypothesis.md).

Only if calibrated measurements show net electrical output exceeding total input *under multiple control conditions* does the hypothesis advance.

---

## Repository Structure (Rev. C Target)

```
├── README.md
├── docs/
│   ├── REV_C_PLAN.md
│   ├── energy-budget.md
│   ├── mhd-model.md
│   ├── seg-hypothesis.md
│   └── ...
├── schematics/
├── calculations/
├── simulation/
├── experiments/
├── data/
└── images/
```

---

## Immediate Engineering Priority

Close the first-principles MHD model for the existing 1.60 m × 0.85 m geometry:

1. Define fluid channel cross-section
2. Establish realistic B-field and the power required to produce it
3. Calculate mass flow, current density, Lorentz force, and electrical extraction
4. Sum every loss term
5. Report the net electrical power the geometry can actually support

The result of that calculation — not marketing language — will determine the next design iteration.

---

**Maintained by JediSec / QEMIT**  
https://github.com/jedisecX

*Possibility is interesting. Measurement is mandatory.*
