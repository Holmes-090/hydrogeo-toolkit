"""
Unit conversions for hydrogeology: length, flow rate, hydraulic conductivity.

All conversion factors follow standard SI/US customary definitions used in
environmental and groundwater practice.
"""

# Length: 1 ft = 0.3048 m (exact)
FT_TO_M = 0.3048

# Flow rate: 1 US gpm = 0.0630901964 L/s (exact conversion)
GPM_TO_L_PER_S = 0.0630901964

# Hydraulic conductivity: 1 m/s = 86400 m/day
M_PER_S_TO_M_PER_DAY = 86400.0


def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert length between feet (ft) and metres (m).

    Args:
        value: Numeric length value.
        from_unit: Source unit: "ft" or "m".
        to_unit: Target unit: "ft" or "m".

    Returns:
        Length in the target unit.

    Raises:
        ValueError: If from_unit or to_unit is not "ft" or "m".
    """
    from_unit = from_unit.lower().strip()
    to_unit = to_unit.lower().strip()
    if from_unit not in ("ft", "m") or to_unit not in ("ft", "m"):
        raise ValueError('Length units must be "ft" or "m".')
    if from_unit == to_unit:
        return value
    if from_unit == "ft" and to_unit == "m":
        return value * FT_TO_M
    return value / FT_TO_M


def convert_flow_rate(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert volumetric flow rate between US gpm and L/s.

    Args:
        value: Numeric flow rate.
        from_unit: Source unit: "gpm" or "L/s" (or "L/s", "l/s").
        to_unit: Target unit: "gpm" or "L/s".

    Returns:
        Flow rate in the target unit.

    Raises:
        ValueError: If from_unit or to_unit is not "gpm" or "L/s".
    """
    from_unit = from_unit.lower().strip().replace(" ", "")
    to_unit = to_unit.lower().strip().replace(" ", "")
    # Normalize L/s variants (e.g. "l/s", "ls")
    if from_unit in ("l/s", "ls"):
        from_unit = "l/s"
    if to_unit in ("l/s", "ls"):
        to_unit = "l/s"
    if from_unit not in ("gpm", "l/s") or to_unit not in ("gpm", "l/s"):
        raise ValueError('Flow rate units must be "gpm" or "L/s".')
    if from_unit == to_unit:
        return value
    if from_unit == "gpm" and to_unit == "l/s":
        return value * GPM_TO_L_PER_S
    return value / GPM_TO_L_PER_S


def convert_conductivity(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert hydraulic conductivity between m/s and m/day.

    Args:
        value: Numeric hydraulic conductivity.
        from_unit: Source unit: "m/s" or "m/day".
        to_unit: Target unit: "m/s" or "m/day".

    Returns:
        Hydraulic conductivity in the target unit.

    Raises:
        ValueError: If from_unit or to_unit is not "m/s" or "m/day".
    """
    from_unit = from_unit.lower().strip().replace(" ", "")
    to_unit = to_unit.lower().strip().replace(" ", "")
    if from_unit not in ("m/s", "m/day") or to_unit not in ("m/s", "m/day"):
        raise ValueError('Conductivity units must be "m/s" or "m/day".')
    if from_unit == to_unit:
        return value
    if from_unit == "m/s" and to_unit == "m/day":
        return value * M_PER_S_TO_M_PER_DAY
    return value / M_PER_S_TO_M_PER_DAY
