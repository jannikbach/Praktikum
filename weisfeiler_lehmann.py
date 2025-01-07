import json
import networkx as nx
from xxhash import xxh64


def weisfeiler_lehmann_init(graph: nx.Graph, node_attr:list[str], edge_attr:list[str]):
    """
    The first iteration step that uses node/edge attributes to create hashes.
    Adds the "hash" attribute to each node.
    """
    for node, node_data in graph.nodes(data=True):
        d = {}
        for neighbor in graph.neighbors(node):
            label = _get_initial_neighbor_label(graph, node, neighbor, node_attr, edge_attr)
            if label not in d:
                d[label] = 1
            else:
                d[label] += 1
        node_data["hash"] = _hash_dict(d)


def weisfeiler_lehmann_step(graph: nx.Graph):
    for node, node_data in graph.nodes(data=True):
        d = {}
        for neighbor in graph.neighbors(node):
            label = graph.nodes[neighbor]["hash"]
            if label not in d:
                d[label] = 1
            else:
                d[label] += 1
        node_data["hash"] = _hash_dict(d)


def hash_graph(graph: nx.Graph) -> int:
    d = {}
    for node, node_data in graph.nodes(data=True):
        label = node_data["hash"]
        if label not in d:
            d[label] = 1
        else:
            d[label] += 1
    return _hash_dict(d)


def _get_initial_neighbor_label(graph: nx.Graph, from_node, to_node, node_attr, edge_attr) -> str:
    node = graph.nodes[to_node]
    edge = graph.edges[from_node, to_node]

    node_label = ",".join([str(node[a]) for a in node_attr])
    edge_label = ",".join([str(edge[a]) for a in edge_attr])

    return f"{node_label}_{edge_label}"


def _hash_dict(d: dict) -> int:
    return xxh64(json.dumps(d, sort_keys=True).encode()).intdigest()
