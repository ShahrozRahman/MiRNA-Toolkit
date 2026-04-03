import pandas as pd
import plotly.express as px


def volcano_plot(
    de_results: pd.DataFrame,
    log2fc_col: str = "log2FoldChange",
    pvalue_col: str = "pvalue",
    label_col: str = "feature",
):
    data = de_results.copy()
    data["neg_log10_p"] = -(data[pvalue_col].clip(lower=1e-300)).map(lambda x: __import__("math").log10(x))
    fig = px.scatter(data, x=log2fc_col, y="neg_log10_p", hover_name=label_col, template="plotly_white")
    fig.update_layout(title="Volcano Plot", xaxis_title="log2 Fold Change", yaxis_title="-log10(p-value)")
    return fig
