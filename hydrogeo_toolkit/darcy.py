"""
Darcy's Law calculator for groundwater flow.

Q = K * I * A

Where:
  Q = volumetric discharge (same units as K * I * A)
  K = hydraulic conductivity
  I = hydraulic gradient (dimensionless)
  A = cross-sectional area perpendicular to flow
"""


def darcy_flow(K: float, I: float, A: float) -> float:
    """
    Compute volumetric discharge from Darcy's Law: Q = K * I * A.

    Units of Q match the product of K, I, and A. Use consistent units
    (e.g. K in m/s, A in m² → Q in m³/s; or K in m/day, A in m² → Q in m³/day).

    Args:
        K: Hydraulic conductivity (e.g. m/s or m/day).
        I: Hydraulic gradient (dimensionless, Δh/ΔL).
        A: Cross-sectional area perpendicular to flow (e.g. m²).

    Returns:
        Volumetric discharge Q in the same dimension as K * I * A.
    """
    return K * I * A
