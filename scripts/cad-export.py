#!/usr/bin/env python3
"""
Headless runner for pure build123d scripts.
Executes the script and exports found geometry to STEP (and optionally STL).

Usage:
  python scripts/cad-export.py path/to/model.py
  python scripts/cad-export.py path/to/model.py --stl
  python scripts/cad-export.py path/to/model.py -o out/dir
"""

from __future__ import annotations

import argparse
import inspect
import runpy
import sys
from contextlib import suppress
from pathlib import Path
from typing import Any


def is_cad_object(obj: Any) -> bool:
    """Heuristic: build123d / OCP-like geometry objects."""
    if obj is None:
        return False
    if inspect.isclass(obj) or inspect.isroutine(obj) or inspect.ismodule(obj):
        return False
    return (
        hasattr(obj, "wrapped")
        or hasattr(obj, "part")
        or hasattr(obj, "sketch")
        or hasattr(obj, "solid")
    )


def unwrap(obj: Any) -> Any:
    """Prefer the actual solid/part when a builder context is returned."""
    if hasattr(obj, "part") and obj.part is not None:
        return obj.part
    if hasattr(obj, "solid") and callable(obj.solid):
        with suppress(AttributeError, TypeError, ValueError, RuntimeError):
            return obj.solid()
    return obj


def collect_cad_objects(namespace: dict) -> list[Any]:
    objects = []
    for name, val in namespace.items():
        if name.startswith("_"):
            continue
        if is_cad_object(val):
            objects.append(unwrap(val))
    return objects


def export_objects(objects: list[Any], out_base: Path, do_stl: bool) -> None:
    from build123d import Compound, export_step, export_stl

    if not objects:
        print("No CAD objects found to export.")
        sys.exit(1)

    # One object → direct export; several → Compound
    if len(objects) == 1:
        shape = objects[0]
    else:
        shape = Compound(children=objects)

    step_path = out_base.with_suffix(".step")
    export_step(shape, step_path)
    print(f"STEP written: {step_path}")

    if do_stl:
        stl_path = out_base.with_suffix(".stl")
        export_stl(shape, stl_path)
        print(f"STL written:  {stl_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export build123d script to STEP/STL")
    parser.add_argument("script", type=Path, help="Path to pure build123d .py script")
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=None,
        help="Directory for output files (default: same as script)",
    )
    parser.add_argument(
        "--stl",
        action="store_true",
        help="Also export STL",
    )
    args = parser.parse_args()

    script_path = args.script.resolve()
    if not script_path.exists():
        print(f"File not found: {script_path}")
        sys.exit(1)

    # Run the pure model script
    namespace = runpy.run_path(str(script_path), run_name="__main__")
    objects = collect_cad_objects(namespace)

    out_dir = args.output_dir.resolve() if args.output_dir else script_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    out_base = out_dir / script_path.stem

    export_objects(objects, out_base, do_stl=args.stl)


if __name__ == "__main__":
    main()
