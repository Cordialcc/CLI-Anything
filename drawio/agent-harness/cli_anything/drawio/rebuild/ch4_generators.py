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


def build_fig1_teaser(output_path: Path, base_dir: Path):
    session = rb.new_session(1600, 1100)
    root = session.root

    rb.add_box(root, 40, 30, 1380, 110, "大语言模型", fill_color="#E2EFDA", stroke_color="#548235", font_size=26)
    rb.add_text(root, 1260, 35, "LoRA", width=80, height=24, font_size=12, font_color="#C0392B", bold=True)
    rb.add_text(root, 1450, 65, "回答", width=80, height=32, font_size=18)

    for i in range(6):
        rb.add_box(root, 40 + i * 34, 160, 28, 28, "", rounded=False, fill_color="#A8C4E0", stroke_color="#6A9BC3")
        rb.add_box(root, 1140 + i * 34, 160, 28, 28, "", rounded=False, fill_color="#A0D8A8", stroke_color="#6AB876")

    rb.add_frame(root, 40, 210, 820, 360, stroke_color="#C0392B", fill_color="none", dashed=False, label="DAVA 适配器", label_x=260, label_y=215, font_size=22)
    rb.add_text(root, 760, 220, "× α", width=70, height=24, font_size=12)

    vis_tokens = []
    for i in range(6):
        vis_tokens.append(rb.add_box(root, 40 + i * 34, 610, 28, 28, "", rounded=False, fill_color="#A8C4E0", stroke_color="#6A9BC3"))
    rb.add_text(root, 200, 607, "视觉令牌", width=120, height=28, font_size=12, font_color="#666666")
    rgb_box = rb.add_box(root, 40, 745, 200, 100, "RGB 图像", fill_color="#EFEFEF", stroke_color="#666666", font_size=18)
    depth_box = rb.add_box(root, 380, 745, 200, 100, "深度图", fill_color="#EFEFEF", stroke_color="#666666", font_size=18)
    visenc = rb.add_box(root, 30, 645, 210, 90, "视觉编码器", fill_color="#F2F2F2", stroke_color="#9AA0A6", font_size=20)
    backproj = rb.add_box(root, 360, 645, 210, 90, "反投影", fill_color="#F2F2F2", stroke_color="#9AA0A6", font_size=20)
    rb.add_edge(root, rgb_box, visenc, color="#666666", width=1.2, end_arrow="classic")
    rb.add_edge(root, depth_box, backproj, color="#666666", width=1.2, end_arrow="classic")

    down = rb.add_box(root, 240, 290, 120, 46, "下采样", fill_color="#F6F6F6", stroke_color="#BBBBBB", font_size=12)
    plus1 = rb.add_ellipse(root, 220, 390, 36, 36, "+", fill_color="#FFFFFF", stroke_color="#666666", font_size=14, bold=True)
    geom = rb.add_box(root, 430, 280, 170, 60, "几何增强\n自注意力", fill_color="#F6F6F6", stroke_color="#BBBBBB", font_size=12)
    plus2 = rb.add_ellipse(root, 430, 390, 36, 36, "+", fill_color="#FFFFFF", stroke_color="#666666", font_size=14, bold=True)
    up = rb.add_box(root, 650, 290, 120, 46, "上采样", fill_color="#F6F6F6", stroke_color="#BBBBBB", font_size=12)

    abs_panel = rb.add_box(root, 170, 390, 260, 130, "坐标锚定\nN×3 -> Sin -> Proj -> N×512", fill_color="#D6E4F0", stroke_color="#4472C4", font_size=18, bold=True)
    rel_panel = rb.add_box(root, 470, 390, 260, 130, "空间引导\nN×N×4 -> MLP -> Bias", fill_color="#E2EFDA", stroke_color="#548235", font_size=18, bold=True)
    coord_text = rb.add_text(root, 350, 540, "3D 坐标", width=140, height=28, font_size=16, font_color="#7D5BA6", bold=True)
    rb.add_edge(root, backproj, coord_text, color="#C89B4A", width=1.2, end_arrow="classic")

    rb.add_edge(root, vis_tokens[0], down, color="#666666", width=1.2, end_arrow="classic")
    rb.add_edge(root, down, plus1, color="#666666", width=1.2, end_arrow="classic")
    rb.add_edge(root, plus1, geom, color="#666666", width=1.2, end_arrow="classic")
    rb.add_edge(root, geom, plus2, color="#666666", width=1.2, end_arrow="classic")
    rb.add_edge(root, plus2, up, color="#666666", width=1.2, end_arrow="classic")
    rb.add_edge(root, up, vis_tokens[-1], color="#666666", width=1.2, end_arrow="classic")
    rb.add_edge(root, abs_panel, plus1, color="#4472C4", width=1.4, end_arrow="classic")
    rb.add_edge(root, rel_panel, geom, color="#548235", width=1.4, end_arrow="classic")
    rb.add_line(root, 70, 624, 70, 292, color="#666666", width=1.0)
    rb.add_line(root, 70, 292, 240, 292, color="#666666", width=1.0, end_arrow="classic")

    tokenizer = rb.add_box(root, 1070, 320, 220, 80, "分词器", fill_color="#F2F2F2", stroke_color="#AAAAAA", font_size=24)
    qbox = rb.add_box(root, 1060, 430, 260, 130, "文本输入\n“What is the distance\nto the nearest car?”", fill_color="#FFFFFF", stroke_color="#CCCCCC", font_size=16)
    rb.add_edge(root, qbox, tokenizer, color="#777777", width=1.2, end_arrow="classic")
    rb.add_edge(root, tokenizer, vis_tokens[-1], color="#777777", width=1.2, end_arrow="classic")
    rb.add_edge(root, vis_tokens[-1], vis_tokens[-1], color="#777777", width=1.0, end_arrow="classic")

    return _finish(session, output_path)


def build_fig2_architecture(output_path: Path, base_dir: Path):
    session = rb.new_session(1600, 1250)
    root = session.root

    rb.add_text(root, 560, 20, "DAVA 模块", width=220, height=30, font_size=22, bold=True)
    rb.add_text(root, 765, 22, "(7.8M 参数)", width=140, height=26, font_size=16)
    rb.add_text(root, 590, 50, "视觉令牌", width=160, height=24, font_size=16, bold=True)

    vin = rb.add_text(root, 90, 70, "V ∈ R^(B×N×3584)", width=240, height=28, font_size=18, bold=True)
    rb.add_text(root, 137, 98, "视觉令牌", width=120, height=20, font_size=12, font_color="#666666")

    down = rb.add_box(root, 130, 135, 240, 80, "下投影", fill_color="#F2F2F2", stroke_color="#888888", font_size=24)
    rb.add_text(root, 395, 155, "Wdown: 3584 -> 512", width=220, height=24, font_size=16)
    plus1 = rb.add_ellipse(root, 275, 260, 50, 50, "+", fill_color="#FFFFFF", stroke_color="#777777", font_size=18, bold=True)
    rb.add_text(root, 80, 270, "式 2", width=50, height=20, font_size=14)
    ln1 = rb.add_box(root, 130, 345, 240, 78, "LayerNorm", fill_color="#F2F2F2", stroke_color="#888888", font_size=20)
    attn = rb.add_box(root, 130, 485, 240, 105, "自注意力\nH=8, dk=64", fill_color="#F2F2F2", stroke_color="#888888", font_size=22)
    rb.add_text(root, 80, 520, "式 3", width=50, height=20, font_size=14)
    plus2 = rb.add_ellipse(root, 275, 630, 50, 50, "+", fill_color="#FFFFFF", stroke_color="#777777", font_size=18, bold=True)
    lnffn = rb.add_box(root, 130, 720, 240, 92, "LayerNorm + FFN\n512 -> 1024 -> 512", fill_color="#F2F2F2", stroke_color="#888888", font_size=18)
    rb.add_text(root, 80, 745, "式 4", width=50, height=20, font_size=14)
    plus3 = rb.add_ellipse(root, 275, 865, 50, 50, "+", fill_color="#FFFFFF", stroke_color="#777777", font_size=18, bold=True)
    up = rb.add_box(root, 130, 960, 240, 82, "上投影", fill_color="#F2F2F2", stroke_color="#888888", font_size=24)
    rb.add_text(root, 395, 980, "Wup: 512 -> 3584\n零初始化", width=250, height=44, font_size=16, align="left")
    plus4 = rb.add_ellipse(root, 275, 1085, 50, 50, "+", fill_color="#FFFFFF", stroke_color="#777777", font_size=18, bold=True)
    rb.add_text(root, 35, 1085, "α\n× 1/db = 0.125", width=120, height=60, font_size=14)
    rb.add_text(root, 82, 1128, "式 5", width=50, height=20, font_size=14)
    vout = rb.add_text(root, 95, 1160, "V' ∈ R^(B×N×3584)\n增强后令牌", width=280, height=44, font_size=18, bold=True)

    coord_info = rb.add_box(root, 930, 90, 300, 90, "pi = (Xi, Yi, Zi)\n每令牌三维坐标", fill_color="#F2F2F2", stroke_color="#888888", font_size=18, bold=True)
    absbox = rb.add_box(root, 970, 250, 350, 250, "坐标锚定\np × sc   (sc=30)\n↓\n正弦 PE   (dpe=4002)\n↓\n线性层 + GELU -> 512", fill_color="#D6E4F0", stroke_color="#4472C4", font_size=20, bold=True)
    relbox = rb.add_box(root, 970, 670, 350, 250, "空间引导\nδij = pi - pj\nrij = [ΔX, ΔY, ΔZ, ||δ||]\n↓\nMLP: 4 -> 32 -> 8\nτ·tanh(.),  τ=5", fill_color="#E2EFDA", stroke_color="#548235", font_size=20, bold=True)

    rb.add_frame(root, 40, 60, 1460, 1120, stroke_color="#E8A299", fill_color="none", dashed=True)

    rb.add_edge(root, vin, down, color="#777777", width=1.2, end_arrow="classic")
    rb.add_edge(root, down, plus1, color="#777777", width=1.2, end_arrow="classic")
    rb.add_edge(root, plus1, ln1, color="#777777", width=1.2, end_arrow="classic")
    rb.add_edge(root, ln1, attn, color="#777777", width=1.2, end_arrow="classic")
    rb.add_edge(root, attn, plus2, color="#777777", width=1.2, end_arrow="classic")
    rb.add_edge(root, plus2, lnffn, color="#777777", width=1.2, end_arrow="classic")
    rb.add_edge(root, lnffn, plus3, color="#777777", width=1.2, end_arrow="classic")
    rb.add_edge(root, plus3, up, color="#777777", width=1.2, end_arrow="classic")
    rb.add_edge(root, up, plus4, color="#777777", width=1.2, end_arrow="classic")
    rb.add_edge(root, plus4, vout, color="#777777", width=1.2, end_arrow="classic")
    rb.add_edge(root, coord_info, absbox, color="#4472C4", width=1.2, end_arrow="classic")
    rb.add_edge(root, coord_info, relbox, color="#548235", width=1.2, end_arrow="classic")
    rb.add_edge(root, absbox, plus1, "eabs", color="#4472C4", width=1.6, end_arrow="classic")
    rb.add_edge(root, relbox, attn, "brel", color="#548235", width=1.6, end_arrow="classic")

    rb.add_line(root, 130, 390, 60, 390, color="#BDBDBD", width=1.0, dashed=True)
    rb.add_line(root, 60, 390, 60, 650, color="#BDBDBD", width=1.0, dashed=True)
    rb.add_line(root, 60, 650, 250, 650, color="#BDBDBD", width=1.0, dashed=True)
    rb.add_line(root, 130, 650, 40, 650, color="#BDBDBD", width=1.0, dashed=True)
    rb.add_line(root, 40, 650, 40, 888, color="#BDBDBD", width=1.0, dashed=True)
    rb.add_line(root, 40, 888, 250, 888, color="#BDBDBD", width=1.0, dashed=True)
    rb.add_text(root, 85, 1115, "跳跃连接", width=110, height=20, font_size=12, font_color="#999999")

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
