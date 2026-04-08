# Draw.io Editable Rebuild Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build editable `.drawio` reconstructions for 13 target figures under `ch3` and `ch4`, using draw.io shapes and Songti text rather than screenshots or embedded whole-image assets.

**Architecture:** Extend the existing `drawio` agent harness with rebuild helpers, add figure-specific generators for TikZ-backed and PDF-only figures, then batch-generate `.drawio` outputs next to the sources. Keep the rebuild layer thin and explicit rather than attempting a general PDF or TikZ renderer.

**Tech Stack:** Python 3, existing `cli_anything.drawio` modules, `pytest`, draw.io XML generation.

---

### Task 1: Add spec-aware rebuild tests

**Files:**
- Modify: `drawio/agent-harness/cli_anything/drawio/tests/test_core.py`
- Create: `drawio/agent-harness/cli_anything/drawio/tests/test_rebuild.py`

- [ ] **Step 1: Write the failing tests**

```python
from cli_anything.drawio.utils import rebuild

def test_songti_style_is_applied_to_vertex_and_edge_labels():
    style = rebuild.default_text_style(font_size=12)
    assert style["fontFamily"] == "Songti SC"

def test_rebuild_helpers_do_not_create_image_cells():
    root = rebuild.build_smoke_diagram()
    for cell in rebuild.iter_user_cells(root):
        style = cell.get("style", "")
        assert "image=" not in style
        assert "shape=image" not in style
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/daijidong/Pictures/figures-drawio/CLI-Anything/drawio/agent-harness && pytest cli_anything/drawio/tests/test_rebuild.py -v`
Expected: FAIL because `rebuild` module does not exist yet.

- [ ] **Step 3: Write minimal implementation**

```python
# cli_anything/drawio/utils/rebuild.py
def default_text_style(font_size=12):
    return {"fontFamily": "Songti SC", "fontSize": str(font_size)}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /Users/daijidong/Pictures/figures-drawio/CLI-Anything/drawio/agent-harness && pytest cli_anything/drawio/tests/test_rebuild.py -v`
Expected: PASS for the newly added tests.

- [ ] **Step 5: Commit**

```bash
git add drawio/agent-harness/cli_anything/drawio/tests/test_rebuild.py \
        drawio/agent-harness/cli_anything/drawio/utils/rebuild.py
git commit -m "test: add rebuild helper coverage"
```

### Task 2: Add reusable rebuild helpers with Songti defaults

**Files:**
- Modify: `drawio/agent-harness/cli_anything/drawio/utils/drawio_xml.py`
- Create: `drawio/agent-harness/cli_anything/drawio/utils/rebuild.py`
- Test: `drawio/agent-harness/cli_anything/drawio/tests/test_rebuild.py`

- [ ] **Step 1: Write the failing test**

```python
def test_add_box_applies_songti_defaults():
    root = drawio_xml.create_blank_diagram()
    cell_id = rebuild.add_box(root, 10, 20, 100, 50, "测试")
    cell = drawio_xml.find_cell_by_id(root, cell_id)
    style = drawio_xml.parse_style(cell.get("style", ""))
    assert style["fontFamily"] == "Songti SC"
    assert style["whiteSpace"] == "wrap"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/daijidong/Pictures/figures-drawio/CLI-Anything/drawio/agent-harness && pytest cli_anything/drawio/tests/test_rebuild.py::test_add_box_applies_songti_defaults -v`
Expected: FAIL because helper does not exist or styles are incomplete.

- [ ] **Step 3: Write minimal implementation**

```python
def add_box(mxfile, x, y, width, height, label, style="rectangle", **extra):
    cell_id = drawio_xml.add_vertex(mxfile, style, x, y, width, height, label)
    cell = drawio_xml.find_cell_by_id(mxfile, cell_id)
    apply_text_style(cell, **extra)
    return cell_id
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /Users/daijidong/Pictures/figures-drawio/CLI-Anything/drawio/agent-harness && pytest cli_anything/drawio/tests/test_rebuild.py -v`
Expected: PASS for helper-level tests.

- [ ] **Step 5: Commit**

```bash
git add drawio/agent-harness/cli_anything/drawio/utils/drawio_xml.py \
        drawio/agent-harness/cli_anything/drawio/utils/rebuild.py \
        drawio/agent-harness/cli_anything/drawio/tests/test_rebuild.py
git commit -m "feat: add reusable drawio rebuild helpers"
```

### Task 3: Add figure generator modules and target inventory

**Files:**
- Create: `drawio/agent-harness/cli_anything/drawio/rebuild/__init__.py`
- Create: `drawio/agent-harness/cli_anything/drawio/rebuild/targets.py`
- Create: `drawio/agent-harness/cli_anything/drawio/rebuild/ch3_specs.py`
- Create: `drawio/agent-harness/cli_anything/drawio/rebuild/ch4_generators.py`
- Test: `drawio/agent-harness/cli_anything/drawio/tests/test_rebuild.py`

- [ ] **Step 1: Write the failing tests**

```python
from cli_anything.drawio.rebuild.targets import TARGETS

def test_target_inventory_has_expected_13_figures():
    assert len(TARGETS) == 13
    assert "ch4/fig2_architecture" in TARGETS
    assert "ch3/pgdg_tol_cn" in TARGETS
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/daijidong/Pictures/figures-drawio/CLI-Anything/drawio/agent-harness && pytest cli_anything/drawio/tests/test_rebuild.py::test_target_inventory_has_expected_13_figures -v`
Expected: FAIL because target inventory does not exist yet.

- [ ] **Step 3: Write minimal implementation**

```python
TARGETS = {
    "ch3/obb_cn": {...},
    "ch3/pgdg_tol_cn": {...},
    "ch3/pipeline_tol_cn": {...},
    "ch3/sre_cn": {...},
    "ch3/teaser_tol_cn": {...},
    "ch4/fig1_teaser": {...},
    ...
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /Users/daijidong/Pictures/figures-drawio/CLI-Anything/drawio/agent-harness && pytest cli_anything/drawio/tests/test_rebuild.py -v`
Expected: PASS for target inventory tests.

- [ ] **Step 5: Commit**

```bash
git add drawio/agent-harness/cli_anything/drawio/rebuild \
        drawio/agent-harness/cli_anything/drawio/tests/test_rebuild.py
git commit -m "feat: add editable rebuild target inventory"
```

### Task 4: Implement representative TikZ-backed rebuild generators

**Files:**
- Modify: `drawio/agent-harness/cli_anything/drawio/rebuild/ch4_generators.py`
- Test: `drawio/agent-harness/cli_anything/drawio/tests/test_rebuild.py`

- [ ] **Step 1: Write the failing test**

```python
def test_fig2_architecture_generator_creates_main_blocks():
    result = ch4_generators.build_fig2_architecture(tmp_path)
    root = drawio_xml.parse_drawio(result["output"])
    labels = [cell.get("value", "") for cell in drawio_xml.get_vertices(root)]
    assert any("下投影" in label for label in labels)
    assert any("自注意力" in label for label in labels)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/daijidong/Pictures/figures-drawio/CLI-Anything/drawio/agent-harness && pytest cli_anything/drawio/tests/test_rebuild.py::test_fig2_architecture_generator_creates_main_blocks -v`
Expected: FAIL because generator is incomplete.

- [ ] **Step 3: Write minimal implementation**

```python
def build_fig2_architecture(output_dir):
    session = Session()
    session.new_project(page_width=1600, page_height=1200)
    rebuild.add_box(session.root, 300, 160, 220, 58, "下投影")
    rebuild.add_box(session.root, 300, 360, 220, 80, "自注意力")
    ...
    session.save_project(str(output_path))
    return {"output": str(output_path)}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /Users/daijidong/Pictures/figures-drawio/CLI-Anything/drawio/agent-harness && pytest cli_anything/drawio/tests/test_rebuild.py -v`
Expected: PASS for at least one representative ch4 generator.

- [ ] **Step 5: Commit**

```bash
git add drawio/agent-harness/cli_anything/drawio/rebuild/ch4_generators.py \
        drawio/agent-harness/cli_anything/drawio/tests/test_rebuild.py
git commit -m "feat: add editable rebuild generators for ch4 figures"
```

### Task 5: Implement PDF-only manual rebuild generators

**Files:**
- Modify: `drawio/agent-harness/cli_anything/drawio/rebuild/ch3_specs.py`
- Test: `drawio/agent-harness/cli_anything/drawio/tests/test_rebuild.py`

- [ ] **Step 1: Write the failing test**

```python
def test_pdf_only_generator_outputs_editable_cells():
    result = ch3_specs.build_pgdg_tol_cn(tmp_path)
    root = drawio_xml.parse_drawio(result["output"])
    assert len(drawio_xml.get_vertices(root)) > 0
    assert len(drawio_xml.get_edges(root)) > 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/daijidong/Pictures/figures-drawio/CLI-Anything/drawio/agent-harness && pytest cli_anything/drawio/tests/test_rebuild.py::test_pdf_only_generator_outputs_editable_cells -v`
Expected: FAIL because the manual spec generator is missing.

- [ ] **Step 3: Write minimal implementation**

```python
def build_pgdg_tol_cn(output_dir):
    session = Session()
    session.new_project(page_width=1600, page_height=900)
    build_from_spec(session.root, PGDG_TOL_CN_SPEC)
    session.save_project(str(output_path))
    return {"output": str(output_path)}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /Users/daijidong/Pictures/figures-drawio/CLI-Anything/drawio/agent-harness && pytest cli_anything/drawio/tests/test_rebuild.py -v`
Expected: PASS for the manual-spec coverage.

- [ ] **Step 5: Commit**

```bash
git add drawio/agent-harness/cli_anything/drawio/rebuild/ch3_specs.py \
        drawio/agent-harness/cli_anything/drawio/tests/test_rebuild.py
git commit -m "feat: add editable rebuild generators for ch3 pdf-only figures"
```

### Task 6: Add batch rebuild entry point

**Files:**
- Create: `drawio/agent-harness/cli_anything/drawio/rebuild/run_rebuild.py`
- Modify: `drawio/agent-harness/cli_anything/drawio/drawio_cli.py`
- Test: `drawio/agent-harness/cli_anything/drawio/tests/test_rebuild.py`

- [ ] **Step 1: Write the failing test**

```python
def test_batch_rebuild_reports_generated_outputs(tmp_path):
    outputs = run_rebuild.run_selected(["ch4/fig2_architecture"], base_dir=tmp_path)
    assert outputs[0].endswith(".drawio")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/daijidong/Pictures/figures-drawio/CLI-Anything/drawio/agent-harness && pytest cli_anything/drawio/tests/test_rebuild.py::test_batch_rebuild_reports_generated_outputs -v`
Expected: FAIL because batch entry point does not exist.

- [ ] **Step 3: Write minimal implementation**

```python
def run_selected(names, base_dir):
    outputs = []
    for name in names:
        outputs.append(dispatch_target(name, base_dir)["output"])
    return outputs
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /Users/daijidong/Pictures/figures-drawio/CLI-Anything/drawio/agent-harness && pytest cli_anything/drawio/tests/test_rebuild.py -v`
Expected: PASS for batch runner tests.

- [ ] **Step 5: Commit**

```bash
git add drawio/agent-harness/cli_anything/drawio/rebuild/run_rebuild.py \
        drawio/agent-harness/cli_anything/drawio/drawio_cli.py \
        drawio/agent-harness/cli_anything/drawio/tests/test_rebuild.py
git commit -m "feat: add batch editable rebuild command"
```

### Task 7: Generate target outputs and verify structure

**Files:**
- Modify: `ch3/*.drawio`
- Modify: `ch4/*.drawio`
- Modify: `drawio/agent-harness/cli_anything/drawio/tests/TEST.md`

- [ ] **Step 1: Run the batch rebuild command**

Run: `cd /Users/daijidong/Pictures/figures-drawio/CLI-Anything/drawio/agent-harness && python3 -m cli_anything.drawio.rebuild.run_rebuild`
Expected: 13 `.drawio` output paths printed.

- [ ] **Step 2: Verify files exist and parse**

Run: `python3 - <<'PY'\nfrom pathlib import Path\nfrom xml.etree import ElementTree as ET\nfor p in sorted(Path('/Users/daijidong/Pictures/figures-drawio').glob('ch[34]/*.drawio')):\n    ET.parse(p)\n    print(p)\nPY`
Expected: every target `.drawio` parses without XML errors.

- [ ] **Step 3: Run the focused test suite**

Run: `cd /Users/daijidong/Pictures/figures-drawio/CLI-Anything/drawio/agent-harness && pytest cli_anything/drawio/tests/test_rebuild.py cli_anything/drawio/tests/test_core.py -v`
Expected: PASS with zero failures.

- [ ] **Step 4: Append verification notes to TEST.md**

```text
Add a short section describing rebuild coverage, target count, and the exact pytest command output.
```

- [ ] **Step 5: Commit**

```bash
git add /Users/daijidong/Pictures/figures-drawio/ch3/*.drawio \
        /Users/daijidong/Pictures/figures-drawio/ch4/*.drawio \
        drawio/agent-harness/cli_anything/drawio/tests/TEST.md
git commit -m "feat: generate editable drawio rebuild outputs"
```

### Task 8: Push to the user's fork

**Files:**
- Modify: git branch state only

- [ ] **Step 1: Verify git status is clean except intended changes**

Run: `git -C /Users/daijidong/Pictures/figures-drawio/CLI-Anything status --short`
Expected: only the intended rebuild-related files appear before commit, then a clean tree after commit.

- [ ] **Step 2: Push feature branch**

Run: `git -C /Users/daijidong/Pictures/figures-drawio/CLI-Anything push -u fork feature/drawio-editable-rebuild`
Expected: branch published to `Cordialcc/CLI-Anything`.

- [ ] **Step 3: Record resulting branch URL**

```text
https://github.com/Cordialcc/CLI-Anything/tree/feature/drawio-editable-rebuild
```

- [ ] **Step 4: Final verification**

Run: `git -C /Users/daijidong/Pictures/figures-drawio/CLI-Anything status --short`
Expected: clean working tree.
