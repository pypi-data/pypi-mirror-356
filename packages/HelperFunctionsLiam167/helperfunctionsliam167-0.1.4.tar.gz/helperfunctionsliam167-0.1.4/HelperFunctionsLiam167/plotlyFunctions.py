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
    "domain_map": {"sent": "#636EFA", "click": "#EF553B", "control_group": "#00CC96"}
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

display(config_card)
import builtins
builtins.cfg = get_plotly_config()
pio.templates.default = builtins.cfg["template"]


# ------------------
# FEATURE - EXCEL DOWNLOAD BUTTON 
# ------------------

def hex_to_rgb_string(hex_color):
    hex_color = hex_color.lstrip("#")
    return '#{:02X}{:02X}{:02X}'.format(
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16)
    )

def dataframe_to_excel_with_colors(
    df, x, y_metrics, group=None, labels=None, kind='bar', title_prefix='', x_title='', legend_title='', cfg=None
):
    """Exports dataframe as a styled Excel with chart for each metric."""
    metrics = [y_metrics] if isinstance(y_metrics, str) else y_metrics
    labels = labels or {m: m for m in metrics}
    cfg = cfg or builtins.cfg
    import io
    with pd.ExcelWriter(io.BytesIO(), engine='xlsxwriter') as writer:
        for metric in metrics:
            if group:
                pivot = df.pivot_table(index=x, columns=group, values=metric)
                group_names = list(pivot.columns)
            else:
                pivot = df.set_index(x)[[metric]]
                group_names = [metric]
            sheetname = str(labels[metric])
            pivot.to_excel(writer, sheet_name=sheetname)
            worksheet = writer.sheets[sheetname]
            for col_idx, col_name in enumerate(group_names, start=1):
                col_hex = cfg["domain_map"].get(str(col_name).lower(), cfg["fallback"])
                fmt = writer.book.add_format({'bg_color': hex_to_rgb_string(col_hex), 'bold': True})
                worksheet.write(0, col_idx, col_name, fmt)
            chart_type = 'column' if kind == 'bar' else 'line'
            chart = writer.book.add_chart({'type': chart_type})
            n_rows = len(pivot)
            for col_idx, col_name in enumerate(group_names):
                col_hex = cfg["domain_map"].get(str(col_name).lower(), cfg["fallback"])
                rgb = hex_to_rgb_string(col_hex)
                series = {
                    'name':       [sheetname, 0, col_idx+1],
                    'categories': [sheetname, 1, 0, n_rows, 0],
                    'values':     [sheetname, 1, col_idx+1, n_rows, col_idx+1],
                    'fill':       {'color': rgb},
                }
                if chart_type == 'line': series['line'] = {'color': rgb}
                chart.add_series(series)
            chart.set_title({'name': f'{labels[metric]} by {x}'})
            chart.set_x_axis({'name': x_title or x})
            chart.set_y_axis({'name': labels[metric]})
            chart.set_legend({'position': 'bottom'})
            worksheet.insert_chart(2, len(group_names) + 3, chart)
        excel_buffer = writer.book.filename
    excel_buffer.seek(0)
    return excel_buffer

def add_excel_download_button(
    df, x, y_metrics, group=None, labels=None, kind='bar', title_prefix='', x_title='', legend_title='', cfg=None
):
    """Adds an Excel download button below a plot."""
    def on_download_excel_clicked(_):
        buf = dataframe_to_excel_with_colors(
            df, x, y_metrics, group, labels, kind, title_prefix, x_title, legend_title, cfg
        )
        fname = f"{title_prefix.replace(' ', '_').lower()}chart.xlsx"
        with open(fname, "wb") as f:
            f.write(buf.read())
        files.download(fname)
    btn = widgets.Button(description="⬇️ Download as Excel")
    btn.on_click(on_download_excel_clicked)
    display(btn)

# ------------------
# FINAL PLOTLY RENDER 
# -------------------
def plotly_group_dropdown(
    df, x, y_metrics, group, labels=None, kind='bar',
    title_prefix='', x_title='', legend_title='', show=True
):
    cfg = builtins.cfg
    fig = go.Figure()
    metrics = [y_metrics] if isinstance(y_metrics, str) else y_metrics
    labels = labels or {m: m for m in metrics}
    groups = df[group].unique()
    for metric_idx, metric in enumerate(metrics):
        for g in groups:
            sub = df[df[group] == g]
            trace_args = dict(
                x=sub[x], y=sub[metric], name=str(g),
                marker_color=cfg["domain_map"].get(str(g).lower(), cfg["fallback"]),
                visible=(metric_idx == 0), showlegend=(metric_idx == 0)
            )
            if kind == 'bar': fig.add_trace(go.Bar(**trace_args))
            elif kind == 'line': fig.add_trace(go.Scatter(mode='lines+markers', **trace_args))
    if len(metrics) > 1:
        n_groups, n_metrics = len(groups), len(metrics)
        buttons = []
        for metric_idx, metric in enumerate(metrics):
            visibility = [False]*(n_groups*n_metrics)
            for group_idx in range(n_groups):
                visibility[metric_idx*n_groups + group_idx] = True
            showlegend = [v for v in visibility]
            buttons.append(dict(
                label=labels[metric], method="update",
                args=[{"visible": visibility, "showlegend": showlegend},
                      {"title": f"{title_prefix}{labels[metric]}", "yaxis": {"title": labels[metric]}}]
            ))
        fig.update_layout(
            updatemenus=[dict(active=0, buttons=buttons, x=1.1, y=0.7, xanchor='center', yanchor='top')],
            title=f"{title_prefix}{labels[metrics[0]]}",
            xaxis_title=x_title, yaxis_title=labels[metrics[0]],
            barmode='group' if kind == 'bar' else None,
            legend_title=legend_title, template=cfg["template"],
            width=cfg["max_width"], autosize=True,
            margin=dict(l=20, r=20, t=50, b=20)
        )
    else:
        fig.update_layout(
            title=f"{title_prefix}{labels[metrics[0]]}",
            xaxis_title=x_title, yaxis_title=labels[metrics[0]],
            barmode='group' if kind == 'bar' else None,
            legend_title=legend_title, template=cfg["template"],
            width=cfg["max_width"], autosize=True,
            margin=dict(l=20, r=20, t=50, b=20)
        )
    fig.update_layout(autosize=True, margin=dict(l=20, r=20, t=50, b=20))
    if show: fig.show(config=dict(responsive=True, displayModeBar=True))
    add_excel_download_button(df, x, y_metrics, group, labels, kind, title_prefix, x_title, legend_title, cfg)
    return fig
