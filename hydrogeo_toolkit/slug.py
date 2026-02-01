"""
Slug test analysis for hydraulic conductivity estimation.

Slug tests involve instantaneously displacing water in a well (e.g. with a slug)
and measuring head recovery over time. Used for first-pass estimates of
hydraulic conductivity in environmental and groundwater studies without
pumping equipment.

References:
  Hvorslev, M.J. (1951). Time lag and soil permeability in groundwater
  observations. U.S. Army Corps of Engineers Waterways Experiment Station,
  Bulletin 36.
  Bouwer, H., and Rice, R.C. (1976). A slug test for determining hydraulic
  conductivity of unconfined aquifers with completely or partially penetrating
  wells. Water Resources Research, 12(3), 423–428.
"""

import math


def hvorslev_k(r: float, L: float, t37: float) -> float:
    """
    Calculate hydraulic conductivity using the Hvorslev method.

    The Hvorslev method relates the time for head to recover to 37% of the
    initial displacement to hydraulic conductivity, assuming a confined
    or semi-confined response and a fully penetrating well screen.

    Formula:
        K = (r^2 * ln(L / r)) / (2 * L * t37)

    Where:
        r   = well radius (L)
        L   = length of screened interval (L)
        t37 = time for head to dissipate to 37% of initial displacement (T)

    Args:
        r: Well radius (e.g. m). Must be positive.
        L: Length of screened interval (e.g. m). Must be positive and > r.
        t37: Time to 37% recovery (e.g. seconds). Must be positive.

    Returns:
        Hydraulic conductivity K in L/T (e.g. m/s), same time dimension as 1/t37.

    Raises:
        ValueError: If r, L, or t37 is zero or negative, or if L <= r.
    """
    if r <= 0 or L <= 0 or t37 <= 0:
        raise ValueError("r, L, and t37 must be positive.")
    if L <= r:
        raise ValueError("L must be greater than r for ln(L/r) to be positive.")
    return (r * r * math.log(L / r)) / (2.0 * L * t37)


def bouwer_rice_k(rw: float, re: float, L: float, t37: float) -> float:
    """
    Calculate hydraulic conductivity using the Bouwer–Rice method.

    The Bouwer–Rice method extends slug-test analysis to unconfined aquifers
    and partially penetrating wells by using an effective radius of influence
    (re) that accounts for geometry. Head recovery to 37% is used.

    Formula:
        K = (rw^2 * ln(re / rw)) / (2 * L * t37)

    Where:
        rw  = well radius (L)
        re  = effective radius of influence (L)
        L   = screen length (L)
        t37 = time for 37% recovery (T)

    Args:
        rw: Well radius (e.g. m). Must be positive.
        re: Effective radius of influence (e.g. m). Must be positive and > rw.
        L: Screen length (e.g. m). Must be positive.
        t37: Time to 37% recovery (e.g. seconds). Must be positive.

    Returns:
        Hydraulic conductivity K in L/T (e.g. m/s), same time dimension as 1/t37.

    Raises:
        ValueError: If rw, re, L, or t37 is zero or negative, or if re <= rw.
    """
    if rw <= 0 or re <= 0 or L <= 0 or t37 <= 0:
        raise ValueError("rw, re, L, and t37 must be positive.")
    if re <= rw:
        raise ValueError("re must be greater than rw for ln(re/rw) to be positive.")
    return (rw * rw * math.log(re / rw)) / (2.0 * L * t37)
