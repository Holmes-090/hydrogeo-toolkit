"""
HydroGeo Mini Toolkit — utilities for environmental and groundwater science.

Provides unit conversions, Darcy's Law, hydraulic gradient, contamination
concentration calculations, pumping test analysis (Cooper–Jacob, Theis), and slug test analysis
(Hvorslev, Bouwer–Rice) for field and consulting use.
"""

__version__ = "1.0.0"

from hydrogeo_toolkit.conversions import convert_length, convert_flow_rate, convert_conductivity
from hydrogeo_toolkit.darcy import darcy_flow
from hydrogeo_toolkit.gradient import hydraulic_gradient
from hydrogeo_toolkit.contamination import mgL_to_ugL, ugL_to_mgL, molL_to_mgL, mgL_to_molL
from hydrogeo_toolkit.pumping import calculate_transmissivity, calculate_storativity, theis_drawdown
from hydrogeo_toolkit.slug import hvorslev_k, bouwer_rice_k

__all__ = [
    "convert_length",
    "convert_flow_rate",
    "convert_conductivity",
    "darcy_flow",
    "hydraulic_gradient",
    "mgL_to_ugL",
    "ugL_to_mgL",
    "molL_to_mgL",
    "mgL_to_molL",
    "calculate_transmissivity",
    "calculate_storativity",
    "theis_drawdown",
    "hvorslev_k",
    "bouwer_rice_k",
]
