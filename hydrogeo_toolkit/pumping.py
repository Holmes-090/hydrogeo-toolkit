"""
Pumping test analysis using the Cooper–Jacob straight-line approximation.

The Cooper–Jacob method assumes confined conditions and sufficient elapsed time
so that drawdown vs. log(time) is approximately linear. Used for preliminary
estimates of transmissivity and storativity from pumping test data in
environmental consulting and groundwater studies.

References:
  Cooper, H.H. Jr., and Jacob, C.E. (1946). A generalized graphical method for
  evaluating formation constants and summarizing well-field history.
  Transactions, American Geophysical Union, 27(4), 526–534.
"""

import math


def calculate_transmissivity(Q: float, delta_s: float) -> float:
    """
    Compute transmissivity from the Cooper–Jacob straight-line slope.

    In the Cooper–Jacob approximation, drawdown (s) vs. log10(t) is a straight
    line with slope Δs per log cycle. Transmissivity is derived from this slope
    and the pumping rate.

    Formula:
        T = (2.3 * Q) / (4 * π * Δs)

    Where:
        Q   = pumping rate (L³/T), e.g. m³/s or m³/day
        Δs  = drawdown per log cycle (same length units as used in the analysis)

    Args:
        Q: Pumping rate (e.g. m³/s). Must be positive.
        delta_s: Drawdown per log cycle of time (e.g. m). Must be positive.

    Returns:
        Transmissivity T in L²/T (e.g. m²/s), same time dimension as Q.

    Raises:
        ValueError: If Q or delta_s is zero or negative.
    """
    if Q <= 0 or delta_s <= 0:
        raise ValueError("Q and delta_s must be positive.")
    return (2.3 * Q) / (4.0 * math.pi * delta_s)


def calculate_storativity(T: float, t0: float, r: float) -> float:
    """
    Compute storativity from the Cooper–Jacob straight-line time intercept.

    The straight line of drawdown vs. log10(t) extrapolates to zero drawdown
    at time t0. Storativity is derived from t0, transmissivity, and the
    radial distance to the observation well.

    Formula:
        S = (2.25 * T * t0) / r²

    Where:
        T  = transmissivity (L²/T)
        t0 = time at zero drawdown from the straight-line intercept (T)
        r  = radial distance from pumping well to observation well (L)

    Args:
        T: Transmissivity (e.g. m²/s). Must be positive.
        t0: Time intercept at zero drawdown (e.g. seconds or days). Must be positive.
        r: Radial distance to observation well (e.g. m). Must be positive.

    Returns:
        Storativity S (dimensionless).

    Raises:
        ValueError: If T, t0, or r is zero or negative.
    """
    if T <= 0 or t0 <= 0 or r <= 0:
        raise ValueError("T, t0, and r must be positive.")
    return (2.25 * T * t0) / (r * r)
