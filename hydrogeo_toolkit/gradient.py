"""
Hydraulic gradient calculator.

I = Δh / ΔL

Where:
  I = hydraulic gradient (dimensionless)
  Δh = head difference (e.g. m or ft)
  ΔL = distance along flow path (same length units as Δh)
"""


def hydraulic_gradient(dh: float, dL: float) -> float:
    """
    Compute hydraulic gradient I = Δh / ΔL.

    Units of dh and dL must match; I is dimensionless.

    Args:
        dh: Head difference (e.g. metres or feet).
        dL: Distance along the flow path (same units as dh).

    Returns:
        Hydraulic gradient I (dimensionless).

    Raises:
        ValueError: If dL is zero.
    """
    if dL == 0:
        raise ValueError("ΔL (distance) must be non-zero.")
    return dh / dL
