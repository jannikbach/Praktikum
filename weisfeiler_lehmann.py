import json
import networkx as nx
from xxhash import xxh64


def weisfeiler_lehmann_init(graph: nx.Graph, node_attr:list[str], edge_attr:list[str]):
    """
    The first iteration step that uses node/edge attributes to create hashes.
    Adds the "hash" attribute to each node.
    """
    hashes = {}

    for node, node_data in graph.nodes(data=True):
        d = {}
        for neighbor in graph.neighbors(node):
            label = _get_initial_neighbor_label(graph, node, neighbor, node_attr, edge_attr)
            if label not in d:
                d[label] = 1
            else:
                d[label] += 1
        hashes[node] = _hash_dict(d)

    for node, hash in hashes.items():
        graph.nodes[node]["hash"] = hash

def weisfeiler_lehmann_step(graph: nx.Graph):
    new_hashes = {}

    for node, node_data in graph.nodes(data=True):
        d = {}
        # do we neet to put the node hash in the dict?
        d[node_data["hash"]] = 1
        for neighbor in graph.neighbors(node):
            label = graph.nodes[neighbor]["hash"]
            if label not in d:
                d[label] = 1
            else:
                d[label] += 1
        new_hashes[node] = _hash_dict(d)

    for node, new_hash in new_hashes.items():
        graph.nodes[node]["hash"] = new_hash


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

    node_label = ",".join(sorted([str(node[a]) for a in node_attr]))
    edge_label = ",".join(sorted([str(edge[a]) for a in edge_attr]))

    return f"{node_label}_{edge_label}"


def _hash_dict(d: dict) -> int:
    return xxh64(json.dumps(d, sort_keys=True).encode()).intdigest()

