import networkx as nx

def count_nodes(graph):
    return graph.number_of_nodes()

G = nx.Graph()
G.add_nodes_from([1,2,3,4,5])
print(count_nodes(G))