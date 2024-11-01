import networkx as nx

def count_high_degree_nodes(graph):
    high_degree_nodes = [node for node in graph.nodes if graph.degree(node) > 5]
    return len(high_degree_nodes)

G = nx.Graph()
G.add_nodes_from([1,2,3,4,5])
G.add_edges_from([(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(2,3),(2,4),(2,5),(2,6)])

print("number of nodes with degree > 5:", count_high_degree_nodes(G))