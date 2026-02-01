"""
Contamination concentration conversions for water quality and risk assessment.

Supports mg/L ↔ µg/L and mol/L ↔ mg/L (with molecular weight).
"""


def mgL_to_ugL(value: float) -> float:
    """
    Convert concentration from mg/L to µg/L.

    Args:
        value: Concentration in mg/L.

    Returns:
        Concentration in µg/L.
    """
    return value * 1000.0


def ugL_to_mgL(value: float) -> float:
    """
    Convert concentration from µg/L to mg/L.

    Args:
        value: Concentration in µg/L.

    Returns:
        Concentration in mg/L.
    """
    return value / 1000.0


def molL_to_mgL(value: float, mw: float) -> float:
    """
    Convert concentration from mol/L to mg/L using molecular weight.

    mg/L = mol/L * MW * 1000  (MW in g/mol).

    Args:
        value: Concentration in mol/L.
        mw: Molecular weight in g/mol.

    Returns:
        Concentration in mg/L.
    """
    return value * mw * 1000.0


def mgL_to_molL(value: float, mw: float) -> float:
    """
    Convert concentration from mg/L to mol/L using molecular weight.

    mol/L = (mg/L) / (MW * 1000).

    Args:
        value: Concentration in mg/L.
        mw: Molecular weight in g/mol.

    Returns:
        Concentration in mol/L.
    """
    if mw <= 0:
        raise ValueError("Molecular weight must be positive.")
    return value / (mw * 1000.0)
