# MHD First-Principles Model — MAC 5000 Module B

## Governing Equations (already in README)

Momentum:
\[
\rho\left(\frac{\partial\mathbf{v}}{\partial t}+\mathbf{v}\cdot\nabla\mathbf{v}\right)
= -\nabla P + \mathbf{J}\times\mathbf{B} + \mu\nabla^{2}\mathbf{v}
\]

Induction:
\[
\frac{\partial\mathbf{B}}{\partial t}
= \nabla\times(\mathbf{v}\times\mathbf{B}) + \frac{1}{\mu_0\sigma}\nabla^{2}\mathbf{B}
\]

Constraints:
\[
\nabla\cdot\mathbf{B}=0,\qquad\nabla\cdot\mathbf{v}=0
\]

Ohm’s law:
\[
\mathbf{J}=\sigma(\mathbf{E}+\mathbf{v}\times\mathbf{B})
\]

## Calculation Chain Required for Rev. C

1. **Geometry**
   - Core outer diameter 1.60 m, height 0.85 m
   - Define exact fluid channel cross-section (radial width × height)
   - Mean path length of the toroidal flow

2. **Material Properties (measured, not assumed)**
   - \(\sigma(T)\) for the actual Galinstan batch
   - Density \(\rho(T)\)
   - Viscosity \(\mu(T)\)
   - Operating temperature range treated as experimental variable (see Galinstan notes)

3. **Magnetic Field**
   - Peak and average \(|\mathbf{B}|\) produced by the drive coils at the fluid
   - Spatial distribution (poloidal + toroidal components)
   - Power required to produce that field (coil current × voltage + losses)

4. **Flow**
   - Target or calculated mean / peak velocity
   - Mass flow rate \(\dot{m}=\rho A v\)
   - Reynolds and magnetic Reynolds numbers

5. **Electromagnetic Interaction**
   - Induced \(\mathbf{E}\) or applied load
   - Current density \(\mathbf{J}\)
   - Lorentz force density \(\mathbf{J}\times\mathbf{B}\)
   - Mechanical power transferred to/from the fluid
   - Electrical power extracted at the pickup coils: \(\int\mathbf{J}\cdot\mathbf{E}\,dV\)

6. **Loss Integration**
   - Viscous dissipation
   - Joule heating in fluid and coils
   - All other terms from the energy-budget document

7. **Net Result**
   - Electrical power available after all losses
   - Sensitivity of that number to B, v, channel aspect ratio, and temperature

Only after this chain is closed does a power claim become an engineering prediction rather than a target.
