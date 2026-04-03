import pandas as pd
import plotly.express as px


def expression_heatmap(expression: pd.DataFrame, title: str = "miRNA Expression Heatmap"):
    fig = px.imshow(expression, aspect="auto", color_continuous_scale="Viridis", title=title)
    fig.update_layout(template="plotly_white")
    return fig
