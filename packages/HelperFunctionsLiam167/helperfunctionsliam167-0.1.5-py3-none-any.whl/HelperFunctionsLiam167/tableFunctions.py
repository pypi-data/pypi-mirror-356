import ipywidgets as widgets
from IPython.display import display, clear_output

def show_df_toggle(df, button_text_open="Show dataframe", button_text_close="Hide dataframe", button_style="info"):
    out = widgets.Output()
    btn = widgets.ToggleButton(
        description=button_text_open,
        icon="table",
        value=False,
        button_style=button_style
    )

    def on_toggle(change):
        with out:
            out.clear_output()
            if btn.value:
                display(df)
                btn.description = button_text_close
            else:
                btn.description = button_text_open

    btn.observe(on_toggle, 'value')
    display(widgets.VBox([btn, out]))