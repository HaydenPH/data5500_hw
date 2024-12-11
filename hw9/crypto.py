# Worked on this assigment with Sofia Perez and Jared Hougaard
import requests
import json
import time
import os
from datetime import datetime, timedelta
from itertools import permutations
from itertools import combinations

import networkx as nx
from networkx.classes.function import path_weight

import matplotlib.pyplot as plt

# define lists of crypto ID's and symbols
ids = ['ripple', 'cardano', 'bitcoin-cash', 'eos', 'litecoin', 'ethereum', 'bitcoin', 'polkadot', 'tron', 'avalanche', 'dogecoin', 'cronos', 'aptos']
currencies = ['xrp', 'ada', 'bch', 'eos', 'ltc', 'eth', 'btc', 'dot', 'trx', 'avax', 'doge', 'cro', 'apt']

g = nx.DiGraph() #Creates graph
edges = []

url = 'https://api.coingecko.com/api/v3/simple/price'
params = {
    'ids': ",".join(ids),
    'vs_currencies': ",".join(currencies)}

response = requests.get(url, params=params)
exchange_rates = response.json()

# loops through pairs of currencies to add edges
for c1, c2 in permutations(ids,2):
    print(c1,'to',c2)
    base_currency = currencies[ids.index(c1)]
    target_currency = currencies[ids.index(c2)]

    try:
        rate = exchange_rates[c1][target_currency]
        edges.append((c1,c2,rate))
    except:
        print("Can't convert currency")

g.add_weighted_edges_from(edges)

# Saving graph visualization as an image
curr_dir = os.path.dirname(__file__) # get the current directory of this file
graph_visual_fil = curr_dir + "/" + "currencies_graph_visual.png"

pos=nx.circular_layout(g) # pos = nx.nx_agraph.graphviz_layout(G)
nx.draw_networkx(g,pos)
labels = nx.get_edge_attributes(g,'weight')
nx.draw_networkx_edge_labels(g,pos,edge_labels=labels)
plt.savefig(graph_visual_fil)

# Function to calculate the weights
def calc_path_weight(graph, path):
    weight = 1
    for i in range(len(path)-1):
        weight *= graph[path[i]][path[i+1]]['weight']
    return weight

# makes a min and max number to compare to
min_arbitrage = float('inf')
max_arbitrage = -float('inf')
min_arbitrage_paths = []
max_arbitrage_paths = []

# Loop through all pairs of start and end nodes in the graph
for start, end in permutations(g.nodes, 2):
    forward_paths = list(nx.all_simple_paths(g, source=start, target=end))
    reverse_paths = list(nx.all_simple_paths(g, source=end, target=start))

    if not forward_paths or not reverse_paths: # skip if no path exists between node
        continue
#Calculate arbitrage factors for all forward and reverse path combos
    print(f'\nPaths from {start} to {end} ---------------------------')
    for fwd_path in forward_paths:
        forward_weight = calc_path_weight(g, fwd_path)
        for rev_path in reverse_paths:
            reverse_weight = calc_path_weight(g, rev_path)
            arbitrage = forward_weight * reverse_weight
            
            print(fwd_path, forward_weight)
            print(rev_path, reverse_weight)
            print(arbitrage)
# update minimum and maximum arbitrage factor and their paths
            if arbitrage < min_arbitrage:
                min_arbitrage = arbitrage
                min_arbitrage_paths = [fwd_path, rev_path]
            elif arbitrage > max_arbitrage:
                max_arbitrage = arbitrage
                max_arbitrage_paths = [fwd_path, rev_path]
# Print results for smallest and largest factor 
print(f'\nSmallest Paths Weight Factor: {min_arbitrage}')
print(f'Paths: {min_arbitrage_paths[0]}, {min_arbitrage_paths[1]}')

print(f'\nGreatest Paths Weight Factor: {min_arbitrage}')
print(f'Paths: {max_arbitrage_paths[0]}, {max_arbitrage_paths[1]}')

