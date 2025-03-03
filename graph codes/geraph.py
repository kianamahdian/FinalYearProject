import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

file_path = "relations.csv" 
data = pd.read_csv(file_path)
print(data.head())

print("\nColumns in the CSV file:", data.columns)

agent1_col = data.columns[1]  
agent2_col = data.columns[2] 
relation_col = data.columns[4]

G = nx.DiGraph()

for _, row in data.iterrows():
    agent1 = row[agent1_col]
    agent2 = row[agent2_col]
    relation = row[relation_col]

    G.add_edge(agent1, agent2, relation=relation)

plt.figure(figsize=(12, 8))

edge_labels = {(u, v): d["relation"] for u, v, d in G.edges(data=True)}

pos = nx.spring_layout(G)

nx.draw(G, pos, with_labels=True, node_color="lightgreen", node_size=3000, font_size=10, font_weight="bold", arrowsize=15)

nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="blue", font_size=10)

plt.title("Agent Relationships")
plt.show()

