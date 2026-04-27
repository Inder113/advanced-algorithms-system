
import pandas as pd
import networkx as nx

# Load the CSV file that has railway connections
df = pd.read_csv("task1_3_data.csv", header=None, names=["Station1", "Station2", "Cost", "Time"])


# Make a graph object using networkx
G = nx.DiGraph()

# Go through each row and add it to the graph
for _, row in df.iterrows():
    station1 = row["Station1"].strip().lower()
    station2 = row["Station2"].strip().lower()
    cost = int(row["Cost"])
    time = int(row["Time"])
    
    # Add edge with both cost and time stored
    G.add_edge(station1, station2, cost=cost, time=time)

# Ask the user for starting and ending stations
start = input("Enter starting station: ").strip().lower()
end = input("Enter destination station: ").strip().lower()

# Ask user to choose whether they want cheapest or fastest route
choice = input("Do you want the 'cheapest' or 'fastest' route? ").strip().lower()

try:
    if choice == "cheapest":
        # Find the shortest path using cost
        path = nx.dijkstra_path(G, start, end, weight='cost')
        total_cost = sum(G[u][v]['cost'] for u, v in zip(path[:-1], path[1:]))
        print(f"The total cost is {total_cost} with the following route: {path}")
    elif choice == "fastest":
        # Find the shortest path using time
        path = nx.dijkstra_path(G, start, end, weight='time')
        total_time = sum(G[u][v]['time'] for u, v in zip(path[:-1], path[1:]))
        print(f"The total time is {total_time} with the following route: {path}")
    else:
        print("You must type 'cheapest' or 'fastest'.")
except nx.NetworkXNoPath:
    print("Sorry, there is no route between those stations.")
except nx.NodeNotFound:
    print("One or both station names were not found in the data.")
