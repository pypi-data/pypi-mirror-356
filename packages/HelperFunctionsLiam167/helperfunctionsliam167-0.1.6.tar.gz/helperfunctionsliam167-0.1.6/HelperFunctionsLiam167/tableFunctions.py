import ipywidgets as widgets
from IPython.display import HTML, display, clear_output

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


def df_styled(
    df,
    max_rows: int = 100,
    float_fmt: str = "{:,.2f}",
    int_fmt: str   = "{:,}"
):
    """
    Render `df.head(max_rows)` as a Tailwind-CSS table card.
    """
    # Take a slice
    df2 = df.head(max_rows)

    # Start building HTML
    html = """
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
<div class="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg m-10">
  <table class="min-w-full divide-y divide-gray-200">
    <thead class="bg-blue-500">
      <tr>
    """
    # headers
    for col in df2.columns:
        html += f'''
        <th scope="col"
            class="px-6 py-3 text-left text-xs text-white uppercase tracking-wider font-bold">
          {col}
        </th>'''
    html += """
      </tr>
    </thead>
    <tbody class="bg-white divide-y divide-gray-200">
    """

    # rows
    for _, row in df2.iterrows():
        html += '<tr class="hover:bg-gray-100">'
        for v in row:
            if isinstance(v, float):
                cell = float_fmt.format(v)
            elif isinstance(v, int):
                cell = int_fmt.format(v)
            else:
                cell = v
            html += f'''
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
            {cell}
          </td>'''
        html += "</tr>"
    html += """
    </tbody>
  </table>
</div>
"""
    display(HTML(html))
