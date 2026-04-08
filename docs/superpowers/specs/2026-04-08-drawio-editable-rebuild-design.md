# Draw.io Editable Rebuild Design

**Date:** 2026-04-08

## Goal

Use the local `drawio` CLI harness to convert selected figure assets under `/Users/daijidong/Pictures/figures-drawio` into truly editable `.drawio` diagrams. The output must be built from draw.io vertices, edges, labels, and styles rather than screenshots, raster images, or full-figure embeds. All text must default to Songti (`Songti SC` on macOS).

## Scope

### Included targets

- `ch3/obb_cn.pdf`
- `ch3/pgdg_tol_cn.pdf`
- `ch3/pipeline_tol_cn.pdf`
- `ch3/sre_cn.pdf`
- `ch3/teaser_tol_cn.pdf`
- `ch4/fig1_teaser.{pdf,tex}`
- `ch4/fig2_architecture.{pdf,tex}`
- `ch4/fig3_backprojection_h.{pdf,tex}`
- `ch4/fig4_waterfall.{pdf,tex}`
- `ch4/fig6_perturbation.{pdf,tex}`
- `ch4/fig7_selectivity.{pdf,tex}`
- `ch4/fig8_params.{pdf,tex}`
- `ch4/fig9_gate_gradient.{pdf,tex}`

### Excluded targets

- Any figure that already has a Python source version.
- Personal non-figure PDFs under `/Users/daijidong/Pictures`.
- Any screenshot-based or image-embedded reconstruction approach.

## Constraints

- Every delivered `.drawio` file must remain editable in draw.io.
- Text must be stored as draw.io text and rendered with Songti styling.
- PDF-only figures may be rebuilt manually, but still as draw.io primitives.
- TikZ-backed figures should reuse the source `.tex` where practical.
- The implementation should live in the existing `CLI-Anything/drawio` harness so future rebuilds can reuse it.

## Chosen approach

Use a hybrid rebuild pipeline:

1. Add reusable rebuild primitives to the draw.io harness.
2. For `pdf+tex` figures, create small source-specific rebuild scripts that translate known TikZ structures into draw.io nodes, edges, labels, and styling.
3. For `pdf-only` figures, define explicit figure specifications in Python and generate the output from those specs.
4. Centralize font defaults and common visual helpers so every generated diagram uses Songti consistently.

This avoids the instability of PDF vector reverse-engineering while preserving editability.

## Architecture

### Rebuild primitives

Add helper functions that can:

- create pages with explicit page sizes
- add styled boxes, circles, diamonds, and text nodes
- add styled connectors, dashed guides, and labeled arrows
- apply consistent font, spacing, stroke, and color defaults

These helpers should be thin wrappers over the existing XML/session utilities.

### Figure generators

Add a rebuild module that exposes one callable per target figure. Each callable should:

- open a fresh draw.io session
- place shapes and text using reusable primitives
- save to a deterministic `.drawio` output path

For `ch4` TikZ figures, the generators may parse a constrained subset of the original `.tex` or directly encode the reconstructed layout from the `.tex` source. The important requirement is that the resulting file is editable, not that the parser is fully generic.

For `ch3` PDF-only figures, each generator should be a manual reconstruction script with explicit positions and labels.

### Batch entry point

Provide a command-line entry point or script that:

- enumerates the approved target set
- skips Python-backed figures
- rebuilds the selected diagrams
- reports the generated `.drawio` paths

## Output locations

Generated files should live next to the source figures:

- `ch3/<name>.drawio`
- `ch4/<name>.drawio`

## Font strategy

Set a default text style for all generated shapes and labels:

- `fontFamily=Songti SC`
- preserve diagram-specific font size when needed
- black text unless the original figure clearly uses colored labels

If a shape preset does not already carry font metadata, the rebuild layer must inject it.

## Testing strategy

### Unit tests

- verify default Songti font style is applied to vertices and edges
- verify rebuild helpers generate editable cells instead of image/embed nodes
- verify representative figure generators produce the expected number and kinds of cells

### Integration tests

- generate a representative `pdf+tex` figure and inspect structure
- generate a representative `pdf-only` figure and inspect structure
- verify output files exist and parse as draw.io XML

## Risks and mitigations

- TikZ is too broad to parse generally:
  Use source-specific builders rather than a full TikZ engine.

- Layout drift from the reference PDF:
  Prefer coordinates and semantic groupings from the `.tex` source where available.

- Font mismatch across draw.io environments:
  Store `Songti SC` explicitly in the draw.io style so macOS draw.io resolves it predictably.

## Success criteria

- 13 target figures produce `.drawio` files.
- The files open in draw.io without import errors.
- Shapes, arrows, and text are editable primitives.
- No screenshot or raster fallback is used.
- Text defaults to Songti.
