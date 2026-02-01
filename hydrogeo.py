#!/usr/bin/env python3
"""
HydroGeo Mini Toolkit — CLI entry point.

Run conversions and calculators for groundwater and environmental science.
Example:
  python hydrogeo.py convert length --from ft --to m --value 10
  python hydrogeo.py darcy --k 1e-5 --i 0.01 --a 10
  python hydrogeo.py gradient --dh 5 --dl 100
  python hydrogeo.py contam mol2mg --value 0.01 --mw 78.11
  python hydrogeo.py pumping cooper-jacob transmissivity --q 0.01 --ds 0.5
  python hydrogeo.py pumping cooper-jacob storativity --t 1e-3 --t0 120 --r 10
  python hydrogeo.py pumping theis drawdown --q 0.01 --t 1e-3 --s 1e-4 --r 10 --time 3600
"""

from hydrogeo_toolkit.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
