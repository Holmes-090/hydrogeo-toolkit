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
from hydrogeo_toolkit.pumping import (
    calculate_transmissivity,
    calculate_storativity,
    theis_drawdown,
)
from hydrogeo_toolkit.slug import hvorslev_k, bouwer_rice_k


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


def _cmd_pumping(args: argparse.Namespace) -> int:
    """Handle 'pumping <method> <calculation>' subcommands."""
    try:
        if args.method == "cooper-jacob":
            if args.calculation == "transmissivity":
                result = calculate_transmissivity(args.q, args.ds)
                print(result)
            elif args.calculation == "storativity":
                result = calculate_storativity(args.t, args.t0, args.r)
                print(result)
            else:
                print(f"Unknown Cooper–Jacob calculation: {args.calculation}", file=sys.stderr)
                return 1
        elif args.method == "theis":
            if args.calculation == "drawdown":
                drawdown, u_val = theis_drawdown(args.q, args.t, args.s, args.r, args.time)
                print(f"u={u_val}")
                print(drawdown)
            else:
                print(f"Unknown Theis calculation: {args.calculation}", file=sys.stderr)
                return 1
        else:
            print(f"Unknown pumping method: {args.method}", file=sys.stderr)
            return 1
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def _cmd_slug(args: argparse.Namespace) -> int:
    """Handle 'slug' subcommand: Hvorslev or Bouwer-Rice hydraulic conductivity."""
    try:
        if args.slug_method == "hvorslev":
            print("Method: Hvorslev")
            print(f"  r={args.r}, L={args.l}, t37={args.t37}")
            K = hvorslev_k(args.r, args.l, args.t37)
        elif args.slug_method == "bouwer-rice":
            print("Method: Bouwer-Rice")
            print(f"  rw={args.rw}, re={args.re}, L={args.l}, t37={args.t37}")
            K = bouwer_rice_k(args.rw, args.re, args.l, args.t37)
        else:
            print(f"Unknown slug method: {args.slug_method}", file=sys.stderr)
            return 1
        print(f"K = {K}")
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

    # --- pumping: method → calculation (nested subcommands) ---
    pumping_p = subparsers.add_parser(
        "pumping",
        help="Pumping test analysis. Use: pumping <method> <calculation> [options]",
        description="Pumping test analysis by method. Methods: cooper-jacob (transmissivity, storativity), theis (drawdown).",
    )
    pumping_sub = pumping_p.add_subparsers(dest="method", required=True, help="Analysis method")

    # Cooper–Jacob: transmissivity | storativity
    cj_p = pumping_sub.add_parser(
        "cooper-jacob",
        help="Cooper–Jacob straight-line method",
        description="Cooper–Jacob straight-line approximation. Calculations: transmissivity, storativity.",
    )
    cj_sub = cj_p.add_subparsers(dest="calculation", required=True, help="Quantity to calculate")
    cj_trans = cj_sub.add_parser("transmissivity", help="T = (2.3*Q) / (4*pi*ds)")
    cj_trans.add_argument("--q", type=float, required=True, help="Pumping rate (L³/T)")
    cj_trans.add_argument("--ds", type=float, required=True, help="Drawdown per log cycle")
    cj_trans.set_defaults(func=_cmd_pumping, method="cooper-jacob", calculation="transmissivity")
    cj_stor = cj_sub.add_parser("storativity", help="S = (2.25*T*t0) / r^2")
    cj_stor.add_argument("--t", type=float, required=True, help="Transmissivity (L²/T)")
    cj_stor.add_argument("--t0", type=float, required=True, help="Time at zero drawdown (intercept)")
    cj_stor.add_argument("--r", type=float, required=True, help="Radial distance to observation well")
    cj_stor.set_defaults(func=_cmd_pumping, method="cooper-jacob", calculation="storativity")

    # Theis: drawdown
    theis_p = pumping_sub.add_parser(
        "theis",
        help="Theis analytical solution",
        description="Theis transient drawdown. Calculation: drawdown.",
    )
    theis_sub = theis_p.add_subparsers(dest="calculation", required=True, help="Quantity to calculate")
    theis_dd = theis_sub.add_parser("drawdown", help="s = (Q/(4*pi*T))*W(u), u = r^2*S/(4*T*t)")
    theis_dd.add_argument("--q", type=float, required=True, help="Pumping rate (L³/T)")
    theis_dd.add_argument("--t", type=float, required=True, help="Transmissivity (L²/T)")
    theis_dd.add_argument("--s", type=float, required=True, help="Storativity (dimensionless)")
    theis_dd.add_argument("--r", type=float, required=True, help="Radial distance to observation well")
    theis_dd.add_argument("--time", type=float, required=True, help="Time since pumping started (T)")
    theis_dd.set_defaults(func=_cmd_pumping, method="theis", calculation="drawdown")

    # --- slug (Hvorslev, Bouwer-Rice) ---
    slug_p = subparsers.add_parser(
        "slug",
        help="Slug test analysis for hydraulic conductivity",
        description="Slug test estimators: Hvorslev, Bouwer-Rice. Output: method, inputs, K.",
    )
    slug_sub = slug_p.add_subparsers(dest="slug_method", required=True, help="Slug test method")
    slug_hv = slug_sub.add_parser("hvorslev", help="Hvorslev: K = (r^2*ln(L/r)) / (2*L*t37)")
    slug_hv.add_argument("--r", type=float, required=True, help="Well radius (L)")
    slug_hv.add_argument("--l", type=float, required=True, help="Length of screened interval (L)")
    slug_hv.add_argument("--t37", type=float, required=True, help="Time to 37%% recovery (T)")
    slug_hv.set_defaults(func=_cmd_slug, slug_method="hvorslev")
    slug_br = slug_sub.add_parser("bouwer-rice", help="Bouwer-Rice: K = (rw^2*ln(re/rw)) / (2*L*t37)")
    slug_br.add_argument("--rw", type=float, required=True, help="Well radius (L)")
    slug_br.add_argument("--re", type=float, required=True, help="Effective radius of influence (L)")
    slug_br.add_argument("--l", type=float, required=True, help="Screen length (L)")
    slug_br.add_argument("--t37", type=float, required=True, help="Time to 37%% recovery (T)")
    slug_br.set_defaults(func=_cmd_slug, slug_method="bouwer-rice")

    return parser


def main() -> int:
    """Entry point: parse args and run the selected command."""
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
