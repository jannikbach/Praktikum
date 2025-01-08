import networkx as nx
from xxhash import xxh64


# invariant
def wl_init(graph) -> None:
    weisfeiler_lehmann_init(graph, node_attr=["element", "charge"], edge_attr=["order"])


# invariant
def wl_step(graph) -> None:
    weisfeiler_lehmann_step(graph)


def weisfeiler_lehmann_init(graph: nx.Graph, node_attr: list[str], edge_attr: list[str]):
    """
    The first iteration step that uses node/edge attributes to create hashes.
    Adds the "hash" attribute to each node.
    """
    new_hashes = {}  # store hashes for the next iteration (don't override the current ones)

    for node, node_data in graph.nodes(data=True):
        d = {
            _node_label(node_data, node_attr): 0
        }
        for neighbor in graph.neighbors(node):
            label = _get_initial_neighbor_label(graph, node, neighbor, node_attr, edge_attr)
            if label not in d:
                d[label] = 1
            else:
                d[label] += 1
        new_hashes[node] = _hash_dict(d)

    # replace all hashes with the new hashes
    for node, node_hash in new_hashes.items():
        graph.nodes[node]["hash"] = node_hash


def weisfeiler_lehmann_step(graph: nx.Graph):
    new_hashes = {}  # store hashes for the next iteration (don't override the current ones)

    for node, node_data in graph.nodes(data=True):
        d = {
            node_data["hash"]: 0
        }
        for neighbor in graph.neighbors(node):
            label = graph.nodes[neighbor]["hash"]
            if label not in d:
                d[label] = 1
            else:
                d[label] += 1
        new_hashes[node] = _hash_dict(d)

    # replace all hashes with the new hashes
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


def _node_label(node, node_attrs):
    return ",".join(sorted([str(node[a]) for a in node_attrs]))


def _edge_label(edge, edge_attrs):
    return ",".join(sorted([str(edge[a]) for a in edge_attrs]))


def _get_initial_neighbor_label(graph: nx.Graph, from_node, to_node, node_attr, edge_attr) -> str:
    node = graph.nodes[to_node]
    edge = graph.edges[from_node, to_node]

    node_label = _node_label(node, node_attr)
    edge_label = _edge_label(edge, edge_attr)

    return f"{node_label}_{edge_label}"


def _hash_dict(d: dict) -> int:
    fst = lambda x: x[0]  # for the functional bros
    s = str(sorted(d.items(), key=fst))
    return xxh64(s.encode()).intdigest()
