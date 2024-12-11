# I worked on this with Sofia Perez and Jared Hougaard
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

import alpaca_trade_api as tradeapi 

#Connect to API for paper trading
api_key = 'PKDBWC6OV2ZGX5SFFKO5'
api_secret = 'Xs9zNWqcjsXHqp4s7esD7w7hmgd4uIhUW4SpmIez'
base_url = 'https://paper-api.alpaca.markets'

api = tradeapi.REST(api_key, api_secret, base_url, api_version = 'v2')


ids = ['maker','bitcoin-cash','chainlink','polkadot','ethereum','bitcoin']
currencies = ['mkr','bch','link','dot','eth','btc']

g =  nx.DiGraph()
edges = []

# Define CoinGecko API URL with multiple IDs and currencies
url = "https://api.coingecko.com/api/v3/simple/price"
params = {
    "ids": ",".join(ids),
    "vs_currencies": ",".join(currencies)}

# gets all exchange rates at once
response = requests.get(url, params=params)
exchange_rates = response.json()


def save_currency_pair_data(currency_from, currency_to, exchange_rate):
    if not os.path.exists("data"):
        os.makedirs("data")

    timestamp = datetime.now().strftime("%Y.%m.%d:%H.%M")
    filename = f"data/currency_pair_{currency_from}_{currency_to}_{timestamp}.txt"

    with open(filename, 'w') as file:
        file.write(f"currency_from, currency_to, exchange_rate\n")
        file.write(f"{currency_from}, {currency_to}, {exchange_rate}\n")
    print(f"Saved data for {currency_from} to {currency_to} at {timestamp}.")


#adding edges to the graph
for c1, c2 in permutations(ids,2):
    print(c1, 'to', c2)
    base_currency = currencies[ids.index(c1)]
    target_currency = currencies[ids.index(c2)]
    
    try:
        rate = exchange_rates[c1][target_currency]
        edges.append((c1,c2,rate))
        save_currency_pair_data(base_currency, target_currency,rate)
    except:
        print("Can't convert currency")

g.add_weighted_edges_from(edges)

#Saving Graph Visual
curr_dir = os.path.dirname(__file__) # get the current directory of this file
graph_visual_fil = curr_dir + "/" + "currencies_graph_visual.png"

pos=nx.circular_layout(g) # pos = nx.nx_agraph.graphviz_layout(G)
nx.draw_networkx(g,pos)
labels = nx.get_edge_attributes(g,'weight')
nx.draw_networkx_edge_labels(g,pos,edge_labels=labels)

plt.savefig(graph_visual_fil)

#creates a function to calculate the weights
def calc_path_weight(graph, path):
    weight = 1
    for i in range(len(path)-1):
        weight *= graph[path[i]][path[i+1]]['weight']
    return weight

#defines a function to place a paper trade order
def place_trade(symbol, side):
    api.submit_order(
        symbol=symbol.upper(),
        qty=1,
        side=side,
        type='market',
        time_in_force='gtc'
    )
    print(f'Placed {side} order of {symbol}')
    
# Store the results in a JSON file
def save_results_to_json(results):
    base_directory = "/Users/haydenhatch/data5500/final_project"
    # Create the directory if it doesn't exist
    if not os.path.exists(base_directory):
        os.makedirs(base_directory)
    filename = os.path.join(base_directory,'results.json')
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            existing_results = json.load(f)
    else:
        existing_results = []

    existing_results.append(results)
    
    with open(filename, 'w') as f:
        json.dump(existing_results, f, indent=4)

min_arbitrage = float('inf') #creates a min number to compare to which is infinity
max_arbitrage = -float('inf') #creates a max number to compare to which is -infinity
min_arbitrage_paths = []
max_arbitrage_paths = []
results = []

#loops through every node in the graph
for start, end in permutations(g.nodes, 2):
    #finds all paths going from start to finish and back
    forward_paths = list(nx.all_simple_paths(g, source=start, target=end))
    reverse_paths = list(nx.all_simple_paths(g, source=end, target=start))

    if not forward_paths or not reverse_paths:
        continue
    
    best_arbitrage = -float('inf')
    best_forward_path = None
    best_reverse_path = None

    #finds the weight of each forward path
    for fwd_path in forward_paths:
        forward_weight = calc_path_weight(g, fwd_path)

        #finds the weight of each reverse path
        for rev_path in reverse_paths:
            reverse_weight = calc_path_weight(g, rev_path)
            #multiplies the forward and reverse weight to find the arbitrage factor
            arbitrage = forward_weight * reverse_weight

            #keeps track of the max and min arbitrage factors
            if arbitrage > best_arbitrage:
                best_arbitrage = arbitrage
                best_forward_path = fwd_path
                best_reverse_path = rev_path

    if best_arbitrage > 1:
        print(f"\nProfitable arbitrage found between {start} and {end}: Factor {best_arbitrage}")
        print(f"Forward Path: {best_forward_path}")
        print(f"Reverse Path: {best_reverse_path}")
            #loop through teh forward path 
        for i in range(len(best_forward_path)-1):
            from_currency = best_forward_path[i]
            index = ids.index(from_currency)
            from_currency = currencies[index]
            to_currency = best_forward_path[i+1]
            index2 = ids.index(to_currency)
            to_currency = currencies[index2]
                #place a buy trade for the cuurency
            try:
                place_trade(to_currency, 'buy')
            except:
                print(f'Error placing buy order for {to_currency}')
                print(to_currency)
                break
                    #loop through the reverse path
        for i in range(len(best_reverse_path)-1):
            from_currency = best_reverse_path[i]
            index = ids.index(from_currency)
            from_currency = currencies[index]
            to_currency = best_reverse_path[i+1]
            index2 = ids.index(to_currency)
            to_currency = currencies[index2]

            # place a sell trade for currency
            try:
                place_trade(to_currency, 'sell')
            except:
                print(f'Error placing sell order for {to_currency}')
                break

        print(f'Completed arbitrage trade for {start}-{end}.')
        #record the details in the results list
        results.append({
            "start_currency" : start,
            "end_currency" : end,
            "arbitrage_factor" : best_arbitrage,
            "forward_path" : best_forward_path,
            "reverse_path" : best_reverse_path,
            "timestamp" : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
save_results_to_json(results)


