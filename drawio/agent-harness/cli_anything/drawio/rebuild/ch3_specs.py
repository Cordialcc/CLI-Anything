"""Editable rebuild generators for ch3 PDF-only figures."""

from __future__ import annotations

from pathlib import Path

from ..utils import rebuild as rb


def _finish(session, output_path: Path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rb.save_session(session, output_path)
    return {"output": str(output_path)}


def build_obb_cn(output_path: Path, base_dir: Path):
    session = rb.new_session(1500, 900)
    root = session.root

    rb.add_text(root, 30, 20, "(a) BEV 鸟瞰视角 — 最小多边形距离", width=520, height=30, font_size=18, bold=True, align="left")
    rb.add_text(root, 1040, 20, "(b) 高度分解", width=220, height=30, font_size=18, bold=True, align="left")

    rb.add_prism(root, 90, 250, 220, 150, 70, 45, fill_color="#AFC4DA", stroke_color="#5C7EA3")
    rb.add_text(root, 220, 170, "自车", width=120, height=24, font_size=18)
    rb.add_prism(root, 590, 120, 210, 120, 70, 45, fill_color="#A8D1C8", stroke_color="#2B908F")
    rb.add_text(root, 700, 45, "目标", width=120, height=24, font_size=18)
    rb.add_ellipse(root, 235, 300, 12, 12, "", fill_color="#5C7EA3", stroke_color="#5C7EA3")
    rb.add_ellipse(root, 700, 165, 12, 12, "", fill_color="#2B908F", stroke_color="#2B908F")
    rb.add_line(root, 330, 250, 620, 165, color="#999999", width=1.4, dashed=True, end_arrow="classic")
    rb.add_text(root, 400, 195, "dcenter ×", width=120, height=24, font_size=16, font_color="#666666")
    rb.add_line(root, 310, 360, 625, 205, color="#C59D1C", width=3.0, end_arrow="classic")
    rb.add_text(root, 485, 325, "dsurface ✓", width=160, height=28, font_size=18, font_color="#B8860B", bold=True)
    rb.add_line(root, 25, 470, 855, 130, color="#D6D6D6", width=1.0, end_arrow="classic")
    rb.add_line(root, 140, 560, 910, 225, color="#D6D6D6", width=1.0, end_arrow="classic")
    rb.add_text(root, 500, 515, "dsurface < dcenter", width=220, height=28, font_size=18, bold=True)

    rb.add_box(root, 930, 70, 470, 340, "", fill_color="#F5F5F5", stroke_color="#DDDDDD")
    rb.add_box(root, 975, 195, 150, 90, "", rounded=False, fill_color="#AFC4DA", stroke_color="#5C7EA3")
    rb.add_box(root, 1180, 95, 130, 110, "", rounded=False, fill_color="#A8D1C8", stroke_color="#2B908F")
    rb.add_text(root, 1040, 295, "(b) 高度分解", width=180, height=24, font_size=16)
    rb.add_line(root, 1120, 255, 1175, 225, color="#C59D1C", width=2.0, end_arrow="classic")
    rb.add_line(root, 1120, 255, 1220, 195, color="#C59D1C", width=2.0, end_arrow="classic")
    rb.add_text(root, 1140, 230, "dbev (BEV plane)", width=180, height=24, font_size=14, font_color="#B8860B", align="left")

    rb.add_box(root, 930, 440, 470, 180, "", fill_color="#F5F5F5", stroke_color="#DDDDDD")
    rb.add_box(root, 975, 510, 150, 90, "", rounded=False, fill_color="#AFC4DA", stroke_color="#5C7EA3")
    rb.add_box(root, 1090, 445, 120, 130, "", rounded=False, fill_color="#A8D1C8", stroke_color="#2B908F")
    rb.add_text(root, 1075, 585, "(c) 重叠情况", width=220, height=24, font_size=16)
    rb.add_text(root, 1220, 515, "OBB 重叠时:\ndbev = 0", width=160, height=52, font_size=16, font_color="#8A4C7D")
    rb.add_line(root, 975, 598, 1355, 598, color="#CCCCCC", width=1.0)

    rb.add_box(root, 30, 650, 1370, 140, "dobb = √(d_bev^2 + d_z^2)\n反映实际间隙（如变道空间）， 非中心距离", fill_color="#F5F5F5", stroke_color="#D0D0D0", font_size=24)
    rb.add_text(root, 1120, 700, "dbev: BEV 多边形最小距离\ndz: 高度区间间距；重叠时为 0", width=240, height=60, font_size=14, align="left")

    return _finish(session, output_path)


def build_pgdg_tol_cn(output_path: Path, base_dir: Path):
    session = rb.new_session(1500, 900)
    root = session.root

    rb.add_box(root, 0, 0, 1500, 140, "", fill_color="#F8F8F8", stroke_color="none")
    rb.add_box(root, 0, 175, 1500, 230, "", fill_color="#E7F4EA", stroke_color="none")
    rb.add_box(root, 0, 410, 1500, 170, "", fill_color="#FAF1DA", stroke_color="none")
    rb.add_box(root, 0, 595, 1500, 200, "", fill_color="#F5E7F0", stroke_color="none")

    rb.add_text(root, 35, 35, "上下文层", width=50, height=90, font_size=20)
    rb.add_text(root, 35, 225, "感知层", width=50, height=90, font_size=20)
    rb.add_text(root, 35, 445, "推理层", width=50, height=90, font_size=20)
    rb.add_text(root, 35, 655, "规划层", width=50, height=90, font_size=20)
    rb.add_text(root, 1310, 18, "认知层级\n可观测 / 错配推理 / 推测性", width=150, height=70, font_size=12)

    c1 = rb.add_box(root, 480, 35, 170, 70, "C1\n场景描述", fill_color="#F8F8F8", stroke_color="#7A8190", font_size=22, bold=True)
    c2 = rb.add_box(root, 725, 35, 170, 70, "C2\n自车状态", fill_color="#F8F8F8", stroke_color="#7A8190", font_size=22, bold=True)

    q2 = rb.add_box(root, 90, 205, 165, 70, "Q2\n距离", fill_color="#EAF7F4", stroke_color="#2B908F", font_size=22, bold=True)
    q4 = rb.add_box(root, 285, 205, 165, 70, "Q4\n定位", fill_color="#EAF7F4", stroke_color="#2B908F", font_size=22, bold=True)
    q6 = rb.add_box(root, 480, 205, 165, 70, "Q6\n方位", fill_color="#EAF7F4", stroke_color="#2B908F", font_size=22, bold=True)
    l1 = rb.add_box(root, 675, 205, 165, 70, "L1\n空间关系", fill_color="#EAF7F4", stroke_color="#2B908F", font_size=22, bold=True)
    l5 = rb.add_box(root, 905, 205, 165, 70, "L5\n远近比较", fill_color="#EAF7F4", stroke_color="#2B908F", font_size=22, bold=True)
    s1 = rb.add_box(root, 1115, 205, 165, 70, "S1\n车辆状态", fill_color="#EAF7F4", stroke_color="#2B908F", font_size=22, bold=True)
    o1 = rb.add_box(root, 1310, 205, 165, 70, "O1\n车头朝向", fill_color="#EAF7F4", stroke_color="#2B908F", font_size=22, bold=True)
    q3 = rb.add_box(root, 145, 300, 165, 70, "Q3\n物体间距", fill_color="#EAF7F4", stroke_color="#2B908F", font_size=22, bold=True)
    l3 = rb.add_box(root, 390, 300, 165, 70, "L3\n比较", fill_color="#EAF7F4", stroke_color="#2B908F", font_size=22, bold=True)
    l4 = rb.add_box(root, 580, 300, 165, 70, "L4\n最高/最近", fill_color="#EAF7F4", stroke_color="#2B908F", font_size=22, bold=True)
    l7 = rb.add_box(root, 980, 300, 165, 70, "L7\n存在性", fill_color="#EAF7F4", stroke_color="#2B908F", font_size=22, bold=True)
    o2 = rb.add_box(root, 1265, 300, 165, 70, "O2\n同/反向", fill_color="#EAF7F4", stroke_color="#2B908F", font_size=22, bold=True)

    r3 = rb.add_box(root, 310, 455, 210, 80, "R3\n态势推理", fill_color="#FFF6DE", stroke_color="#D3A53C", font_size=24, bold=True)
    r7 = rb.add_box(root, 670, 455, 210, 80, "R7\n轨迹预测", fill_color="#FFF6DE", stroke_color="#D3A53C", font_size=24, bold=True)
    r0 = rb.add_box(root, 1135, 455, 210, 80, "R0\n综合推理", fill_color="#FFF6DE", stroke_color="#D3A53C", font_size=24, bold=True)

    p1 = rb.add_box(root, 660, 645, 200, 80, "P1\n决策规划", fill_color="#FCEBF5", stroke_color="#AA3C7A", font_size=24, bold=True)

    for source, target in [(c1, q6), (c2, l1), (q2, q3), (q4, r3), (q6, r3), (l1, r7), (l4, r7), (l5, r7), (s1, r0), (o1, o2), (o2, r0), (l7, r0), (r3, p1), (r7, p1), (r0, p1)]:
        rb.add_edge(root, source, target, color="#7A8190", width=1.2, end_arrow="classic", orthogonal=True)

    return _finish(session, output_path)


def build_pipeline_tol_cn(output_path: Path, base_dir: Path):
    session = rb.new_session(1700, 900)
    root = session.root

    input_box = rb.add_box(root, 30, 300, 250, 180, "NuScenes\n数据集\n三维标注·相机图像·\n自车位姿", fill_color="#F2F2F2", stroke_color="#666666", font_size=24, bold=True)
    stage1 = rb.add_box(root, 360, 120, 460, 210, "阶段一：场景图构建", fill_color="#E8F0FA", stroke_color="#4E7DA8", font_size=24, bold=True)
    s1a = rb.add_box(root, 400, 205, 110, 70, "NuScenes\nAPI", fill_color="#FFFFFF", stroke_color="#B0B0B0", font_size=18)
    s1b = rb.add_box(root, 540, 205, 140, 70, "三维标注提取", fill_color="#FFFFFF", stroke_color="#B0B0B0", font_size=18)
    s1c = rb.add_box(root, 705, 205, 100, 70, "自车位姿\n获取", fill_color="#FFFFFF", stroke_color="#B0B0B0", font_size=18)
    rb.add_text(root, 520, 285, "SceneGraphSample", width=220, height=24, font_size=14, font_color="#4E7DA8")

    stage2 = rb.add_box(root, 360, 365, 460, 190, "阶段二：投影与过滤", fill_color="#E4F5F3", stroke_color="#18A199", font_size=24, bold=True)
    s2a = rb.add_box(root, 390, 440, 135, 75, "三维到二维\n坐标变换", fill_color="#FFFFFF", stroke_color="#B0B0B0", font_size=18)
    s2b = rb.add_box(root, 545, 440, 135, 75, "可见性与\n深度过滤", fill_color="#FFFFFF", stroke_color="#B0B0B0", font_size=18)
    s2c = rb.add_box(root, 700, 440, 105, 75, "OBB 表面\n距离", fill_color="#FFFFFF", stroke_color="#B0B0B0", font_size=18)
    rb.add_text(root, 500, 525, "FrameAnnotation", width=200, height=24, font_size=14, font_color="#18A199")

    stage3 = rb.add_box(root, 910, 120, 250, 435, "阶段三：QA 图生成", fill_color="#FFF8E8", stroke_color="#D8A400", font_size=24, bold=True)
    rb.add_box(root, 955, 190, 165, 70, "SRE 编码", fill_color="#FFFFFF", stroke_color="#D0C8A0", font_size=18)
    rb.add_box(root, 955, 285, 165, 70, "PGDG 四层 DAG", fill_color="#FFFFFF", stroke_color="#D0C8A0", font_size=18)
    rb.add_box(root, 955, 380, 78, 70, "模板引擎", fill_color="#FFFFFF", stroke_color="#D0C8A0", font_size=18)
    rb.add_box(root, 1045, 380, 78, 70, "LLM", fill_color="#FFFFFF", stroke_color="#D0C8A0", font_size=18)
    rb.add_box(root, 955, 470, 165, 70, "混合答案生成", fill_color="#FFFFFF", stroke_color="#D0C8A0", font_size=18)
    rb.add_text(root, 985, 520, "QAGraph", width=120, height=24, font_size=14, font_color="#B18B00")

    stage4 = rb.add_box(root, 1215, 150, 220, 380, "阶段四：\n输出与增强", fill_color="#FBEAF1", stroke_color="#B04A7D", font_size=24, bold=True)
    rb.add_box(root, 1270, 225, 130, 70, "多轮对话格式化", fill_color="#FFFFFF", stroke_color="#D0B0C0", font_size=18)
    rb.add_box(root, 1270, 320, 130, 70, "依赖感知采样", fill_color="#FFFFFF", stroke_color="#D0B0C0", font_size=18)
    rb.add_box(root, 1270, 415, 130, 70, "质量验证", fill_color="#FFFFFF", stroke_color="#D0B0C0", font_size=18)
    rb.add_text(root, 1265, 500, "data.json", width=140, height=24, font_size=14, font_color="#8A4C7D")

    out_box = rb.add_box(root, 1470, 240, 180, 170, "结构化\nQA 数据\n13.27 万 QA 对 ·\n23 种类型 ·\n4 层认知", fill_color="#25354B", stroke_color="#25354B", font_size=22, font_color="#FFFFFF", bold=True)

    for source, target in [(input_box, stage1), (stage1, stage3), (stage2, stage3), (stage3, stage4), (stage4, out_box)]:
        rb.add_edge(root, source, target, color="#333333", width=2.0, end_arrow="classic")

    return _finish(session, output_path)


def build_sre_cn(output_path: Path, base_dir: Path):
    session = rb.new_session(1600, 900)
    root = session.root

    rb.add_text(root, 500, 20, "SRE 三段式输入架构", width=320, height=30, font_size=24, bold=True)
    rb.add_text(root, 300, 55, "DG2 系统通过三个互补输入通道编码空间信息，建立三重对齐", width=980, height=24, font_size=14)

    image_box = rb.add_box(root, 40, 155, 360, 270, "", fill_color="#E3E6EA", stroke_color="#D0D0D0")
    rb.add_box(root, 75, 220, 75, 95, "2", fill_color="#70C1B3", stroke_color="#2B7A78", font_size=20, bold=True)
    rb.add_box(root, 165, 210, 115, 80, "1", fill_color="#FFFFFF", stroke_color="#A0B6D0", font_size=24, bold=True)
    rb.add_box(root, 295, 170, 75, 55, "3", fill_color="#52677A", stroke_color="#D48A2A", font_size=22, font_color="#FFFFFF", bold=True)
    rb.add_text(root, 85, 460, "标注图像", width=120, height=28, font_size=20, bold=True)
    rb.add_text(root, 55, 500, "SRE 编码叠加于\n二维包围盒中心", width=180, height=52, font_size=16)

    spatial = rb.add_box(root, 560, 110, 420, 330, "<spatial_list>\n1. type: bounding_box\n   center: [8.3, -1.2, 0.5]\n   size: [4.0, 2.0, 1.5]\n2. type: cylinder\n   center: [3.5, -0.5, 0.9]\n3. type: bounding_box\n   center: [12.1, 2.8, 0.3]\n</spatial_list>", fill_color="#EEF4FB", stroke_color="#5C7EA3", font_size=16, align="left")
    rb.add_text(root, 640, 470, "空间参考列表", width=240, height=28, font_size=22, bold=True)
    rb.add_text(root, 630, 505, "自车坐标系下的\n三维几何参数", width=220, height=50, font_size=16)

    qa = rb.add_box(root, 1160, 150, 320, 240, "Q: 物体#1 距自车多远?\n\nA: 白色轿车是物体 1（中心: [8.3, -1.2, 0.5]）。\n距离车 8.3m， 方位: 右前方。", fill_color="#F8EAF1", stroke_color="#A27490", font_size=18, align="left")
    rb.add_text(root, 1210, 455, "自然语言 QA", width=220, height=28, font_size=22, bold=True)
    rb.add_text(root, 1180, 495, "完整绑定（首次提及）\n-> 紧凑引用", width=260, height=50, font_size=16)

    rb.add_edge(root, image_box, spatial, "编号 ↔ 坐标", color="#5C7EA3", width=2.0, end_arrow="classic")
    rb.add_edge(root, spatial, qa, "坐标 ↔ 语言", color="#5C7EA3", width=2.0, end_arrow="classic")
    rb.add_line(root, 80, 680, 1450, 680, color="#7FA0C3", width=2.0, start_arrow="classic", end_arrow="classic")
    rb.add_text(root, 480, 645, "三重对齐： 图像 ↔ 空间列表 ↔ 语言", width=520, height=28, font_size=18, bold=True)

    return _finish(session, output_path)


def build_teaser_tol_cn(output_path: Path, base_dir: Path):
    session = rb.new_session(1600, 900)
    root = session.root

    rb.add_text(root, 130, 30, "输入", width=120, height=30, font_size=22, bold=True)
    rb.add_text(root, 610, 30, "自动化处理", width=220, height=30, font_size=22, bold=True)
    rb.add_text(root, 1235, 30, "结构化输出", width=220, height=30, font_size=22, bold=True)

    input_box = rb.add_box(root, 35, 95, 320, 300, "NuScenes 数据集", fill_color="#F6F7F9", stroke_color="#7A8190", font_size=24, bold=True)
    rb.add_box(root, 70, 170, 250, 155, "", rounded=False, fill_color="#4F5D73", stroke_color="#4F5D73")
    rb.add_text(root, 55, 345, "850 scenes · 34k keyframes · 6 cameras", width=280, height=24, font_size=13)
    rb.add_text(root, 60, 420, "原始传感器数据 + 三维标注", width=260, height=26, font_size=16)

    pipeline = rb.add_box(root, 435, 95, 520, 300, "DG2 管线", fill_color="#EAF0F8", stroke_color="#4E7DA8", font_size=24, bold=True)
    sg = rb.add_box(root, 500, 215, 95, 90, "Scene\nGraph", fill_color="#FFFFFF", stroke_color="#4E7DA8", font_size=18)
    proj = rb.add_box(root, 630, 215, 120, 90, "3D->2D\nProjection", fill_color="#E4F5F3", stroke_color="#18A199", font_size=18)
    sre = rb.add_box(root, 785, 215, 110, 90, "SRE +\nPGDG", fill_color="#FFF8E8", stroke_color="#D8A400", font_size=18)
    outfmt = rb.add_box(root, 930, 215, 100, 90, "Output\nFormat", fill_color="#FBEAF1", stroke_color="#B04A7D", font_size=18)
    for source, target in [(sg, proj), (proj, sre), (sre, outfmt)]:
        rb.add_edge(root, source, target, color="#555555", width=1.5, end_arrow="classic")

    rb.add_box(root, 500, 450, 140, 90, "SRE:\nStructured\nspatial\nreferences", fill_color="#18A199", stroke_color="#18A199", font_size=18, font_color="#FFFFFF", bold=True)
    rb.add_box(root, 675, 450, 140, 90, "PGDG:\nCausal\ndependency\ngraph", fill_color="#D8A400", stroke_color="#D8A400", font_size=18, font_color="#FFFFFF", bold=True)
    rb.add_box(root, 850, 450, 145, 90, "Hybrid:\nTemplate +\nLLM generation", fill_color="#B04A7D", stroke_color="#B04A7D", font_size=18, font_color="#FFFFFF", bold=True)
    rb.add_line(root, 570, 448, 570, 395, color="#18A199", width=1.6, end_arrow="classic")
    rb.add_line(root, 745, 448, 820, 395, color="#D8A400", width=1.6, end_arrow="classic")
    rb.add_line(root, 920, 448, 980, 395, color="#B04A7D", width=1.6, end_arrow="classic")

    out1 = rb.add_box(root, 1135, 95, 345, 180, "PGDG", fill_color="#EAFBF7", stroke_color="#18A199", font_size=24, bold=True)
    rb.add_text(root, 1185, 170, "C1  Q2  L5  R3  P1", width=220, height=24, font_size=14)
    rb.add_text(root, 1170, 225, "四层认知 DAG 与依赖追踪", width=260, height=24, font_size=18)
    out2 = rb.add_box(root, 1135, 325, 345, 180, "结构化 QA", fill_color="#FFF8E8", stroke_color="#D8A400", font_size=24, bold=True)
    rb.add_text(root, 1160, 390, "Q: 物体#6 距自车多远?\nA: 物体#1 距 8.3m，方向: 右前方。风险: 中。", width=300, height=68, font_size=16, align="left")
    rb.add_text(root, 1160, 520, "13.2 万 QA 对 · 23 种类型", width=260, height=24, font_size=16)

    rb.add_edge(root, input_box, pipeline, color="#44546A", width=2.0, end_arrow="classic")
    rb.add_edge(root, pipeline, out1, color="#44546A", width=2.0, end_arrow="classic")
    rb.add_edge(root, pipeline, out2, color="#44546A", width=2.0, end_arrow="classic")
    rb.add_box(root, 0, 770, 1600, 60, "132,203 QA 对 | 23 种问题类型 | 4 层认知 | 全自动化生成", fill_color="#E4F5F3", stroke_color="none", font_size=22)

    return _finish(session, output_path)
