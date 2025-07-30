import networkx as nx
import networkx.algorithms.community as nx_comm
import metis
from typing import List, Set
from hdh.hdh import HDH

def compute_cut(hdh: HDH, num_parts: int) -> List[Set[str]]:
    """
    Use METIS to partition HDH nodes into disjoint blocks.
    
    Returns a list of disjoint sets of node IDs.
    """
    # 1. Build undirected graph from HDH
    G = nx.Graph()
    G.add_nodes_from(hdh.S)
    
    for edge in hdh.C:
        edge_nodes = list(edge)
        for i in range(len(edge_nodes)):
            for j in range(i + 1, len(edge_nodes)):
                G.add_edge(edge_nodes[i], edge_nodes[j])

    # 2. Convert to METIS-compatible graph (requires contiguous integer node IDs)
    node_list = list(G.nodes)
    node_idx_map = {node: idx for idx, node in enumerate(node_list)}
    idx_node_map = {idx: node for node, idx in node_idx_map.items()}

    metis_graph = nx.relabel_nodes(G, node_idx_map, copy=True)
    
    # 3. Call METIS
    _, parts = metis.part_graph(metis_graph, nparts=num_parts)
    
    # 4. Build partition sets
    partition = [set() for _ in range(num_parts)]
    for idx, part in enumerate(parts):
        node_id = idx_node_map[idx]
        partition[part].add(node_id)
    
    return partition
