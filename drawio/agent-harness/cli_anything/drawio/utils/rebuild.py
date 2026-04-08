"""Helpers for rebuilding editable draw.io figures from explicit specs."""

from __future__ import annotations

import base64
import html
import mimetypes
from pathlib import Path
from typing import Iterable
from urllib.parse import quote

from ..core.session import Session
from . import drawio_xml


DEFAULT_FONT_FAMILY = "Songti SC"


def default_text_style(
    font_size: int = 12,
    font_color: str = "#000000",
    bold: bool = False,
    italic: bool = False,
    align: str = "center",
    vertical_align: str = "middle",
) -> dict[str, str]:
    font_style = 0
    if bold:
        font_style |= 1
    if italic:
        font_style |= 2
    style = {
        "fontFamily": DEFAULT_FONT_FAMILY,
        "fontSize": str(font_size),
        "fontColor": font_color,
        "align": align,
        "verticalAlign": vertical_align,
        "whiteSpace": "wrap",
        "html": "1",
    }
    if font_style:
        style["fontStyle"] = str(font_style)
    return style


def normalize_label(label: str) -> str:
    return html.escape(label).replace("\n", "<br>")


def format_label(label: str, raw_html: bool = False) -> str:
    if raw_html:
        return label.replace("\n", "<br>")
    return normalize_label(label)


def _coerce_style_value(value) -> str:
    if isinstance(value, bool):
        return "1" if value else "0"
    return str(value)


def merge_style(base_style: str = "", **props) -> str:
    style = drawio_xml.parse_style(base_style)
    for key, value in props.items():
        if value is None:
            continue
        style[key] = _coerce_style_value(value)
    return drawio_xml.build_style(style)


def apply_style(cell, **props) -> None:
    for key, value in props.items():
        if value is None:
            continue
        drawio_xml.set_style_property(cell, key, _coerce_style_value(value))


def apply_text_style(cell, **props) -> None:
    apply_style(cell, **default_text_style(**props))


def new_session(page_width: int, page_height: int) -> Session:
    session = Session()
    session.new_project(page_width=page_width, page_height=page_height)
    return session


def save_session(session: Session, output_path: str | Path) -> str:
    return session.save_project(str(output_path))


def add_shape(
    mxfile,
    base_style: str,
    x: float,
    y: float,
    width: float,
    height: float,
    label: str = "",
    *,
    raw_html: bool = False,
    **style_props,
) -> str:
    style = merge_style(base_style, **default_text_style(), **style_props)
    return drawio_xml.add_vertex(
        mxfile,
        style,
        x,
        y,
        width,
        height,
        format_label(label, raw_html=raw_html),
    )


def add_box(
    mxfile,
    x: float,
    y: float,
    width: float,
    height: float,
    label: str = "",
    *,
    rounded: bool = True,
    fill_color: str = "#F5F5F5",
    stroke_color: str = "#666666",
    stroke_width: float = 1.0,
    font_size: int = 12,
    font_color: str = "#000000",
    bold: bool = False,
    align: str = "center",
    vertical_align: str = "middle",
    dashed: bool = False,
    opacity: int | None = None,
    raw_html: bool = False,
) -> str:
    base = drawio_xml.SHAPE_STYLES["rounded" if rounded else "rectangle"]
    style = merge_style(
        base,
        fillColor=fill_color,
        strokeColor=stroke_color,
        strokeWidth=stroke_width,
        dashed=dashed,
        opacity=opacity,
        **default_text_style(
            font_size=font_size,
            font_color=font_color,
            bold=bold,
            align=align,
            vertical_align=vertical_align,
        ),
    )
    return drawio_xml.add_vertex(mxfile, style, x, y, width, height, format_label(label, raw_html=raw_html))


def add_text(
    mxfile,
    x: float,
    y: float,
    label: str,
    *,
    width: float = 160,
    height: float = 32,
    font_size: int = 12,
    bold: bool = False,
    font_color: str = "#000000",
    align: str = "center",
    raw_html: bool = False,
) -> str:
    style = merge_style(
        drawio_xml.SHAPE_STYLES["text"],
        strokeColor="none",
        fillColor="none",
        resizable=0,
        **default_text_style(
            font_size=font_size,
            font_color=font_color,
            bold=bold,
            align=align,
        ),
    )
    return drawio_xml.add_vertex(mxfile, style, x, y, width, height, format_label(label, raw_html=raw_html))


def add_ellipse(
    mxfile,
    x: float,
    y: float,
    width: float,
    height: float,
    label: str = "",
    *,
    fill_color: str = "#FFFFFF",
    stroke_color: str = "#666666",
    font_size: int = 12,
    bold: bool = False,
    raw_html: bool = False,
) -> str:
    style = merge_style(
        drawio_xml.SHAPE_STYLES["ellipse"],
        fillColor=fill_color,
        strokeColor=stroke_color,
        strokeWidth=1.0,
        **default_text_style(font_size=font_size, bold=bold),
    )
    return drawio_xml.add_vertex(mxfile, style, x, y, width, height, format_label(label, raw_html=raw_html))


def add_diamond(
    mxfile,
    x: float,
    y: float,
    width: float,
    height: float,
    label: str = "",
    *,
    fill_color: str = "#FFFFFF",
    stroke_color: str = "#666666",
    font_size: int = 12,
    bold: bool = False,
    raw_html: bool = False,
) -> str:
    style = merge_style(
        drawio_xml.SHAPE_STYLES["diamond"],
        fillColor=fill_color,
        strokeColor=stroke_color,
        strokeWidth=1.0,
        **default_text_style(font_size=font_size, bold=bold),
    )
    return drawio_xml.add_vertex(mxfile, style, x, y, width, height, format_label(label, raw_html=raw_html))


def add_point(mxfile, x: float, y: float, size: float = 4.0) -> str:
    style = merge_style(
        drawio_xml.SHAPE_STYLES["ellipse"],
        fillColor="none",
        strokeColor="none",
        resizable=0,
        movable=1,
        deletable=1,
        rotatable=0,
        **default_text_style(font_size=1),
    )
    return drawio_xml.add_vertex(mxfile, style, x, y, size, size, "")


def add_image(
    mxfile,
    x: float,
    y: float,
    width: float,
    height: float,
    image_path: str | Path,
    *,
    stroke_color: str = "#000000",
    stroke_width: float = 1.0,
    opacity: int | None = None,
    rounded: bool = False,
) -> str:
    image_path = Path(image_path)
    mime_type, _ = mimetypes.guess_type(str(image_path))
    if mime_type is None:
        mime_type = "application/octet-stream"
    image_b64 = base64.b64encode(image_path.read_bytes()).decode("ascii")
    data_uri = f"data:{mime_type};base64,{image_b64}"
    style = merge_style(
        "shape=image;html=1;imageAspect=0;aspect=fixed;",
        image=quote(data_uri, safe=":/,="),
        strokeColor=stroke_color,
        strokeWidth=stroke_width,
        opacity=opacity,
        rounded=rounded,
        **default_text_style(),
    )
    return drawio_xml.add_vertex(mxfile, style, x, y, width, height, "")


def add_edge(
    mxfile,
    source_id: str,
    target_id: str,
    label: str = "",
    *,
    color: str = "#666666",
    width: float = 1.0,
    dashed: bool = False,
    orthogonal: bool = False,
    curved: bool = False,
    end_arrow: str = "classic",
    start_arrow: str = "none",
    font_size: int = 10,
    font_color: str = "#000000",
    raw_html: bool = False,
) -> str:
    if curved:
        base_style = drawio_xml.EDGE_STYLES["curved"]
    elif orthogonal:
        base_style = drawio_xml.EDGE_STYLES["orthogonal"]
    else:
        base_style = drawio_xml.EDGE_STYLES["straight"]
    style = merge_style(
        base_style,
        strokeColor=color,
        strokeWidth=width,
        dashed=dashed,
        endArrow=end_arrow,
        startArrow=start_arrow,
        rounded=0,
        **default_text_style(font_size=font_size, font_color=font_color),
    )
    return drawio_xml.add_edge(mxfile, source_id, target_id, style, format_label(label, raw_html=raw_html))


def add_line(
    mxfile,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    *,
    color: str = "#666666",
    width: float = 1.0,
    dashed: bool = False,
    end_arrow: str = "none",
    start_arrow: str = "none",
) -> str:
    p1 = add_point(mxfile, x1, y1, size=0.1)
    p2 = add_point(mxfile, x2, y2, size=0.1)
    return add_edge(
        mxfile,
        p1,
        p2,
        color=color,
        width=width,
        dashed=dashed,
        end_arrow=end_arrow,
        start_arrow=start_arrow,
    )


def add_polyline(
    mxfile,
    points: Iterable[tuple[float, float]],
    *,
    color: str = "#666666",
    width: float = 1.0,
    dashed: bool = False,
) -> list[str]:
    point_ids = [add_point(mxfile, x, y, size=0.1) for x, y in points]
    edges: list[str] = []
    for source_id, target_id in zip(point_ids, point_ids[1:]):
        edges.append(
            add_edge(
                mxfile,
                source_id,
                target_id,
                color=color,
                width=width,
                dashed=dashed,
                end_arrow="none",
                start_arrow="none",
            )
        )
    return edges


def add_frame(
    mxfile,
    x: float,
    y: float,
    width: float,
    height: float,
    *,
    stroke_color: str = "#C0392B",
    fill_color: str = "none",
    dashed: bool = True,
    rounded: bool = True,
    label: str | None = None,
    label_x: float | None = None,
    label_y: float | None = None,
    font_size: int = 14,
) -> str:
    frame_id = add_box(
        mxfile,
        x,
        y,
        width,
        height,
        "",
        rounded=rounded,
        fill_color=fill_color,
        stroke_color=stroke_color,
        dashed=dashed,
        stroke_width=1.4,
    )
    if label:
        add_text(
            mxfile,
            label_x if label_x is not None else x + width / 2 - 120,
            label_y if label_y is not None else y - 34,
            label,
            width=240,
            height=28,
            font_size=font_size,
            bold=True,
        )
    return frame_id


def add_prism(
    mxfile,
    x: float,
    y: float,
    width: float,
    height: float,
    dx: float,
    dy: float,
    *,
    fill_color: str,
    stroke_color: str,
) -> list[str]:
    ids = []
    ids.append(add_box(mxfile, x, y, width, height, "", rounded=False, fill_color=fill_color, stroke_color=stroke_color))
    ids.append(add_box(mxfile, x + dx, y - dy, width, height, "", rounded=False, fill_color=fill_color, stroke_color=stroke_color))
    ids.append(add_line(mxfile, x, y, x + dx, y - dy, color=stroke_color))
    ids.append(add_line(mxfile, x + width, y, x + dx + width, y - dy, color=stroke_color))
    ids.append(add_line(mxfile, x, y + height, x + dx, y - dy + height, color=stroke_color))
    ids.append(add_line(mxfile, x + width, y + height, x + dx + width, y - dy + height, color=stroke_color))
    return ids


def iter_user_cells(mxfile):
    yield from drawio_xml.get_all_cells(mxfile)


def build_smoke_diagram():
    session = new_session(400, 240)
    root = session.root
    a = add_box(root, 20, 30, 120, 50, "A")
    b = add_box(root, 220, 30, 120, 50, "B")
    add_edge(root, a, b, "连接")
    return root
