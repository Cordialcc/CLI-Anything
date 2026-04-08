"""Target inventory for editable figure rebuilds."""

from .ch3_specs import (
    build_obb_cn,
    build_pgdg_tol_cn,
    build_pipeline_tol_cn,
    build_sre_cn,
    build_teaser_tol_cn,
)
from .ch4_generators import (
    build_fig1_teaser,
    build_fig2_architecture,
    build_fig3_backprojection_h,
    build_fig4_waterfall,
    build_fig6_perturbation,
    build_fig7_selectivity,
    build_fig8_params,
    build_fig9_gate_gradient,
)


TARGETS = {
    "ch3/obb_cn": {"subdir": "ch3", "stem": "obb_cn", "builder": build_obb_cn},
    "ch3/pgdg_tol_cn": {"subdir": "ch3", "stem": "pgdg_tol_cn", "builder": build_pgdg_tol_cn},
    "ch3/pipeline_tol_cn": {"subdir": "ch3", "stem": "pipeline_tol_cn", "builder": build_pipeline_tol_cn},
    "ch3/sre_cn": {"subdir": "ch3", "stem": "sre_cn", "builder": build_sre_cn},
    "ch3/teaser_tol_cn": {"subdir": "ch3", "stem": "teaser_tol_cn", "builder": build_teaser_tol_cn},
    "ch4/fig1_teaser": {"subdir": "ch4", "stem": "fig1_teaser", "builder": build_fig1_teaser},
    "ch4/fig2_architecture": {"subdir": "ch4", "stem": "fig2_architecture", "builder": build_fig2_architecture},
    "ch4/fig3_backprojection_h": {"subdir": "ch4", "stem": "fig3_backprojection_h", "builder": build_fig3_backprojection_h},
    "ch4/fig4_waterfall": {"subdir": "ch4", "stem": "fig4_waterfall", "builder": build_fig4_waterfall},
    "ch4/fig6_perturbation": {"subdir": "ch4", "stem": "fig6_perturbation", "builder": build_fig6_perturbation},
    "ch4/fig7_selectivity": {"subdir": "ch4", "stem": "fig7_selectivity", "builder": build_fig7_selectivity},
    "ch4/fig8_params": {"subdir": "ch4", "stem": "fig8_params", "builder": build_fig8_params},
    "ch4/fig9_gate_gradient": {"subdir": "ch4", "stem": "fig9_gate_gradient", "builder": build_fig9_gate_gradient},
}
