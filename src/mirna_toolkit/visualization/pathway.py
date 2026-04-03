import pandas as pd
import plotly.express as px


def pathway_enrichment_bar(
    enrichment_df: pd.DataFrame,
    pathway_col: str = "pathway",
    score_col: str = "score",
):
    fig = px.bar(enrichment_df.sort_values(score_col, ascending=False), x=score_col, y=pathway_col, orientation="h")
    fig.update_layout(title="Pathway Enrichment", template="plotly_white")
    return fig
