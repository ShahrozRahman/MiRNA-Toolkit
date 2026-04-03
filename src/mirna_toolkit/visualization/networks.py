from typing import Any

import networkx as nx
import plotly.graph_objects as go


def plot_mirna_targets(mirna_id: str, targets: list[dict[str, Any]]) -> go.Figure:
    graph = nx.Graph()
    graph.add_node(mirna_id, kind="mirna")

    for row in targets:
        gene = str(row.get("gene") or row.get("target") or row.get("symbol") or "")
        if gene:
            graph.add_node(gene, kind="gene")
            graph.add_edge(mirna_id, gene)

    pos = nx.spring_layout(graph, seed=42)
    edge_x, edge_y = [], []
    for source, target in graph.edges():
        x0, y0 = pos[source]
        x1, y1 = pos[target]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    node_x, node_y, text = [], [], []
    for node in graph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        text.append(node)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode="lines", line=dict(width=1), hoverinfo="none"))
    fig.add_trace(
        go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            text=text,
            textposition="top center",
            marker=dict(size=12),
            hoverinfo="text",
        )
    )
    fig.update_layout(title=f"miRNA-target network: {mirna_id}", template="plotly_white")
    return fig


def plot_mirna_disease_network(edges: list[tuple[str, str]]) -> go.Figure:
    graph = nx.Graph()
    graph.add_edges_from(edges)

    pos = nx.spring_layout(graph, seed=42)
    edge_x, edge_y = [], []
    for source, target in graph.edges():
        x0, y0 = pos[source]
        x1, y1 = pos[target]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    node_x, node_y, text = [], [], []
    for node in graph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        text.append(node)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode="lines", line=dict(width=1), hoverinfo="none"))
    fig.add_trace(
        go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            text=text,
            textposition="top center",
            marker=dict(size=10),
            hoverinfo="text",
        )
    )
    fig.update_layout(title="miRNA-disease network", template="plotly_white")
    return fig
