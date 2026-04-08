"""Tests for editable draw.io rebuild helpers and figure generators."""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from cli_anything.drawio.utils import drawio_xml
from cli_anything.drawio.utils import rebuild
from cli_anything.drawio.rebuild.targets import TARGETS
from cli_anything.drawio.rebuild import run_rebuild


class TestRebuildHelpers:
    def test_default_text_style_uses_songti(self):
        style = rebuild.default_text_style(font_size=13)
        assert style["fontFamily"] == "Songti SC"
        assert style["fontSize"] == "13"

    def test_add_box_applies_songti_defaults(self):
        root = drawio_xml.create_blank_diagram()
        cell_id = rebuild.add_box(root, 10, 20, 180, 64, "测试方框")
        cell = drawio_xml.find_cell_by_id(root, cell_id)
        style = drawio_xml.parse_style(cell.get("style", ""))
        assert style["fontFamily"] == "Songti SC"
        assert style["whiteSpace"] == "wrap"
        assert "image" not in style
        assert style["html"] == "1"


class TestTargetInventory:
    def test_target_inventory_has_expected_13_figures(self):
        assert len(TARGETS) == 13
        assert "ch3/pgdg_tol_cn" in TARGETS
        assert "ch4/fig2_architecture" in TARGETS


class TestGenerators:
    def test_fig2_architecture_generator_creates_key_blocks(self, tmp_path):
        result = run_rebuild.run_selected(
            ["ch4/fig2_architecture"],
            base_dir=Path("/Users/daijidong/Pictures/figures-drawio"),
            output_dir=tmp_path,
        )
        output = Path(result[0])
        assert output.exists()

        root = drawio_xml.parse_drawio(str(output))
        vertices = drawio_xml.get_vertices(root)
        labels = [cell.get("value", "") for cell in vertices]
        assert any("下投影" in label for label in labels)
        assert any("自注意力" in label for label in labels)
        assert any("坐标锚定" in label for label in labels)

        for cell in vertices:
            style = drawio_xml.parse_style(cell.get("style", ""))
            assert style.get("fontFamily") == "Songti SC"
            assert "image" not in style

    def test_pdf_only_generator_outputs_editable_cells(self, tmp_path):
        result = run_rebuild.run_selected(
            ["ch3/pgdg_tol_cn"],
            base_dir=Path("/Users/daijidong/Pictures/figures-drawio"),
            output_dir=tmp_path,
        )
        output = Path(result[0])
        root = drawio_xml.parse_drawio(str(output))
        assert len(drawio_xml.get_vertices(root)) > 0
        assert len(drawio_xml.get_edges(root)) > 0
        for cell in drawio_xml.get_vertices(root):
            style = drawio_xml.parse_style(cell.get("style", ""))
            assert style.get("fontFamily") == "Songti SC"
            assert "image" not in style

    def test_run_all_generates_expected_outputs(self, tmp_path):
        outputs = run_rebuild.run_all(
            base_dir=Path("/Users/daijidong/Pictures/figures-drawio"),
            output_dir=tmp_path,
        )
        assert len(outputs) == 13
        for path in outputs:
            output = Path(path)
            assert output.exists()
            parsed = drawio_xml.parse_drawio(str(output))
            assert parsed.tag == "mxfile"
