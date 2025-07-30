# @title
# 🎨 Plotly Config with Excel Export Only

import os, json, pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import ipywidgets as widgets
from IPython.display import display, clear_output
from google.colab import files


# --------------------
# CONFIGURATION SETUP 
# --------------------

CONFIG_PATH = '/content/plot_config.json'
DEFAULT_CONFIG = {
    "template": "plotly_white",
    "max_width": 1200,
    "fallback": "#007bff",
    "domain_map": {"VirginBet": "#ff0000","LiveScoreBetUK":"#ffa200","LiveScoreBetIE":"#004cff","LiveScoreBetBG":"#8000ff","LiveScoreBetNG":"#00ad0c"}
}

def load_config(path=CONFIG_PATH, defaults=DEFAULT_CONFIG):
    if os.path.exists(path):
        try:
            with open(path, 'r') as f: return json.load(f)
        except Exception: pass
    with open(path, 'w') as f:
        json.dump(defaults, f, indent=2)
    return defaults.copy()

def save_config(cfg): 
    with open(CONFIG_PATH, 'w') as f: json.dump(cfg, f, indent=2)

def get_plotly_config():
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    cfg['domain_map'] = {k.lower(): v for k, v in cfg.get('domain_map', {}).items()}
    return cfg

# --------------------
# FEATURE - CONFIG CARD
# --------------------

config = load_config()
template_widget = widgets.Dropdown(
    options=["plotly", "plotly_white", "plotly_dark", "presentation", "simple_white", "ggplot2", "seaborn"],
    value=config.get("template", DEFAULT_CONFIG["template"]),
    description="Template:", layout=widgets.Layout(width='290px')
)
width_widget = widgets.BoundedIntText(
    value=config.get("max_width", DEFAULT_CONFIG["max_width"]), min=400, max=2400, step=50,
    description="Plot Width:", layout=widgets.Layout(width='200px')
)
fallback_widget = widgets.ColorPicker(
    value=config.get("fallback", DEFAULT_CONFIG["fallback"]),
    description="Fallback:", layout=widgets.Layout(width='200px')
)

def make_domain_row(domain, color):
    name_widget = widgets.Text(value=domain, layout=widgets.Layout(width='120px'))
    color_widget = widgets.ColorPicker(value=color, layout=widgets.Layout(width='80px'))
    remove_btn = widgets.Button(icon='trash', layout=widgets.Layout(width='32px'))
    row = widgets.HBox([name_widget, color_widget, remove_btn])
    remove_btn.on_click(lambda _: domain_colors_box.children.remove(row))
    return row

domain_colors_box = widgets.VBox([
    make_domain_row(dom, col) for dom, col in config.get("domain_map", {}).items()
])
add_domain_btn = widgets.Button(description="Add Domain", icon='plus')
def add_domain_row_callback(_):
    domain_colors_box.children = domain_colors_box.children + (make_domain_row("new_domain", "#222222"),)

add_domain_btn.on_click(add_domain_row_callback)

def get_domain_map():
    return {row.children[0].value.strip().lower(): row.children[1].value
            for row in domain_colors_box.children if row.children[0].value.strip()}

out = widgets.Output()
def on_save(_):
    config['template'] = template_widget.value
    config['max_width'] = width_widget.value
    config['fallback'] = fallback_widget.value
    config['domain_map'] = get_domain_map()
    save_config(config)
    with out: clear_output(); print("✅ Config saved!")
    import builtins
    builtins.cfg = get_plotly_config()
    pio.templates.default = builtins.cfg["template"]

save_btn = widgets.Button(description="💾 Save Config", button_style="primary")
save_btn.on_click(on_save)

config_card = widgets.VBox([
    widgets.HTML("<b>Plotly Settings</b>"),
    template_widget, width_widget, fallback_widget,
    widgets.HTML("<b>Domain Colors</b>"), domain_colors_box,
    add_domain_btn, save_btn, out
], layout=widgets.Layout(border="1px solid #e0e0e0", border_radius="10px", padding="20px", width="370px"))

import builtins
builtins.cfg = get_plotly_config()
pio.templates.default = builtins.cfg["template"]


# ------------------
# FEATURE - EXCEL DOWNLOAD BUTTON 
# ------------------
# ========= colour & luminance helpers =================================
from matplotlib.colors import to_rgb, to_hex
def _adjust_lightness(hex_col, factor=1.0):
    r, g, b = to_rgb(hex_col)
    return to_hex((min(r * factor, 1), min(g * factor, 1), min(b * factor, 1)))

def hex_to_rgb_string(hex_color: str) -> str:
    hex_color = hex_color.lstrip("#")
    return "#{:02X}{:02X}{:02X}".format(
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16),
    )

# ========= Excel exporter =============================================
import pandas as pd, io, itertools, builtins

def _unique_in_order(arr):
    seen, out = set(), []
    for v in arr:
        if v not in seen:
            out.append(v); seen.add(v)
    return out

def dataframe_to_excel_with_colors(
    df, x, y_metrics, *,
    group=None, stack_by=None,
    labels=None, kind="bar",
    title_prefix="", x_title="", legend_title="", cfg=None,
):
    """
    Handles *all* combos, inc. x==group.  When both `group` and `stack_by`
    are given it builds a two-level column header (group, segment) so each
    domain-tier pair becomes its own series and keeps the right colour.
    """

    metrics = [y_metrics] if isinstance(y_metrics, str) else list(y_metrics)
    labels  = labels or {m: m for m in metrics}
    cfg     = cfg or builtins.cfg

    with pd.ExcelWriter(io.BytesIO(), engine="xlsxwriter") as writer:
        for metric in metrics:

            # ---------- build the pivot table --------------------------------
            if group and stack_by:                       # ⇢ 2-level header
                if group == x:                           # avoid duplication
                    alias = f"__{group}__for_cols"
                    df_   = df.assign(**{alias: df[group]})
                    pivot = df_.pivot_table(
                        index=x,
                        columns=[stack_by],
                        values=metric,
                        aggfunc="sum",
                    )
                    def colour_for(col_key, row_domain):
                      base = cfg["domain_map"].get(str(row_domain).lower(), cfg["fallback"])
                      factor = 0.6 + 0.4 * (list(pivot.columns).index(col_key) % 4)
                      return _adjust_lightness(base, factor)
                else:
                    pivot = df.pivot_table(
                        index=x, columns=[group, stack_by],
                        values=metric, aggfunc="sum",
                    )

            elif group:                                  # ⇢ single-level cols
                if group == x:                           # same trick as above
                    alias = f"__{group}__for_cols"
                    df_   = df.assign(**{alias: df[group]})
                    pivot = df_.pivot_table(
                        index=x, columns=alias, values=metric, aggfunc="sum"
                    )
                else:
                    pivot = df.pivot_table(
                        index=x, columns=group, values=metric, aggfunc="sum"
                    )

            else:                                        # ⇢ no columns split
                pivot = df.set_index(x)[[metric]]

            sheet = str(labels[metric])[:31]             # Excel tab ≤ 31 chars
            pivot.to_excel(writer, sheet_name=sheet)
            ws    = writer.sheets[sheet]

            # ---------- colour lookup helpers -------------------------------
            segments = _unique_in_order(df[stack_by].dropna()) if stack_by else []
            seg_pos  = {s: i for i, s in enumerate(segments)}
            groups   = _unique_in_order(df[group]) if group else []

            def colour_for(col_key):
                """col_key = scalar or (group, segment) tuple."""
                g = col_key[0] if isinstance(col_key, tuple) else col_key
                s = col_key[1] if isinstance(col_key, tuple) and stack_by else None
                base = cfg["domain_map"].get(str(g).lower(), cfg["fallback"])
                if s is not None:                        # shade by segment
                    factor = 0.6 + 0.4 * (seg_pos[s] % 4)
                    return _adjust_lightness(base, factor)
                return base

            # ---------- header cell styling ---------------------------------
            for col_idx, col_key in enumerate(pivot.columns, start=1):
                rgb = hex_to_rgb_string(colour_for(col_key))
                fmt = writer.book.add_format({"bg_color": rgb, "bold": True})
                label = " – ".join(map(str, col_key)) if isinstance(col_key, tuple) else str(col_key)
                ws.write(0, col_idx, label, fmt)

            # ---------- embed the chart -------------------------------------
            n_rows       = len(pivot)
            chart_kwargs = {"type": "line"} if kind == "line" else {
                "type": "column",
                "subtype": "stacked" if stack_by else "clustered",
            }
            chart = writer.book.add_chart(chart_kwargs)

            for col_idx, col_key in enumerate(pivot.columns):
                rgb = hex_to_rgb_string(colour_for(col_key))
                series = {
                    "name":       [sheet, 0, col_idx + 1],
                    "categories": [sheet, 1, 0, n_rows, 0],
                    "values":     [sheet, 1, col_idx + 1, n_rows, col_idx + 1],
                    "fill":       {"color": rgb},
                }
                if kind == "line":
                    series["line"] = {"color": rgb}
                chart.add_series(series)

            chart.set_title({"name": f"{labels[metric]} by {x}"})
            chart.set_x_axis({"name": x_title or x})
            chart.set_y_axis({"name": labels[metric]})
            chart.set_legend({"position": "bottom"})
            ws.insert_chart(2, len(pivot.columns) + 3, chart)

        buf = writer.book.filename
    buf.seek(0)
    return buf

# ========= button wrapper ============================================
def add_excel_download_button(
    df, x, y_metrics, *, group=None, stack_by=None,
    labels=None, kind="bar",
    title_prefix="", x_title="", legend_title="", cfg=None,
):
    """
    Shows a “⬇️ Download as Excel” button that mirrors the current chart.
    """
    import ipywidgets as widgets
    from IPython.display import display
    try:
        from google.colab import files   # Colab
    except ImportError:
        import ipywidgets as files       # dummy shim for Jupyter

    def _on_click(_):
        buf = dataframe_to_excel_with_colors(
            df, x, y_metrics,
            group=group, stack_by=stack_by,
            labels=labels, kind=kind,
            title_prefix=title_prefix, x_title=x_title,
            legend_title=legend_title, cfg=cfg,
        )
        fname = (title_prefix or "chart").replace(" ", "_").lower() + ".xlsx"
        with open(fname, "wb") as f:
            f.write(buf.read())
        files.download(fname)

    btn = widgets.Button(description="⬇️ Download as Excel")
    btn.on_click(_on_click)
    display(btn)



# ------------------
# FINAL PLOTLY RENDER 
# -------------------
from matplotlib.colors import to_rgb, to_hex
import plotly.graph_objects as go
import plotly.express as px        # used only for its built-in colour lists
import builtins

# ── helper ─────────────────────────────────────────────────────────────
def _adjust_lightness(hex_col, factor=1.0):
    r, g, b = to_rgb(hex_col)
    return to_hex((min(r * factor, 1), min(g * factor, 1), min(b * factor, 1)))

# ── flexible plot function ─────────────────────────────────────────────
def plotly_group_dropdown(
    df,
    x,
    y_metrics,
    *,                    # all remaining args are keyword-only
    group=None,           # primary split – optional
    stack_by=None,        # secondary split for stacked bars – optional
    labels=None,
    kind="bar",           # "bar"  ▸ grouped / stacked
                          # "line" ▸ separate traces
    title_prefix="",
    x_title="",
    legend_title="",
    show_dropdown=True,   # turn metric selector on / off
    show=True,            # auto-render
):
    """
    One function ≈ three chart types:
      • plain time-series / bar chart          (no group, no stack)
      • small-multiple style by *group*        (group, no stack)
      • stacked-bar split by *stack_by*        (stack_by, bar mode)
      • any combo of the above with a metric selector

    Parameters
    ----------
    df : DataFrame
    x  : column to plot on X-axis
    y_metrics : str | list[str]
        1 + numeric columns.  If more than one and *show_dropdown* is True,
        a dropdown appears that toggles each metric.
    group : str | None
        Primary grouping column (shown as separate bars/lines or bar clusters).
    stack_by : str | None
        Categorical column to stack on (only makes sense for kind="bar").
    show_dropdown : bool
        Force the dropdown on/off regardless of how many metrics were passed.
    """

    cfg = builtins.cfg               # global Plotly config from template.py
    metrics = [y_metrics] if isinstance(y_metrics, str) else list(y_metrics)
    labels = labels or {m: m for m in metrics}

    # ── categories ────────────────────────────────────────────────────
    groups   = df[group].unique()     if group     else [None]
    segments = df[stack_by].unique()  if stack_by  else [None]

    # ── palette: flexible variant shading or px colours ───────────────
    pal = {}
    if stack_by:
        # Each *group* keeps its base colour (from cfg['domain_map'] or fallback).
        # We then lighten / darken that base per *segment* index.
        for gi, g in enumerate(groups):
            base = cfg["domain_map"].get(str(g).lower(), cfg["fallback"])
            for si, s in enumerate(segments):
                # factor cycles around 0.6 → 1.0 → 1.4 ...
                factor = 0.6 + 0.4 * (si % 4)
                pal[(g, s)] = _adjust_lightness(base, factor)
    else:
        # No stacking – fall back to regular group colours
        for g in groups:
            pal[(g, None)] = cfg["domain_map"].get(str(g).lower(),
                                                   cfg["fallback"])

    # ── build traces ──────────────────────────────────────────────────
    fig = go.Figure()

    for m_idx, metric in enumerate(metrics):
        for g in groups:
            for s in segments:
                mask = True
                if group:    mask &= df[group]     == g
                if stack_by: mask &= df[stack_by]  == s
                sub = df[mask]
                if sub.empty:
                    continue

                trace = dict(
                    x=sub[x], y=sub[metric],
                    name=" – ".join([str(v) for v in (g, s) if v is not None]),
                    marker_color=pal[(g, s)],
                    visible=(m_idx == 0),          # only first metric on
                    showlegend=(m_idx == 0),
                )
                if kind == "bar":
                    fig.add_trace(go.Bar(**trace))
                elif kind == "line":
                    fig.add_trace(go.Scatter(mode="lines+markers", **trace))

    # ── dropdown (metric selector) ─────────────────────────────────────
    make_dropdown = show_dropdown and len(metrics) > 1
    if make_dropdown:
        n_traces_per_metric = len(fig.data) // len(metrics)
        buttons = []
        for m_idx, metric in enumerate(metrics):
            vis = [False] * len(fig.data)
            start = m_idx * n_traces_per_metric
            vis[start : start + n_traces_per_metric] = [True] * n_traces_per_metric
            buttons.append(
                dict(
                    label=labels[metric],
                    method="update",
                    args=[
                        {"visible": vis},
                        {"title": f"{title_prefix}{labels[metric]}",
                         "yaxis": {"title": labels[metric]}},
                    ],
                )
            )
        fig.update_layout(
            updatemenus=[dict(active=0, buttons=buttons,
                              x=1.05, y=0.5, xanchor="left", yanchor="middle")]
        )

    # ── layout / styling ──────────────────────────────────────────────
    y0 = labels[metrics[0]]
    fig.update_layout(
        title=f"{title_prefix}{y0}",
        xaxis_title=x_title,
        yaxis_title=y0,
        barmode=("stack" if stack_by and kind == "bar"
                 else "group" if kind == "bar" and group else None),
        legend_title=legend_title,
        template=cfg["template"],
        width=cfg["max_width"],
        margin=dict(l=20, r=20, t=50, b=20),
    )

    if show:
        fig.show(config=dict(responsive=True, displayModeBar=True))
# ... inside your new plotly_group_dropdown, just *before* the final `return fig`
    add_excel_download_button(
        df, x, y_metrics,
        group=group, stack_by=stack_by,
        labels=labels, kind=kind,
        title_prefix=title_prefix, x_title=x_title,
        legend_title=legend_title, cfg=cfg,
    )
    return fig

