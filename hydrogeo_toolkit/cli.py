"""
Command-line interface for HydroGeo Mini Toolkit.

Parses subcommands and delegates to the appropriate calculation or conversion.
"""

import argparse
import sys

from hydrogeo_toolkit.conversions import (
    convert_length,
    convert_flow_rate,
    convert_conductivity,
)
from hydrogeo_toolkit.darcy import darcy_flow
from hydrogeo_toolkit.gradient import hydraulic_gradient
from hydrogeo_toolkit.contamination import (
    mgL_to_ugL,
    ugL_to_mgL,
    molL_to_mgL,
    mgL_to_molL,
)


def _cmd_convert(args: argparse.Namespace) -> int:
    """Handle 'convert' subcommand (length, flow, conductivity)."""
    try:
        if args.conversion_type == "length":
            result = convert_length(args.value, args.frm, args.to)
        elif args.conversion_type == "flow":
            result = convert_flow_rate(args.value, args.frm, args.to)
        elif args.conversion_type == "conductivity":
            result = convert_conductivity(args.value, args.frm, args.to)
        else:
            print(f"Unknown conversion type: {args.conversion_type}", file=sys.stderr)
            return 1
        print(result)
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def _cmd_darcy(args: argparse.Namespace) -> int:
    """Handle 'darcy' subcommand: Q = K * I * A."""
    try:
        result = darcy_flow(args.k, args.i, args.a)
        print(result)
        return 0
    except (ValueError, TypeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def _cmd_gradient(args: argparse.Namespace) -> int:
    """Handle 'gradient' subcommand: I = Δh / ΔL."""
    try:
        result = hydraulic_gradient(args.dh, args.dl)
        print(result)
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def _cmd_contam(args: argparse.Namespace) -> int:
    """Handle 'contam' subcommand: mg/L ↔ µg/L, mol/L ↔ mg/L."""
    try:
        if args.contam_op == "mg2ug":
            result = mgL_to_ugL(args.value)
        elif args.contam_op == "ug2mg":
            result = ugL_to_mgL(args.value)
        elif args.contam_op == "mol2mg":
            if args.mw is None:
                print("Error: --mw (molecular weight) required for mol2mg.", file=sys.stderr)
                return 1
            result = molL_to_mgL(args.value, args.mw)
        elif args.contam_op == "mg2mol":
            if args.mw is None:
                print("Error: --mw (molecular weight) required for mg2mol.", file=sys.stderr)
                return 1
            result = mgL_to_molL(args.value, args.mw)
        else:
            print(f"Unknown operation: {args.contam_op}", file=sys.stderr)
            return 1
        print(result)
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def build_parser() -> argparse.ArgumentParser:
    """Build the main CLI argument parser and subparsers."""
    parser = argparse.ArgumentParser(
        prog="hydrogeo",
        description="HydroGeo Mini Toolkit — conversions and calculators for groundwater and environmental science.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Command to run")

    # --- convert ---
    convert_p = subparsers.add_parser("convert", help="Unit conversions (length, flow, conductivity)")
    convert_p.add_argument(
        "conversion_type",
        choices=["length", "flow", "conductivity"],
        help="Type of conversion",
    )
    convert_p.add_argument("--from", dest="frm", required=True, help="Source unit (e.g. ft, m, gpm, m/s)")
    convert_p.add_argument("--to", dest="to", required=True, help="Target unit (e.g. m, ft, L/s, m/day)")
    convert_p.add_argument("--value", type=float, required=True, help="Numeric value to convert")
    convert_p.set_defaults(func=_cmd_convert)

    # --- darcy ---
    darcy_p = subparsers.add_parser("darcy", help="Darcy's Law: Q = K * I * A")
    darcy_p.add_argument("--k", type=float, required=True, help="Hydraulic conductivity (e.g. m/s)")
    darcy_p.add_argument("--i", type=float, required=True, help="Hydraulic gradient (dimensionless)")
    darcy_p.add_argument("--a", type=float, required=True, help="Cross-sectional area (e.g. m²)")
    darcy_p.set_defaults(func=_cmd_darcy)

    # --- gradient ---
    grad_p = subparsers.add_parser("gradient", help="Hydraulic gradient: I = Δh / ΔL")
    grad_p.add_argument("--dh", type=float, required=True, help="Head difference (e.g. m)")
    grad_p.add_argument("--dl", type=float, required=True, help="Distance along flow path (e.g. m)")
    grad_p.set_defaults(func=_cmd_gradient)

    # --- contam ---
    contam_p = subparsers.add_parser("contam", help="Contamination concentration conversions")
    contam_p.add_argument(
        "contam_op",
        choices=["mg2ug", "ug2mg", "mol2mg", "mg2mol"],
        help="Conversion: mg2ug, ug2mg, mol2mg, mg2mol",
    )
    contam_p.add_argument("--value", type=float, required=True, help="Concentration value")
    contam_p.add_argument("--mw", type=float, default=None, help="Molecular weight (g/mol); required for mol2mg and mg2mol")
    contam_p.set_defaults(func=_cmd_contam)

    return parser


def main() -> int:
    """Entry point: parse args and run the selected command."""
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
