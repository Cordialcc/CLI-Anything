"""Batch runner for editable draw.io figure rebuilds."""

from __future__ import annotations

import argparse
from pathlib import Path

from .targets import TARGETS


def _resolve_output_path(base_dir: Path, target_name: str, output_dir: Path | None) -> Path:
    target = TARGETS[target_name]
    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir / f"{target['stem']}.drawio"
    return base_dir / target["subdir"] / f"{target['stem']}.drawio"


def run_selected(names, base_dir, output_dir=None):
    base_dir = Path(base_dir)
    output_dir = Path(output_dir) if output_dir is not None else None
    outputs = []
    for name in names:
        if name not in TARGETS:
            raise KeyError(f"Unknown rebuild target: {name}")
        output_path = _resolve_output_path(base_dir, name, output_dir)
        result = TARGETS[name]["builder"](output_path=output_path, base_dir=base_dir)
        outputs.append(str(Path(result["output"])))
    return outputs


def run_all(base_dir, output_dir=None):
    return run_selected(list(TARGETS.keys()), base_dir=base_dir, output_dir=output_dir)


def main():
    parser = argparse.ArgumentParser(description="Generate editable draw.io rebuilds for target figures.")
    parser.add_argument(
        "--base-dir",
        default="/Users/daijidong/Pictures/figures-drawio",
        help="Base directory containing ch3/ and ch4/ figure folders.",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Optional directory for test outputs. If omitted, files are written next to the sources.",
    )
    parser.add_argument("targets", nargs="*", help="Subset of targets to run. Defaults to all.")
    args = parser.parse_args()

    names = args.targets or list(TARGETS.keys())
    outputs = run_selected(names, base_dir=args.base_dir, output_dir=args.output_dir)
    for path in outputs:
        print(path)


if __name__ == "__main__":
    main()
