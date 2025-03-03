import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load the dataset
file_path = "relations.csv"  # Update with the actual file path if needed
data = pd.read_csv(file_path)

# Display the first few rows and column names for verification
print(data.head())
print("\nColumns in the CSV file:", data.columns)

# Specify the relevant columns
agent1_col = "Agent1"  # Column name for Agent 1
agent2_col = "Agent2"  # Column name for Agent 2
relation_col = "Status"  # Column name for the relationship type

# Create a directed graph
G = nx.DiGraph()

# Add edges with relationships
for _, row in data.iterrows():
    agent1 = row[agent1_col]
    agent2 = row[agent2_col]
    relation = row[relation_col]

    G.add_edge(agent1, agent2, relation=relation)

# Define the graph layout and style
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)  # Seed for consistent layout

# Extract edge labels
edge_labels = {(u, v): d["relation"] for u, v, d in G.edges(data=True)}

# Draw the graph
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color="lightgreen",
    node_size=3000,
    font_size=10,
    font_weight="bold",
    arrowsize=15
)
nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=edge_labels,
    font_color="blue",
    font_size=10
)

# Add a title and show the plot
plt.title("Agent Relationships", fontsize=14)
plt.show()

