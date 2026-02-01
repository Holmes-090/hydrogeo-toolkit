"""
Pumping test analysis: Cooper–Jacob straight-line and Theis solutions.

The Cooper–Jacob method assumes confined conditions and sufficient elapsed time
so that drawdown vs. log(time) is approximately linear. Used for preliminary
estimates of transmissivity and storativity from pumping test data.

The Theis solution models transient radial flow to a well in a confined aquifer;
drawdown is given by the well function W(u) = -Ei(-u), where u = r²S/(4Tt).

References:
  Cooper, H.H. Jr., and Jacob, C.E. (1946). A generalized graphical method for
  evaluating formation constants and summarizing well-field history.
  Transactions, American Geophysical Union, 27(4), 526–534.
  Theis, C.V. (1935). The relation between the lowering of the piezometric
  surface and the rate and duration of discharge of a well using groundwater
  storage. Transactions, American Geophysical Union, 16(2), 519–524.
"""

import math
from typing import Tuple

# Euler–Mascheroni constant γ, used in the well function W(u) = -Ei(-u)
_EULER_GAMMA = 0.5772156649015328606065120900824024310421593359399235988057672348849


def _well_function_small_u(u: float, max_terms: int = 80) -> float:
    """
    Well function W(u) = -Ei(-u) for small u, using series expansion.

    W(u) = -γ - ln(u) + u - u²/(2·2!) + u³/(3·3!) - ...
    Converges for all u > 0; use for u ≤ 1.
    """
    if u <= 0:
        raise ValueError("u must be positive.")
    term = u
    factorial_k = 1  # k!
    w = -_EULER_GAMMA - math.log(u) + u
    for k in range(2, max_terms + 1):
        factorial_k *= k
        term *= u
        coeff = ((-1) ** (k + 1)) / (k * factorial_k)
        w += coeff * term
        if abs(coeff * term) <= 1e-15 * abs(w):
            break
    return w


def _well_function_large_u(u: float, max_terms: int = 30) -> float:
    """
    Well function W(u) = -Ei(-u) for large u, using asymptotic expansion.

    W(u) ≈ e^(-u) / u * (1 - 1/u + 2!/u² - 3!/u³ + ...)
    Series is divergent; we stop when terms start increasing in magnitude.
    """
    if u <= 0:
        raise ValueError("u must be positive.")
    factor = math.exp(-u) / u
    inv_u = 1.0 / u
    w = 1.0
    factorial_n = 1
    prev_abs_term = 1.0
    for n in range(1, max_terms + 1):
        factorial_n *= n
        term = ((-1) ** n) * factorial_n * (inv_u ** n)
        abs_term = abs(term)
        if abs_term > prev_abs_term:
            break
        w += term
        prev_abs_term = abs_term
        if abs_term <= 1e-15 * abs(w):
            break
    return factor * w


def _well_function(u: float) -> float:
    """
    Well function W(u) = -Ei(-u), the exponential integral.

    Uses series expansion for u ≤ 2 and asymptotic expansion for u > 2,
    where the asymptotic series behaves well. Standard library only (math).
    """
    if u <= 0:
        raise ValueError("u must be positive.")
    if u <= 2.0:
        return _well_function_small_u(u)
    return _well_function_large_u(u)


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


def theis_drawdown(Q: float, T: float, S: float, r: float, t: float) -> Tuple[float, float]:
    """
    Calculate drawdown using the Theis solution for transient radial flow.

    In a confined aquifer with instantaneous pumping start, drawdown at
    distance r and time t is s = (Q / (4πT)) * W(u), where u = r²S/(4Tt)
    and W(u) is the well function (exponential integral -Ei(-u)).

    Formula:
        s = (Q / (4 * π * T)) * W(u)
        u = (r² * S) / (4 * T * t)

    Where:
        Q = pumping rate (L³/T)
        T = transmissivity (L²/T)
        S = storativity (dimensionless)
        r = radial distance to observation point (L)
        t = time since pumping started (T)

    Args:
        Q: Pumping rate (e.g. m³/s). Must be positive.
        T: Transmissivity (e.g. m²/s). Must be positive.
        S: Storativity (dimensionless). Must be positive.
        r: Radial distance to observation well (e.g. m). Must be positive.
        t: Time since pumping started (e.g. seconds). Must be positive.

    Returns:
        Tuple (drawdown, u): drawdown in length units (e.g. m), and the
        dimensionless argument u for transparency.

    Raises:
        ValueError: If any input is zero or negative.
    """
    if Q <= 0 or T <= 0 or S <= 0 or r <= 0 or t <= 0:
        raise ValueError("Q, T, S, r, and t must be positive.")
    u = (r * r * S) / (4.0 * T * t)
    w_u = _well_function(u)
    s = (Q / (4.0 * math.pi * T)) * w_u
    return (s, u)
