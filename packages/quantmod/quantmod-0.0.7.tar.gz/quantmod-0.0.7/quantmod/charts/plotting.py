"""
quantmod.charts.plotting

Interactive Plotting Utilities for Quantmod

Usage Notes:
- In **Jupyter notebooks**, interactive plots display inline automatically when you call `df.iplot(...)`.
- In **Python scripts**, interactive plots open in your default web browser. For best results, set:
    import plotly.io as pio
    pio.renderers.default = "browser"
    fig = df.iplot(...)
    fig.show()
- In **headless environments** (e.g., servers), save plots to HTML files:
    fig = df.iplot(...)
    fig.write_html("plot.html")
    print("Plot saved to plot.html. Open this file in your browser to view the plot.")

Available Chart Types:
- "line": Line chart
- "scatter": Scatter plot
- "ohlc": OHLC (Open-High-Low-Close) chart
- "candlestick": Candlestick chart
- "subplots": Multiple line charts as subplots
- "histogram": Histogram of daily returns
- "bar": Bar chart
- "heatmap": Heatmap
- "box": Box plot
- "pie": Pie chart
- "treemap": Treemap chart
- "overlay": Overlay multiple series with secondary y-axis
- "normalized": Normalized line chart (base=100)

"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express.colors as pc
from plotly.subplots import make_subplots
import plotly.io as pio
from .themes import THEMES, COLOR_SCALES, create_template

# Set global Plotly theme and dimensions
# pio.templates["pearl"] = create_pearl_template()
# pio.templates.default = "pearl"
# DEFAULT_THEME = "pearl"

# Register all available themes
for theme_name in THEMES.keys():
    pio.templates[theme_name] = create_template(theme_name)

# Set default template
pio.templates.default = "pearl"

DEFAULT_THEME = "pearl"
DEFAULT_WIDTH = 1000
DEFAULT_HEIGHT = 600


# Main plot dispatcher
def _iplot(self, kind="line", **kwargs):
    if kind == "normalized":
        return _plot_normalized(self, **kwargs)
    if kind == "overlay":
        return _plot_overlay(self, **kwargs)
    if isinstance(self, pd.Series):
        df = self.to_frame()
    else:
        df = self.copy()

    # Create a lowercase column mapping
    colmap = {col.lower(): col for col in df.columns}

    if kind == "line":
        fig = _plot_line(df, **kwargs)
    elif kind == "scatter":
        fig = _plot_scatter(df, **kwargs)
    elif kind == "ohlc":
        fig = _plot_ohlc(df, colmap, **kwargs)
    elif kind == "candlestick":
        fig = _plot_candlestick(df, colmap, **kwargs)
    elif kind == "subplots":
        fig = _plot_subplots(df, **kwargs)
    elif kind == "histogram":
        fig = _plot_histogram(df, **kwargs)
    elif kind == "bar":
        fig = _plot_bar(df, **kwargs)
    elif kind == "heatmap":
        fig = _plot_heatmap(df, **kwargs)
    elif kind == "box":
        fig = _plot_box(df, **kwargs)
    elif kind == "pie":
        fig = _plot_pie(df, **kwargs)
    elif kind == "treemap":
        fig = _plot_treemap(df, **kwargs)
    else:
        raise ValueError(f"Plot type '{kind}' not supported.")

    return fig


def _get_colors(theme_name):
    """Get colors for the specified theme - FIXED"""
    colorscale_name = THEMES.get(theme_name, {}).get("colorscale", "original")
    colors = COLOR_SCALES.get(colorscale_name, COLOR_SCALES["original"])
    return colors


def _plot_line(df, x=None, y=None, **kwargs):
    theme_name = kwargs.get("theme", DEFAULT_THEME)
    colors = _get_colors(theme_name)

    trace_kwargs = {}
    if "color" in kwargs:
        trace_kwargs["line"] = {"color": kwargs.pop("color")}
    else:
        # Use theme colors if no specific color provided
        trace_kwargs["line"] = {"color": colors[0]}

    for k in ["line", "name", "hoverinfo", "opacity"]:
        if k in kwargs:
            if k == "line" and "line" in trace_kwargs:
                trace_kwargs["line"].update(kwargs.pop(k))
            else:
                trace_kwargs[k] = kwargs.pop(k)

    x_data = df.index if x is None else df[x]
    y_data = df[y] if isinstance(y, str) else df.iloc[:, 0]

    fig = go.Figure(
        go.Scatter(x=x_data, y=y_data, mode="lines", name="", **trace_kwargs)
    )
    _update_layout(fig, kwargs, default_title="Stock Prices", yaxis_title="")
    return fig


def _plot_scatter(df, x=None, y=None, **kwargs):
    theme_name = kwargs.get("theme", DEFAULT_THEME)
    colors = _get_colors(theme_name)

    trace_kwargs = {}
    if "color" in kwargs:
        trace_kwargs["marker"] = {"color": kwargs.pop("color")}
    else:
        trace_kwargs["marker"] = {"color": colors[0]}

    for k in ["marker", "line", "name", "hoverinfo", "opacity"]:
        if k in kwargs:
            if k == "marker" and "marker" in trace_kwargs:
                trace_kwargs["marker"].update(kwargs.pop(k))
            else:
                trace_kwargs[k] = kwargs.pop(k)

    x_data = df.index if x is None else df[x]
    y_data = df[y] if isinstance(y, str) else df.iloc[:, 0]

    fig = go.Figure(
        go.Scatter(x=x_data, y=y_data, mode="markers", name="", **trace_kwargs)
    )
    _update_layout(fig, kwargs, default_title="Scatter Plot", yaxis_title="")
    return fig


def _plot_ohlc(df, colmap, **kwargs):
    # df = df[-30:] if len(df) > 30 else df
    fig = go.Figure(
        go.Ohlc(
            x=df.index,
            open=df[colmap.get("open")],
            high=df[colmap.get("high")],
            low=df[colmap.get("low")],
            close=df[colmap.get("close")],
            name="",
        )
    )
    _update_layout(fig, kwargs, default_title="OHLC Chart", yaxis_title="")
    return fig


def _plot_candlestick(df, colmap, **kwargs):
    # df = df[-30:] if len(df) > 30 else df
    fig = go.Figure(
        go.Candlestick(
            x=df.index,
            open=df[colmap.get("open")],
            high=df[colmap.get("high")],
            low=df[colmap.get("low")],
            close=df[colmap.get("close")],
            name="",
        )
    )
    _update_layout(fig, kwargs, default_title="Candlestick Chart", yaxis_title="")
    return fig


def _plot_subplots(df, cols=None, **kwargs):
    ncols = kwargs.pop("ncols", 2)
    shared_yaxes = kwargs.pop("shared_yaxes", False)
    theme_name = kwargs.get("theme", DEFAULT_THEME)
    colors = _get_colors(theme_name)

    cols = df.columns if cols is None else cols
    n = len(cols)
    rows = (n - 1) // ncols + 1
    fig = make_subplots(rows=rows, cols=ncols, shared_yaxes=shared_yaxes)

    for i, col in enumerate(cols):
        r, c = divmod(i, ncols)
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df[col],
                mode="lines",
                name=col,
                line=dict(color=colors[i % len(colors)]),
            ),
            row=r + 1,
            col=c + 1,
        )
    _update_layout(fig, kwargs, default_title="Subplots", yaxis_title="")
    return fig


def _plot_histogram(df, columns=None, **kwargs):
    overlap = kwargs.pop("overlap", True)
    ncols = kwargs.pop("ncols", 2)
    shared_yaxes = kwargs.pop("shared_yaxes", False)
    theme_name = kwargs.get("theme", DEFAULT_THEME)
    colors = _get_colors(theme_name)

    columns = df.columns if columns is None else columns

    if overlap:
        fig = go.Figure()
        for i, col in enumerate(columns):
            fig.add_trace(
                go.Histogram(
                    x=df[col] * 100,
                    nbinsx=kwargs.get("nbinsx", 50),
                    name=col,
                    opacity=0.75,
                    marker_color=colors[i % len(colors)],
                )
            )
    else:
        rows = (len(columns) - 1) // ncols + 1
        fig = make_subplots(rows=rows, cols=ncols, shared_yaxes=shared_yaxes)
        for i, col in enumerate(columns):
            r, c = divmod(i, ncols)
            fig.add_trace(
                go.Histogram(
                    x=df[col] * 100,
                    nbinsx=kwargs.get("nbinsx", 50),
                    name=col,
                    opacity=0.75,
                    marker_color=colors[i % len(colors)],
                ),
                row=r + 1,
                col=c + 1,
            )

    _update_layout(
        fig,
        kwargs,
        default_title="Histogram of Daily Returns",
        xaxis_title="",
        yaxis_title="Frequency",
    )
    return fig


def _plot_bar(df, x=None, y=None, scale=False, **kwargs):
    if scale:
        df = df * 100

    theme_name = kwargs.get("theme", DEFAULT_THEME)
    colors = kwargs.pop("colors", _get_colors(theme_name))
    fig = go.Figure()

    if df.shape[0] == 1:  # single-row DataFrame
        y_vals = df.iloc[0] if y is None else df[y]
        x_vals = df.columns if x is None else x
        for i, (xi, yi) in enumerate(zip(x_vals, y_vals)):
            fig.add_trace(
                go.Bar(
                    x=[xi], y=[yi], name=str(xi), marker_color=colors[i % len(colors)]
                )
            )
    else:  # multi-row DataFrame — use index as x, columns as series
        columns_to_plot = (
            df.columns if y is None else ([y] if isinstance(y, str) else y)
        )
        for i, col in enumerate(columns_to_plot):
            fig.add_trace(
                go.Bar(
                    x=df.index,
                    y=df[col],
                    name=col,
                    marker_color=colors[i % len(colors)],
                )
            )

    _update_layout(fig, kwargs, default_title="Bar Chart", yaxis_title="")
    return fig


def _plot_heatmap(df, matrix=False, **kwargs):
    colorscale = kwargs.pop("colorscale", "Viridis")
    if matrix:
        cols = df.columns
        n = len(cols)
        rows = (n - 1) // 2 + 1
        fig = make_subplots(rows=rows, cols=2)
        for i, col in enumerate(cols):
            r, c = divmod(i, 2)
            fig.add_trace(
                go.Heatmap(
                    z=df[[col]].values, x=[col], y=df.index, colorscale=colorscale
                ),
                row=r + 1,
                col=c + 1,
            )
    else:
        fig = go.Figure(
            data=go.Heatmap(
                z=df.values, x=df.columns, y=df.index, colorscale=colorscale
            )
        )
    _update_layout(fig, kwargs, default_title="Heatmap", xaxis_title="", yaxis_title="")
    return fig


def _plot_box(df, columns=None, **kwargs):
    columns = df.columns if columns is None else columns
    theme_name = kwargs.get("theme", DEFAULT_THEME)
    colors = _get_colors(theme_name)

    fig = go.Figure()
    for i, col in enumerate(columns):
        fig.add_trace(go.Box(y=df[col], name=col, marker_color=colors[i % len(colors)]))
    _update_layout(
        fig, kwargs, default_title="Box Plot", xaxis_title="", yaxis_title=""
    )
    return fig


def _plot_pie(df, names=None, values=None, **kwargs):
    theme_name = kwargs.get("theme", DEFAULT_THEME)
    colors = _get_colors(theme_name)

    names_data = df.index if names is None else df[names]
    values_data = df.iloc[:, 0] if values is None else df[values]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=names_data,
                values=values_data,
                marker_colors=colors[: len(names_data)],
            )
        ]
    )
    _update_layout(fig, kwargs, default_title="Pie Chart")
    return fig


def _plot_overlay(df, secondary_y=None, **kwargs):
    theme_name = kwargs.get("theme", DEFAULT_THEME)
    colors = _get_colors(theme_name)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    cols = df.columns
    for i, col in enumerate(cols):
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df[col],
                mode="lines",
                name=col,
                line=dict(color=colors[i % len(colors)]),
            ),
            secondary_y=(col == secondary_y),
        )
    _update_layout(fig, kwargs, default_title="Overlay Chart", yaxis_title="")
    return fig


def _plot_normalized(df, **kwargs):
    theme_name = kwargs.get("theme", DEFAULT_THEME)
    colors = _get_colors(theme_name)

    norm_df = (df / df.iloc[0]) * 100
    fig = go.Figure()
    for i, col in enumerate(norm_df.columns):
        fig.add_trace(
            go.Scatter(
                x=norm_df.index,
                y=norm_df[col],
                mode="lines",
                name=col,
                line=dict(color=colors[i % len(colors)]),
            )
        )
    _update_layout(
        fig,
        kwargs,
        default_title="Normalized Prices",
        yaxis_title="Normalized (Base = 100)",
    )
    return fig


def _plot_treemap(df, path=None, values=None, labels=None, parents=None, **kwargs):
    if path is not None:
        df = df.copy()
        for p in path:
            if p not in df.columns:
                raise ValueError(f"Column '{p}' not in DataFrame")
        labels = df[path[-1]]
        parents = df[path[-2]] if len(path) > 1 else [""] * len(df)
        values = df[values or df.columns[0]]
    elif labels is not None and parents is not None and values is not None:
        labels = df[labels] if isinstance(labels, str) else labels
        parents = df[parents] if isinstance(parents, str) else parents
        values = df[values] if isinstance(values, str) else values
    else:
        raise ValueError(
            "Must provide either 'path' or all of 'labels', 'parents', and 'values'"
        )

    fig = go.Figure(
        go.Treemap(
            labels=labels,
            parents=parents,
            values=values,
            hoverinfo="label+value+percent parent",
            marker=dict(colors=_get_colors(DEFAULT_THEME)),
        )
    )

    _update_layout(fig, kwargs, default_title="Treemap")
    return fig


def _update_layout(fig, user_kwargs, default_title="", xaxis_title="", yaxis_title=""):
    theme_name = user_kwargs.pop("theme", DEFAULT_THEME)
    theme_layout = THEMES.get(theme_name, {}).get("layout", {})

    layout_defaults = dict(
        title=default_title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        width=user_kwargs.pop("width", DEFAULT_WIDTH),
        height=user_kwargs.pop("height", DEFAULT_HEIGHT),
        showlegend=user_kwargs.pop("showlegend", False),
    )
    layout_defaults.update(theme_layout)
    layout_defaults.update(user_kwargs)  # allow override
    fig.update_layout(**layout_defaults)


# Attach iplot method to both DataFrame and Series
pd.DataFrame.iplot = _iplot
pd.Series.iplot = _iplot
