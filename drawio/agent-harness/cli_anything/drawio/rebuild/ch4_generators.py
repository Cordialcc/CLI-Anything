"""Editable rebuild generators for ch4 figures."""

from __future__ import annotations

import math
from pathlib import Path

from ..utils import rebuild as rb


def _finish(session, output_path: Path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rb.save_session(session, output_path)
    return {"output": str(output_path)}


def _chart_y(top: float, height: float, y_min: float, y_max: float, value: float) -> float:
    scale = height / (y_max - y_min)
    return top + height - (value - y_min) * scale


def _chart_axes(root, left, top, width, height, y_min, y_max, y_ticks, y_label):
    for tick in y_ticks:
        y = _chart_y(top, height, y_min, y_max, tick)
        rb.add_line(root, left, y, left + width, y, color="#E0E0E0", width=1.0)
        rb.add_text(root, left - 55, y - 14, str(tick), width=40, height=24, font_size=10, align="right")
    rb.add_line(root, left, top, left, top + height, color="#444444", width=1.2)
    rb.add_line(root, left, top + height, left + width, top + height, color="#444444", width=1.2)
    rb.add_text(root, left - 110, top + height / 2 - 20, y_label, width=100, height=80, font_size=12)


def _add_path(root, points, *, color="#666666", width=1.0, dashed=False, end_arrow="none", start_arrow="none"):
    for index, (start, end) in enumerate(zip(points, points[1:])):
        rb.add_line(
            root,
            start[0],
            start[1],
            end[0],
            end[1],
            color=color,
            width=width,
            dashed=dashed,
            start_arrow=start_arrow if index == 0 else "none",
            end_arrow=end_arrow if index == len(points) - 2 else "none",
        )


def build_fig1_teaser(output_path: Path, base_dir: Path):
    scale = 64.0
    x_min, x_max = -0.40, 10.60
    y_min, y_max = -0.85, 7.00
    page_width = int(round((x_max - x_min) * scale))
    page_height = int(round((y_max - y_min) * scale))
    session = rb.new_session(page_width, page_height)
    root = session.root

    def point(x_cm: float, y_cm: float) -> tuple[float, float]:
        return ((x_cm - x_min) * scale, (y_max - y_cm) * scale)

    def center_rect(x_cm: float, y_cm: float, w_cm: float, h_cm: float) -> tuple[float, float, float, float]:
        left = (x_cm - x_min) * scale - w_cm * scale / 2
        top = (y_max - y_cm) * scale - h_cm * scale / 2
        return left, top, w_cm * scale, h_cm * scale

    def corner_rect(x1_cm: float, y1_cm: float, x2_cm: float, y2_cm: float) -> tuple[float, float, float, float]:
        left = (x1_cm - x_min) * scale
        top = (y_max - y2_cm) * scale
        return left, top, (x2_cm - x1_cm) * scale, (y2_cm - y1_cm) * scale

    def add_cm_box(x_cm, y_cm, w_cm, h_cm, label="", **kwargs):
        return rb.add_box(root, *center_rect(x_cm, y_cm, w_cm, h_cm), label, **kwargs)

    def add_cm_text(x_cm, y_cm, label, *, w_cm=1.6, h_cm=0.35, raw_html=False, **kwargs):
        left, top, width, height = center_rect(x_cm, y_cm, w_cm, h_cm)
        return rb.add_text(root, left, top, label, width=width, height=height, raw_html=raw_html, **kwargs)

    def add_cm_image(x_cm, y_cm, w_cm, h_cm, image_path, **kwargs):
        return rb.add_image(root, *center_rect(x_cm, y_cm, w_cm, h_cm), image_path, **kwargs)

    def add_grid(x1_cm, y1_cm, x2_cm, y2_cm, *, fill_color, stroke_color, step_cm):
        left, top, width, height = corner_rect(x1_cm, y1_cm, x2_cm, y2_cm)
        rb.add_box(
            root,
            left,
            top,
            width,
            height,
            "",
            rounded=False,
            fill_color=fill_color,
            stroke_color=stroke_color,
            stroke_width=0.4,
        )
        step_px = step_cm * scale
        columns = int(round(width / step_px))
        rows = int(round(height / step_px))
        for index in range(1, columns):
            x = left + index * step_px
            rb.add_line(root, x, top, x, top + height, color=stroke_color, width=0.35)
        for index in range(1, rows):
            y = top + index * step_px
            rb.add_line(root, left, y, left + width, y, color=stroke_color, width=0.35)

    rgb_path = base_dir / "ch4" / "images" / "sample_rgb_thumb.png"
    depth_path = base_dir / "ch4" / "images" / "sample_depth_thumb.png"

    add_cm_image(0.9, 0.0, 2.0, 1.13, rgb_path, stroke_color="#000000", stroke_width=0.8)
    add_cm_image(3.95, 0.0, 2.0, 1.13, depth_path, stroke_color="#000000", stroke_width=0.8)
    add_cm_text(0.9, -0.72, "RGB 图像", w_cm=1.5, h_cm=0.30, font_size=10)
    add_cm_text(3.95, -0.72, "深度图", w_cm=1.2, h_cm=0.30, font_size=10)

    visenc = add_cm_box(0.9, 1.5, 2.0, 0.85, "视觉编码器", fill_color="#ECEEF0", stroke_color="#9AA0A6", font_size=11)
    bproj = add_cm_box(3.95, 1.5, 2.3, 0.85, "反投影", fill_color="#ECEEF0", stroke_color="#9AA0A6", font_size=11)
    add_cm_text(0.12, 1.88, "❄", w_cm=0.20, h_cm=0.20, font_size=10, font_color="#9AA0A6")
    _add_path(root, [point(0.9, 0.56), point(0.9, 1.08)], color="#6A6E73", width=0.8, end_arrow="classic")
    _add_path(root, [point(3.95, 0.56), point(3.95, 1.08)], color="#6A6E73", width=0.8, end_arrow="classic")

    vis_start = 0.9 - (5 * 0.32 + 0.28) / 2
    for index in range(6):
        add_cm_box(
            vis_start + index * 0.32 + 0.14,
            2.34,
            0.28,
            0.28,
            "",
            rounded=False,
            fill_color="#A8C4E0",
            stroke_color="#6A9BC3",
            stroke_width=0.5,
        )
    add_cm_text(2.55, 2.34, "视觉令牌", w_cm=0.95, h_cm=0.22, font_size=8, font_color="#444444")
    _add_path(root, [point(0.9, 1.92), point(0.9, 2.20)], color="#6A6E73", width=0.8, end_arrow="classic")
    _add_path(root, [point(3.95, 1.92), point(3.95, 2.20)], color="#6A6E73", width=0.8, end_arrow="classic")

    dot_points = [(-0.5, -0.1), (-0.3, 0.1), (-0.2, -0.15), (0.0, 0.05)]
    for dx, dy in dot_points:
        px, py = point(3.95 + dx, 2.34 + dy)
        rb.add_ellipse(root, px - 2.2, py - 2.2, 4.4, 4.4, "", fill_color="#D4A06A", stroke_color="#D4A06A")
    _add_path(
        root,
        [point(3.45, 2.24), point(3.65, 2.44), point(3.95, 2.39)],
        color="#D4A06A",
        width=0.5,
    )
    add_cm_text(4.55, 2.34, "3D 坐标", w_cm=0.9, h_cm=0.24, font_size=8, bold=True, font_color="#7B6AB1")

    frame_left, frame_top, frame_width, frame_height = center_rect(3.4, 4.0, 6.8, 2.75)
    rb.add_box(
        root,
        frame_left,
        frame_top,
        frame_width,
        frame_height,
        "",
        rounded=True,
        fill_color="#FDF2F0",
        stroke_color="#C0392B",
        stroke_width=1.0,
    )
    add_cm_text(3.4, 5.97, "DAVA 适配器", w_cm=2.3, h_cm=0.30, font_size=12, bold=True)
    add_cm_text(6.55, 5.97, "🔥", w_cm=0.25, h_cm=0.25, font_size=12, font_color="#C0392B")

    abs_left, abs_top, abs_width, abs_height = corner_rect(1.1, 2.85, 3.9, 4.0)
    rb.add_box(root, abs_left, abs_top, abs_width, abs_height, "", rounded=True, fill_color="#EEF4FB", stroke_color="#B7CBE5", stroke_width=0.5)
    title_left, title_top, title_width, title_height = corner_rect(1.22, 3.69, 3.78, 3.92)
    rb.add_box(root, title_left, title_top, title_width, title_height, "", rounded=True, fill_color="#D6E4F0", stroke_color="#C8D8EE", stroke_width=0.4)
    add_cm_text(2.5, 3.805, "坐标锚定", w_cm=1.1, h_cm=0.22, font_size=8, bold=True, font_color="#4472C4")

    add_grid(1.43, 2.93, 1.67, 3.35, fill_color="#D6E4F0", stroke_color="#4472C4", step_cm=0.08)
    add_cm_text(1.55, 3.40, "N×3", w_cm=0.40, h_cm=0.15, font_size=6, font_color="#4472C4")
    _add_path(root, [point(1.71, 3.07), point(2.03, 3.07)], color="#4472C4", width=0.5, end_arrow="classic")
    add_cm_text(1.87, 3.20, "Sin", w_cm=0.30, h_cm=0.12, font_size=6, font_color="#4472C4")
    add_grid(2.14, 2.93, 2.64, 3.35, fill_color="#D6E4F0", stroke_color="#4472C4", step_cm=0.08)
    add_cm_text(2.39, 3.40, "N×d<sub>pe</sub>", w_cm=0.60, h_cm=0.15, font_size=6, font_color="#4472C4", raw_html=True)
    _add_path(root, [point(2.68, 3.07), point(2.94, 3.07)], color="#4472C4", width=0.5, end_arrow="classic")
    add_cm_text(2.81, 3.20, "Proj", w_cm=0.36, h_cm=0.12, font_size=6, font_color="#4472C4")
    add_grid(3.05, 2.93, 3.51, 3.35, fill_color="#BFD6F1", stroke_color="#4472C4", step_cm=0.08)
    add_cm_text(3.28, 3.40, "N×512", w_cm=0.50, h_cm=0.15, font_size=6, font_color="#4472C4")
    add_cm_text(3.47, 3.15, "PE", w_cm=0.22, h_cm=0.12, font_size=6, font_color="#4472C4")

    rel_left, rel_top, rel_width, rel_height = corner_rect(4.05, 2.85, 6.7, 4.0)
    rb.add_box(root, rel_left, rel_top, rel_width, rel_height, "", rounded=True, fill_color="#F0F7EB", stroke_color="#C7DEB8", stroke_width=0.5)
    rel_title_left, rel_title_top, rel_title_width, rel_title_height = corner_rect(4.17, 3.69, 6.58, 3.92)
    rb.add_box(root, rel_title_left, rel_title_top, rel_title_width, rel_title_height, "", rounded=True, fill_color="#E2EFDA", stroke_color="#D2E5C7", stroke_width=0.4)
    add_cm_text(5.375, 3.805, "空间引导", w_cm=1.1, h_cm=0.22, font_size=8, bold=True, font_color="#548235")

    for offset in (0.08, 0.04, 0.0):
        add_grid(4.72 + offset, 2.93 + offset, 5.06 + offset, 3.27 + offset, fill_color="#E2EFDA", stroke_color="#548235", step_cm=0.085)
    add_cm_text(5.14, 3.40, "N×N×4", w_cm=0.50, h_cm=0.15, font_size=6, font_color="#548235")
    add_cm_text(4.77, 3.15, "[Δ,d]", w_cm=0.35, h_cm=0.12, font_size=6, font_color="#548235")
    _add_path(root, [point(5.14, 3.07), point(5.56, 3.07)], color="#548235", width=0.5, end_arrow="classic")
    add_cm_text(5.35, 3.20, "MLP", w_cm=0.32, h_cm=0.12, font_size=6, font_color="#548235")
    for offset in (0.08, 0.04, 0.0):
        add_grid(5.60 + offset, 2.93 + offset, 5.94 + offset, 3.27 + offset, fill_color="#E2EFDA", stroke_color="#548235", step_cm=0.085)
    add_cm_text(5.83, 3.40, "H×N×N", w_cm=0.58, h_cm=0.15, font_size=6, font_color="#548235")
    add_cm_text(6.02, 3.15, "Bias", w_cm=0.30, h_cm=0.12, font_size=6, font_color="#548235")

    down = add_cm_box(1.9, 4.40, 0.75, 0.32, "下采样", fill_color="#F8F5F5", stroke_color="#9AA0A6", font_size=6)
    peadd = rb.add_ellipse(root, *center_rect(3.10, 4.40, 0.26, 0.26), "+", fill_color="#FFFFFF", stroke_color="#666666", font_size=8, bold=True)
    sattn = add_cm_box(4.85, 4.40, 1.42, 0.46, "几何增强<br>自注意力", fill_color="#FCE8E4", stroke_color="#D39A92", font_size=6, raw_html=True)
    up = add_cm_box(6.2, 4.40, 0.75, 0.32, "上采样", fill_color="#F8F5F5", stroke_color="#9AA0A6", font_size=6)
    add_node = rb.add_ellipse(root, *center_rect(0.9, 4.76, 0.26, 0.26), "+", fill_color="#FFFFFF", stroke_color="#666666", font_size=8, bold=True)

    _add_path(root, [point(0.9, 2.48), point(0.9, 3.25)], color="#666666", width=0.6)
    _add_path(root, [point(0.9, 3.25), point(0.9, 4.63)], color="#666666", width=0.5, end_arrow="classic")
    _add_path(root, [point(0.9, 3.25), point(1.525, 3.25), point(1.525, 4.40)], color="#666666", width=0.5, end_arrow="classic")
    _add_path(root, [point(3.95, 2.48), point(3.95, 2.76)], color="#D4A06A", width=0.5)
    _add_path(root, [point(3.95, 2.76), point(1.55, 2.76), point(1.55, 2.93)], color="#4472C4", width=0.45, end_arrow="classic")
    _add_path(root, [point(3.95, 2.76), point(4.93, 2.76), point(4.93, 2.93)], color="#548235", width=0.45, end_arrow="classic")
    _add_path(root, [point(3.10, 4.00), point(3.10, 4.27)], color="#4472C4", width=0.45, end_arrow="classic")
    _add_path(root, [point(4.85, 4.00), point(4.85, 4.17)], color="#548235", width=0.45, end_arrow="classic")
    _add_path(root, [point(2.275, 4.40), point(2.97, 4.40)], color="#666666", width=0.5, end_arrow="classic")
    _add_path(root, [point(3.23, 4.40), point(4.14, 4.40)], color="#666666", width=0.5, end_arrow="classic")
    _add_path(root, [point(5.56, 4.40), point(5.825, 4.40)], color="#666666", width=0.5, end_arrow="classic")
    _add_path(root, [point(6.2, 4.56), point(6.2, 4.76), point(1.08, 4.76), point(1.03, 4.76)], color="#C0392B", width=0.5, end_arrow="classic")
    add_cm_text(5.2, 4.98, "×α", w_cm=0.40, h_cm=0.16, font_size=6)
    _add_path(root, [point(0.9, 4.89), point(0.9, 5.15)], color="#666666", width=0.5, end_arrow="classic")

    enr_start = 0.9 - (5 * 0.32 + 0.28) / 2
    for index in range(6):
        add_cm_box(
            enr_start + index * 0.32 + 0.14,
            5.64,
            0.28,
            0.28,
            "",
            rounded=False,
            fill_color="#C5A0C8",
            stroke_color="#A07AA5",
            stroke_width=0.5,
        )
    add_cm_text(0.9, 5.36, "增强视觉令牌", w_cm=1.20, h_cm=0.18, font_size=8)
    _add_path(root, [point(0.9, 5.15), point(0.9, 5.50)], color="#666666", width=0.7, end_arrow="classic")

    add_cm_text(4.75, 5.64, "...", w_cm=0.30, h_cm=0.18, font_size=10)
    txt_start = 8.75 - (5 * 0.32 + 0.28) / 2
    for index in range(6):
        add_cm_box(
            txt_start + index * 0.32 + 0.14,
            5.64,
            0.28,
            0.28,
            "",
            rounded=False,
            fill_color="#FFF8E1",
            stroke_color="#6AB876",
            stroke_width=0.5,
        )
    add_cm_text(8.75, 5.36, "文本令牌", w_cm=0.90, h_cm=0.18, font_size=8)

    qbox = add_cm_box(
        8.75,
        3.40,
        2.50,
        1.50,
        "<b><i>文本输入</i></b><br><br><font color=\"#5A5D61\">&ldquo;What is the distance</font><br><font color=\"#5A5D61\">to the nearest car?&rdquo;</font>",
        fill_color="#FFFFFF",
        stroke_color="#C7C7C7",
        font_size=7,
        align="left",
        raw_html=True,
    )
    tokenizer = add_cm_box(8.75, 4.80, 2.50, 0.75, "分词器", fill_color="#ECEEF0", stroke_color="#9AA0A6", font_size=11)
    _add_path(root, [point(8.75, 4.15), point(8.75, 4.43)], color="#666666", width=0.7, end_arrow="classic")
    _add_path(root, [point(8.75, 5.17), point(8.75, 5.50)], color="#666666", width=0.7, end_arrow="classic")

    llm = add_cm_box(5.0, 6.40, 10.0, 1.0, "大语言模型", fill_color="#E2EFDA", stroke_color="#548235", stroke_width=1.0, font_size=16)
    add_cm_text(0.08, 6.78, "❄", w_cm=0.20, h_cm=0.20, font_size=9, font_color="#9AA0A6")
    add_cm_text(9.55, 6.82, "LoRA", w_cm=0.55, h_cm=0.20, font_size=7, font_color="#C0392B")
    add_cm_text(9.83, 6.78, "🔥", w_cm=0.22, h_cm=0.22, font_size=10, font_color="#C0392B")
    add_cm_text(10.52, 6.40, "回答", w_cm=0.55, h_cm=0.25, font_size=11)
    _add_path(root, [point(10.00, 6.40), point(10.15, 6.40)], color="#666666", width=0.7, end_arrow="classic")

    return _finish(session, output_path)


def build_fig2_architecture(output_path: Path, base_dir: Path):
    session = rb.new_session(900, 980)
    root = session.root

    rb.add_box(root, 24, 48, 822, 830, "", rounded=True, fill_color="#FFFFFF", stroke_color="#E39E97", stroke_width=1.0, dashed=True)
    rb.add_text(root, 330, 18, "DAVA 模块", width=140, height=30, font_size=20, bold=True)
    rb.add_text(root, 468, 20, "(7.8M 参数)", width=120, height=24, font_size=14)

    vin = rb.add_text(
        root,
        46,
        44,
        "<b><i>V</i></b> ∈ <i>R</i><sup>B×N×3584</sup>",
        width=200,
        height=30,
        font_size=17,
        raw_html=True,
    )
    rb.add_text(root, 152, 74, "视觉令牌", width=100, height=18, font_size=10, bold=True)

    down = rb.add_box(root, 72, 94, 174, 58, "下投影", fill_color="#F2F2F2", stroke_color="#888888", font_size=16)
    rb.add_text(root, 266, 108, "<i>W</i><sub>down</sub>: 3584 → 512", width=190, height=22, font_size=13, align="left", raw_html=True)
    plus1 = rb.add_ellipse(root, 147, 176, 34, 34, "+", fill_color="#FFFFFF", stroke_color="#777777", font_size=16, bold=True)
    rb.add_text(root, 28, 184, "式 2", width=40, height=16, font_size=11)
    ln1 = rb.add_box(root, 72, 227, 174, 48, "LayerNorm", fill_color="#F2F2F2", stroke_color="#888888", font_size=14)
    attn = rb.add_box(root, 72, 312, 174, 76, "自注意力<br><font size=\"4\">H=8, d<sub>k</sub>=64</font>", fill_color="#F2F2F2", stroke_color="#888888", font_size=15, raw_html=True)
    rb.add_text(root, 28, 338, "式 3", width=40, height=16, font_size=11)
    plus2 = rb.add_ellipse(root, 147, 415, 34, 34, "+", fill_color="#FFFFFF", stroke_color="#777777", font_size=16, bold=True)
    lnffn = rb.add_box(root, 72, 484, 174, 68, "LayerNorm + FFN<br><font size=\"4\">512 → 1024 → 512</font>", fill_color="#F2F2F2", stroke_color="#888888", font_size=13, raw_html=True)
    rb.add_text(root, 28, 505, "式 4", width=40, height=16, font_size=11)
    plus3 = rb.add_ellipse(root, 147, 579, 34, 34, "+", fill_color="#FFFFFF", stroke_color="#777777", font_size=16, bold=True)
    up = rb.add_box(root, 72, 645, 174, 58, "上投影", fill_color="#F2F2F2", stroke_color="#888888", font_size=16)
    rb.add_text(root, 266, 656, "<i>W</i><sub>up</sub>: 512 → 3584", width=190, height=20, font_size=13, align="left", raw_html=True)
    rb.add_text(root, 266, 680, "零初始化", width=120, height=18, font_size=12, align="left")
    plus4 = rb.add_ellipse(root, 147, 744, 34, 34, "+", fill_color="#FFFFFF", stroke_color="#777777", font_size=16, bold=True)
    rb.add_text(root, 6, 730, "× α/d<sub>b</sub> = 0.125", width=116, height=42, font_size=11, raw_html=True)
    rb.add_text(root, 28, 784, "式 5", width=40, height=16, font_size=11)
    vout = rb.add_text(
        root,
        50,
        812,
        "<b><i>V'</i></b> ∈ <i>R</i><sup>B×N×3584</sup><br>增强后令牌",
        width=240,
        height=38,
        font_size=16,
        align="left",
        raw_html=True,
    )

    coords = rb.add_box(
        root,
        516,
        56,
        170,
        58,
        "<b>p<sub>i</sub> = (X<sub>i</sub>, Y<sub>i</sub>, Z<sub>i</sub>)</b><br>每令牌三维坐标",
        fill_color="#E0E0E0",
        stroke_color="#999999",
        font_size=12,
        raw_html=True,
    )
    absbox = rb.add_box(
        root,
        492,
        155,
        204,
        170,
        "<font color=\"#4472C4\"><b>坐标锚定</b></font><br><br>p × s<sub>c</sub> &nbsp; <font size=\"3\">(s<sub>c</sub>=30)</font><br>↓<br>正弦 PE &nbsp; <font size=\"3\">(d<sub>pe</sub>=4002)</font><br>↓<br>线性层 + GELU → 512",
        fill_color="#D6E4F0",
        stroke_color="#4472C4",
        font_size=12,
        raw_html=True,
    )
    relbox = rb.add_box(
        root,
        492,
        408,
        204,
        170,
        "<font color=\"#548235\"><b>空间引导</b></font><br><br>δ<sub>ij</sub> = p<sub>i</sub> − p<sub>j</sub><br>r<sub>ij</sub> = [ΔX, ΔY, ΔZ, ||δ||]<br>↓<br>MLP: 4 → 32 → 8<br>τ · tanh(·), &nbsp; τ=5",
        fill_color="#E2EFDA",
        stroke_color="#548235",
        font_size=12,
        raw_html=True,
    )

    _add_path(root, [(144, 70), (144, 94)], color="#666666", width=0.8, end_arrow="classic")
    _add_path(root, [(159, 152), (159, 176)], color="#666666", width=0.8, end_arrow="classic")
    _add_path(root, [(159, 210), (159, 227)], color="#666666", width=0.8, end_arrow="classic")
    _add_path(root, [(159, 275), (159, 312)], color="#666666", width=0.8, end_arrow="classic")
    _add_path(root, [(159, 388), (159, 415)], color="#666666", width=0.8, end_arrow="classic")
    _add_path(root, [(159, 449), (159, 484)], color="#666666", width=0.8, end_arrow="classic")
    _add_path(root, [(159, 552), (159, 579)], color="#666666", width=0.8, end_arrow="classic")
    _add_path(root, [(159, 613), (159, 645)], color="#666666", width=0.8, end_arrow="classic")
    _add_path(root, [(159, 703), (159, 744)], color="#666666", width=0.8, end_arrow="classic")
    _add_path(root, [(159, 778), (159, 810)], color="#666666", width=0.8, end_arrow="classic")

    _add_path(root, [(72, 251), (42, 251), (42, 432), (147, 432)], color="#BDBDBD", width=0.9, dashed=True)
    _add_path(root, [(72, 432), (24, 432), (24, 596), (147, 596)], color="#BDBDBD", width=0.9, dashed=True)
    _add_path(root, [(46, 60), (10, 60), (10, 761), (147, 761)], color="#BDBDBD", width=1.0, dashed=True)
    rb.add_text(root, 54, 734, "跳跃连接", width=70, height=16, font_size=10, font_color="#999999")

    _add_path(root, [(601, 114), (601, 142), (552, 142), (552, 155)], color="#4472C4", width=0.9, end_arrow="classic")
    _add_path(root, [(620, 114), (620, 142), (631, 142), (631, 408)], color="#548235", width=0.9, end_arrow="classic")
    _add_path(root, [(492, 240), (452, 240), (452, 193), (181, 193)], color="#4472C4", width=1.0, end_arrow="classic")
    rb.add_text(root, 457, 206, "e<sub>abs</sub>", width=55, height=18, font_size=11, font_color="#4472C4", raw_html=True)
    _add_path(root, [(492, 493), (452, 493), (452, 350), (246, 350)], color="#548235", width=1.0, end_arrow="classic")
    rb.add_text(root, 458, 507, "b<sub>rel</sub>", width=55, height=18, font_size=11, font_color="#548235", raw_html=True)

    return _finish(session, output_path)


def build_fig3_backprojection_h(output_path: Path, base_dir: Path):
    session = rb.new_session(1500, 500)
    root = session.root

    depth = rb.add_box(root, 70, 180, 150, 70, "深度图 D", fill_color="#E8DAEF", stroke_color="#8E44AD", font_size=18)
    bproj = rb.add_box(root, 300, 180, 160, 70, "反投影", fill_color="#F2F2F2", stroke_color="#888888", font_size=18)
    c3d = rb.add_box(root, 540, 180, 170, 70, "三维坐标", fill_color="#E8DAEF", stroke_color="#8E44AD", font_size=18)
    pool = rb.add_box(root, 790, 180, 170, 70, "2×2 池化", fill_color="#F2F2F2", stroke_color="#888888", font_size=18)
    ptok = rb.add_box(root, 1040, 180, 170, 70, "令牌位置", fill_color="#E8DAEF", stroke_color="#8E44AD", font_size=18)
    norm = rb.add_box(root, 1270, 165, 170, 90, "÷ med(Z)\n× sc=30", fill_color="#F2F2F2", stroke_color="#888888", font_size=18)
    out = rb.add_box(root, 1500 - 180, 180, 160, 70, "p_scaled_i", fill_color="#D6E4F0", stroke_color="#4472C4", font_size=18, bold=True)

    for a, b in [(depth, bproj), (bproj, c3d), (c3d, pool), (pool, ptok), (ptok, norm), (norm, out)]:
        rb.add_edge(root, a, b, color="#666666", width=1.2, end_arrow="classic")
    rb.add_text(root, 85, 150, "H × W", width=100, height=20, font_size=12, font_color="#666666")
    rb.add_text(root, 335, 150, "式 6 / K", width=120, height=20, font_size=12, font_color="#666666")
    rb.add_text(root, 560, 150, "H × W × 3", width=120, height=20, font_size=12, font_color="#666666")
    rb.add_text(root, 800, 150, "对齐 Merger", width=120, height=20, font_size=12, font_color="#666666")
    rb.add_text(root, 1080, 150, "N × 3", width=80, height=20, font_size=12, font_color="#666666")
    rb.add_text(root, 1300, 145, "式 7", width=60, height=20, font_size=12, font_color="#666666")
    rb.add_text(root, 1330, 270, "[0, ~90]", width=90, height=20, font_size=12, font_color="#4472C4")
    rb.add_line(root, 1060, 290, 1190, 290, color="#888888", width=1.0)
    rb.add_line(root, 1315, 290, 1440, 290, color="#4472C4", width=1.0)
    rb.add_text(root, 1070, 300, "[0, ~3]", width=110, height=18, font_size=11, font_color="#666666")
    rb.add_text(root, 1320, 300, "[0, ~90]", width=110, height=18, font_size=11, font_color="#4472C4")

    return _finish(session, output_path)


def build_fig4_waterfall(output_path: Path, base_dir: Path):
    session = rb.new_session(1450, 900)
    root = session.root
    left, top, width, height = 120, 120, 980, 450
    y_min, y_max = 48, 68
    _chart_axes(root, left, top, width, height, y_min, y_max, range(48, 67, 2), "三维空间推理准确率 (%)")

    values = [
        ("LoRA\n基线", 51.46, 51.46, "#555555"),
        ("容量\n效应", 51.46, 53.65, "#999999"),
        ("坐标\n锚定", 53.65, 61.50, "#4472C4"),
        ("空间\n引导", 61.50, 63.95, "#548235"),
        ("DAVA\n完整", 48.00, 63.95, "#C0392B"),
    ]
    x_positions = [220, 400, 610, 820, 1050]
    for (label, y0, y1, color), x in zip(values, x_positions):
        y = _chart_y(top, height, y_min, y_max, y1)
        bar_height = max(6, (_chart_y(top, height, y_min, y_max, y0) - y))
        rb.add_box(root, x, y, 80, bar_height, "", rounded=False, fill_color=color, stroke_color="#333333")
        rb.add_text(root, x - 10, y - 28, f"{y1:.2f}" if y0 == 48 else f"+{(y1-y0):.2f}", width=100, height=24, font_size=12, font_color=color, bold=True)
        rb.add_text(root, x - 20, top + height + 20, label, width=120, height=42, font_size=14)

    rb.add_text(root, 1180, 180, "+12.49\nvs LoRA", width=110, height=42, font_size=14, bold=True)
    rb.add_text(root, 660, 85, "独立贡献之和: 12.52\n实际组合改进: 10.30\n重叠: 2.22（信息共享）", width=320, height=60, font_size=12)

    return _finish(session, output_path)


def build_fig6_perturbation(output_path: Path, base_dir: Path):
    session = rb.new_session(1400, 820)
    root = session.root
    left, top, width, height = 120, 120, 920, 420
    y_min, y_max = 45, 67
    _chart_axes(root, left, top, width, height, y_min, y_max, range(46, 67, 2), "三维空间推理准确率 (%)")

    bars = [
        ("正确深度", 63.95, "#27AE60"),
        ("平坦深度", 57.29, "#E67E22"),
        ("打乱深度", 48.11, "#E74C3C"),
        ("容量对照", 53.65, "#999999"),
        ("LoRA", 51.46, "#2C3E50"),
    ]
    xs = [180, 360, 540, 760, 940]
    for (label, value, color), x in zip(bars, xs):
        y = _chart_y(top, height, y_min, y_max, value)
        bar_height = _chart_y(top, height, y_min, y_max, y_min) - y
        rb.add_box(root, x, y, 85, bar_height, "", rounded=False, fill_color=color, stroke_color="#333333")
        rb.add_text(root, x - 8, y - 28, f"{value:.2f}", width=100, height=24, font_size=12, bold=(label == "正确深度"))
        rb.add_text(root, x - 20, top + height + 18, label, width=130, height=28, font_size=14)

    baseline_y = _chart_y(top, height, y_min, y_max, 51.46)
    rb.add_line(root, left, baseline_y, left + width, baseline_y, color="#999999", width=1.0, dashed=True)
    rb.add_text(root, 540, 610, "错误深度\n低于无深度", width=120, height=40, font_size=12)
    rb.add_text(root, 1090, 220, "-15.84", width=80, height=24, font_size=14, bold=True)
    rb.add_text(root, 500, 82, "平坦深度高于容量对照 +3.64", width=260, height=22, font_size=12)

    return _finish(session, output_path)


def build_fig7_selectivity(output_path: Path, base_dir: Path):
    session = rb.new_session(1400, 820)
    root = session.root
    left, top, width, height = 120, 120, 980, 420
    y_min, y_max = 0, 90
    _chart_axes(root, left, top, width, height, y_min, y_max, range(0, 81, 10), "准确率 (%)")

    groups = [
        ("三维空间推理", 51.46, 63.95, "+12.49"),
        ("场景理解", 66.97, 80.14, "+13.17"),
        ("视觉定位", 37.89, 65.91, "+28.02"),
    ]
    base_x = [220, 520, 820]
    for (label, lora, dava, delta), x in zip(groups, base_x):
        yl = _chart_y(top, height, y_min, y_max, lora)
        yd = _chart_y(top, height, y_min, y_max, dava)
        base = _chart_y(top, height, y_min, y_max, 0)
        rb.add_box(root, x, yl, 65, base - yl, "", rounded=False, fill_color="#2C3E50", stroke_color="#333333")
        rb.add_box(root, x + 85, yd, 65, base - yd, "", rounded=False, fill_color="#C0392B", stroke_color="#333333")
        rb.add_text(root, x - 5, yl - 26, f"{lora:.2f}", width=85, height=22, font_size=12)
        rb.add_text(root, x + 80, yd - 26, f"{dava:.2f}", width=85, height=22, font_size=12, bold=True)
        rb.add_text(root, x - 10, top + height + 18, label, width=180, height=28, font_size=14)
        rb.add_text(root, x + 160, (yl + yd) / 2 - 10, delta, width=80, height=22, font_size=12, bold=("28.02" in delta))

    rb.add_box(root, 160, 50, 24, 24, "", rounded=False, fill_color="#2C3E50", stroke_color="#333333")
    rb.add_text(root, 190, 50, "LoRA", width=80, height=24, font_size=12, align="left")
    rb.add_box(root, 280, 50, 24, 24, "", rounded=False, fill_color="#C0392B", stroke_color="#333333")
    rb.add_text(root, 310, 50, "DAVA", width=80, height=24, font_size=12, align="left")

    return _finish(session, output_path)


def build_fig8_params(output_path: Path, base_dir: Path):
    session = rb.new_session(1500, 760)
    root = session.root

    rb.add_text(root, 100, 55, "总可训练参数: 48.2M", width=260, height=28, font_size=16, bold=True, align="left")
    rb.add_box(root, 80, 90, 1005, 70, "LoRA (40.4M, 84%)", rounded=True, fill_color="#EEDAF4", stroke_color="#9B59B6", font_size=20)
    rb.add_box(root, 1095, 90, 195, 70, "7.8M", rounded=True, fill_color="#FADBD8", stroke_color="#C0392B", font_size=18)
    rb.add_text(root, 450, 58, "LoRA", width=120, height=24, font_size=18)
    rb.add_text(root, 1110, 58, "DAVA 模块 (16%)", width=200, height=24, font_size=18)
    rb.add_line(root, 1190, 160, 750, 260, color="#444444", width=1.0, end_arrow="classic")

    x = 120
    y = 320
    widths = [
        ("下投影\n1.84M", 283, "#3498DB"),
        ("坐标投影\n2.05M", 316, "#4472C4"),
        ("自注意力\n1.05M", 162, "#E67E22"),
        ("FFN\n1.05M", 162, "#F39C12"),
        ("上投影\n1.84M", 283, "#1ABC9C"),
        ("关系MLP", 45, "#548235"),
    ]
    for label, w, color in widths:
        rb.add_box(root, x, y, w, 68, label, rounded=False, fill_color=color, stroke_color="#333333", font_size=14)
        x += w
    rb.add_text(root, 100, 412, "DAVA 模块内部分解 (7.8M)", width=260, height=24, font_size=14, align="left")
    rb.add_text(root, 1110, 280, "关系MLP (384 参数)", width=180, height=24, font_size=12)

    return _finish(session, output_path)


def build_fig9_gate_gradient(output_path: Path, base_dir: Path):
    session = rb.new_session(1500, 900)
    root = session.root

    left, top, width, height = 160, 90, 820, 360
    x_min, x_max = -10, 4
    y_min, y_max = 0.0, 0.35

    for tick in [0.0, 0.1, 0.2, 0.3]:
        y = _chart_y(top, height, y_min, y_max, tick)
        rb.add_line(root, left, y, left + width, y, color="#D9D9D9", width=1.0)
        rb.add_text(root, left - 65, y - 14, f"{tick:.1f}".rstrip("0").rstrip("."), width=50, height=22, font_size=11, align="right")
    for tick in [-10, -8, -6, -4, -2, 0, 2, 4]:
        x = left + (tick - x_min) * width / (x_max - x_min)
        rb.add_line(root, x, top, x, top + height, color="#D9D9D9", width=1.0)
        rb.add_text(root, x - 18, top + height + 8, str(tick), width=36, height=22, font_size=11)

    rb.add_box(root, left, top, width * (6 / 14), height, "", rounded=False, fill_color="#FADBD8", stroke_color="none")
    rb.add_line(root, left, top, left, top + height, color="#444444", width=1.2)
    rb.add_line(root, left, top + height, left + width, top + height, color="#444444", width=1.2)
    rb.add_text(root, left - 120, top + 100, "σ'(g) = σ(g)(1 - σ(g))", width=120, height=120, font_size=16)
    rb.add_text(root, left + 250, top + height + 40, "g 处梯度弱 100×", width=180, height=24, font_size=12)
    rb.add_text(root, left + 145, top + 110, "梯度死区", width=70, height=120, font_size=16, font_color="#C0392B")

    def map_x(x_value):
        return left + (x_value - x_min) * width / (x_max - x_min)

    def map_y(y_value):
        return _chart_y(top, height, y_min, y_max, y_value)

    deriv_points = []
    sigmoid_points = []
    for step in range(0, 57):
        x_value = -10 + step * 0.25
        sigma = 1.0 / (1.0 + math.exp(-x_value))
        deriv = sigma * (1.0 - sigma)
        deriv_points.append((map_x(x_value), map_y(deriv)))
        sigmoid_points.append((map_x(x_value), map_y(0.3 * sigma)))
    rb.add_polyline(root, deriv_points, color="#2980B9", width=2.0)
    rb.add_polyline(root, sigmoid_points, color="#666666", width=1.4, dashed=True)
    dead_x = map_x(-6)
    dead_y = map_y((1 / (1 + math.exp(6))) * (1 - 1 / (1 + math.exp(6))))
    rb.add_ellipse(root, dead_x - 8, dead_y - 8, 16, 16, "", fill_color="#C0392B", stroke_color="#C0392B")
    rb.add_ellipse(root, map_x(0) - 8, map_y(0.25) - 8, 16, 16, "", fill_color="#27AE60", stroke_color="#27AE60")
    rb.add_line(root, dead_x, dead_y - 60, dead_x, dead_y, color="#C0392B", width=1.0, end_arrow="classic")
    rb.add_text(root, dead_x - 170, dead_y - 120, "g0 = -6\nσ(-6) ≈ 0.0025\nσ'(-6) ≈ 0.0025", width=180, height=72, font_size=12, font_color="#C0392B", align="left")
    rb.add_text(root, map_x(0) + 20, map_y(0.25) - 20, "峰值: σ'(0)=0.25", width=150, height=24, font_size=12, align="left")
    rb.add_box(root, 160, 500, 1120, 180, "门控方案:  Wup 范数 = 35.16（随机初始化）， 有效值 =\n35.16 × 0.0025 = 0.088\n\n零初始化:  Wup 范数 = 5.05（从零学习）， 有效值 = 5.05 ×\n1.0 = 5.05   （大 57×）", fill_color="#F2F2F2", stroke_color="#999999", font_size=18)
    rb.add_text(root, 1060, 100, "σ'(g)", width=80, height=24, font_size=14, font_color="#2980B9")
    rb.add_text(root, 1060, 130, "0.3 × σ(g)", width=110, height=24, font_size=14, font_color="#666666")

    return _finish(session, output_path)
