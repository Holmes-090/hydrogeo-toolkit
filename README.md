# HydroGeo Mini Toolkit

A command-line utility for environmental and groundwater scientists. It provides unit conversions, Darcy's Law, hydraulic gradient, and contamination concentration calculations in a single, scriptable interface.

**Audience:** Hydrogeologists, environmental consultants, and scientists who need quick, auditable calculations without relying on spreadsheets

---

## Features

- **Unit conversions**
  - Length: ft ↔ m  
  - Flow rate: gpm ↔ L/s  
  - Hydraulic conductivity: m/s ↔ m/day  

- **Darcy's Law** — Volumetric discharge: **Q = K × I × A**  
  (K = hydraulic conductivity, I = hydraulic gradient, A = cross-sectional area)

- **Hydraulic gradient** — **I = Δh / ΔL**  
  (head difference over distance along the flow path)

- **Contamination concentrations**
  - mg/L ↔ µg/L  
  - mol/L ↔ mg/L (with molecular weight in g/mol)

- **Pumping test solvers (Cooper–Jacob straight-line method)**
  - **Transmissivity** — T = (2.3 × Q) / (4π × Δs) from pumping rate and drawdown per log cycle  
  - **Storativity** — S = (2.25 × T × t₀) / r² from T, time intercept t₀, and distance to observation well  

- **Pumping test solvers (Theis analytical solution)**
  - **Theis transient drawdown** — s = (Q/(4πT)) × W(u), u = r²S/(4Tt); computes u and drawdown at time t and radius r  

---

## Installation

Requires **Python 3.7+**. No third-party dependencies; uses the standard library only.

```bash
git clone <repo-url>
cd "HydroGeo Mini Toolkit"
# Optional: create a virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate   # Linux/macOS
```

---

## Quick Start

```bash
python hydrogeo.py --help
```
---

## Using as a Python Library

All calculations can also be imported and used in scripts or notebooks:
```python
from hydrogeo_toolkit.darcy import darcy_flow
from hydrogeo_toolkit.pumping import calculate_transmissivity

q = darcy_flow(K=1e-5, I=0.01, A=10)
T = calculate_transmissivity(Q=0.01, delta_s=0.5)
print(q, T)
```
---

## CLI Examples

**Length conversion (ft → m):**
```bash
python hydrogeo.py convert length --from ft --to m --value 10
# 3.048
```

**Flow rate (gpm → L/s):**
```bash
python hydrogeo.py convert flow --from gpm --to L/s --value 100
```

**Hydraulic conductivity (m/s → m/day):**
```bash
python hydrogeo.py convert conductivity --from m/s --to m/day --value 1e-5
```

**Darcy's Law (Q = K × I × A):**
```bash
python hydrogeo.py darcy --k 1e-5 --i 0.01 --a 10
# 0.001  (e.g. m³/s if K in m/s, A in m²)
```

**Hydraulic gradient (I = Δh / ΔL):**
```bash
python hydrogeo.py gradient --dh 5 --dl 100
# 0.05
```

**Contamination: mol/L → mg/L (e.g. benzene, MW 78.11 g/mol):**
```bash
python hydrogeo.py contam mol2mg --value 0.01 --mw 78.11
# 781.1
```

**Contamination: mg/L → µg/L:**
```bash
python hydrogeo.py contam mg2ug --value 0.5
# 500.0
```

**Pumping test — Transmissivity (Cooper–Jacob):**
```bash
python hydrogeo.py pumping transmissivity --q 0.01 --ds 0.5
# Q in m³/s, Δs in m → T in m²/s
```

**Pumping test — Storativity (Cooper–Jacob):**
```bash
python hydrogeo.py pumping storativity --t 1e-3 --t0 120 --r 10
# T in m²/s, t0 in s, r in m → S dimensionless
```

**Pumping test — Theis transient drawdown:**
```bash
python hydrogeo.py pumping theis --q 0.01 --t 1e-3 --s 1e-4 --r 10 --time 3600
# Output: u value, then drawdown (e.g. m)
```

---

## Project Structure

```
HydroGeo Mini Toolkit/
  hydrogeo_toolkit/
    __init__.py
    conversions.py    # length, flow, conductivity
    darcy.py          # Q = K * I * A
    gradient.py       # I = Δh / ΔL
    contamination.py  # mg/L, µg/L, mol/L
    pumping.py        # Cooper–Jacob and Theis (transmissivity, storativity, drawdown)
    cli.py            # argument parsing and dispatch
  hydrogeo.py         # CLI entry point
  README.md
```

Each calculator lives in its own module so it can be imported and tested independently.

---

## Why This Exists

In environmental consulting and groundwater work, you constantly switch between units (field logs in ft, reports in SI), convert conductivity and flow for pumping tests and modeling, and express contaminant concentrations in mg/L, µg/L, or mol/L for risk and regulatory reporting. Doing this in a spreadsheet or by hand is error-prone and slows down deliverables.

This toolkit gives you a single, auditable place to run those conversions and formulas from the command line or from your own scripts. It is intended as a small, reliable utility—not a demo—so the code stays simple, readable, and correct for use in real projects.

---

## License

MIT License. Free to use, modify, and redistribute with attribution.

---

## Future Extensions

Planned additions may include:
- Additional pumping test methods (e.g. type curves)
- Simple well log visualization
- Additional chemical property lookups
