"""Tests for editable draw.io rebuild helpers and figure generators."""

import os
import sys
from pathlib import Path
from urllib.parse import unquote

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

    def test_add_image_embeds_png_data_uri(self):
        root = drawio_xml.create_blank_diagram()
        image_path = Path("/Users/daijidong/Pictures/figures-drawio/ch4/images/sample_rgb_thumb.png")
        cell_id = rebuild.add_image(root, 12, 18, 100, 56, image_path)
        cell = drawio_xml.find_cell_by_id(root, cell_id)
        style = drawio_xml.parse_style(cell.get("style", ""))
        assert style["shape"] == "image"
        assert unquote(style["image"]).startswith("data:image/png;base64,")
        assert style["imageAspect"] == "0"


class TestTargetInventory:
    def test_target_inventory_has_expected_13_figures(self):
        assert len(TARGETS) == 13
        assert "ch3/pgdg_tol_cn" in TARGETS
        assert "ch4/fig2_architecture" in TARGETS


class TestGenerators:
    def test_fig1_teaser_generator_preserves_source_thumbnails_and_micro_labels(self, tmp_path):
        result = run_rebuild.run_selected(
            ["ch4/fig1_teaser"],
            base_dir=Path("/Users/daijidong/Pictures/figures-drawio"),
            output_dir=tmp_path,
        )
        output = Path(result[0])
        assert output.exists()

        root = drawio_xml.parse_drawio(str(output))
        vertices = drawio_xml.get_vertices(root)
        edges = drawio_xml.get_edges(root)
        image_vertices = []
        labels = [cell.get("value", "") for cell in vertices]
        labels.extend(cell.get("value", "") for cell in edges)

        for cell in vertices:
            style = drawio_xml.parse_style(cell.get("style", ""))
            assert style.get("fontFamily") == "Songti SC"
            if style.get("shape") == "image":
                image_vertices.append(cell)

        assert len(image_vertices) >= 4
        for cell in image_vertices:
            style = drawio_xml.parse_style(cell.get("style", ""))
            assert unquote(style["image"]).startswith("data:image/png;base64,")

        for token in [
            "DAVA 适配器",
            "坐标锚定",
            "空间引导",
            "Sin",
            "Proj",
            "MLP",
            "Bias",
            "3D 坐标",
            "×α",
            "RGB 图像",
            "深度图",
            "文本输入",
            "分词器",
            "大语言模型",
            "回答",
            "深度估计器",
        ]:
            assert any(token in label for label in labels), token

        assert len(vertices) >= 55
        assert len(edges) >= 22

    def test_fig2_architecture_generator_preserves_residuals_and_equation_labels(self, tmp_path):
        result = run_rebuild.run_selected(
            ["ch4/fig2_architecture"],
            base_dir=Path("/Users/daijidong/Pictures/figures-drawio"),
            output_dir=tmp_path,
        )
        output = Path(result[0])
        assert output.exists()

        root = drawio_xml.parse_drawio(str(output))
        vertices = drawio_xml.get_vertices(root)
        edges = drawio_xml.get_edges(root)
        labels = [cell.get("value", "") for cell in vertices]
        labels.extend(cell.get("value", "") for cell in edges)

        for token in [
            "下投影",
            "自注意力",
            "坐标锚定",
            "式 2",
            "式 3",
            "式 4",
            "式 5",
            "跳跃连接",
            "e<sub>abs</sub>",
            "b<sub>rel</sub>",
            "p<sub>i</sub>",
            "X<sub>i</sub>",
        ]:
            assert any(token in label for label in labels), token

        for cell in vertices:
            style = drawio_xml.parse_style(cell.get("style", ""))
            assert style.get("fontFamily") == "Songti SC"
            assert "image" not in style

        dashed_edges = [
            cell for cell in edges
            if drawio_xml.parse_style(cell.get("style", "")).get("dashed") == "1"
        ]
        assert len(dashed_edges) >= 3
        assert len(vertices) >= 42
        assert len(edges) >= 22

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
