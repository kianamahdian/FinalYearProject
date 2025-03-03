import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load the dataset
file_path = "relations.csv"  # Update with your file path
df = pd.read_csv(file_path)

# Display basic info
print("Dataset preview:")
print(df.head())

# Group interactions by norm for analysis
norms = df['Norm'].unique()

for norm in norms:
    print(f"\nAnalyzing interactions for norm: {norm}\n")
    norm_data = df[df['Norm'] == norm]
    
    # Generate a graph for agent interactions
    G = nx.DiGraph()  # Directed graph since stance and status imply direction
    
    for _, row in norm_data.iterrows():
        G.add_node(row['Agent1'], stance=row['Agent1_Stance'])
        G.add_node(row['Agent2'], stance=row['Agent2_Stance'])
        G.add_edge(row['Agent1'], row['Agent2'], status=row['Status'])
    
    # Analyze graph metrics
    print(f"Number of nodes (agents): {G.number_of_nodes()}")
    print(f"Number of edges (interactions): {G.number_of_edges()}")
    
    # Calculate centrality metrics
    in_degree_centrality = nx.in_degree_centrality(G)
    out_degree_centrality = nx.out_degree_centrality(G)
    print("\nIn-Degree Centrality (most influenced agents):")
    print(sorted(in_degree_centrality.items(), key=lambda x: -x[1])[:5])
    print("\nOut-Degree Centrality (most influential agents):")
    print(sorted(out_degree_centrality.items(), key=lambda x: -x[1])[:5])
    
    # Visualize the graph
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=1500, font_size=10)
    edge_labels = nx.get_edge_attributes(G, 'status')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title(f"Agent Interaction Graph for Norm: {norm}")
    plt.show()

