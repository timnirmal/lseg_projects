from step_analyze.dataset import int_list as mccp_ids
from step_analyze.line_analysis import not_used
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

# Function to create 2D plot
def create_2d_plot(G):
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(G)  # Positioning the nodes
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=500, edge_color='gray')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
    plt.title("Graph of Number Transitions")
    plt.show()


# Function to create 3D interactive plot
import plotly.graph_objects as go

def create_3d_interactive_plot(G):
    # Use a 3D spring layout algorithm
    pos = nx.spring_layout(G, dim=3)

    edge_x = []
    edge_y = []
    edge_z = []
    for edge in G.edges():
        x0, y0, z0 = pos[edge[0]]
        x1, y1, z1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_z.extend([z0, z1, None])

    node_x = []
    node_y = []
    node_z = []
    node_text = []
    for node in pos:
        node_x.append(pos[node][0])
        node_y.append(pos[node][1])
        node_z.append(pos[node][2])
        node_text.append('{}'.format(node))  # Node label text

    edge_trace = go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        mode='lines',
        line=dict(color='blue', width=2),
        hoverinfo='none'
    )

    node_trace = go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers+text',
        marker=dict(color='red', size=5),
        text=node_text,  # Add node labels
        textposition='middle center',
        hoverinfo='text'
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title="3D Interactive Graph of Number Transitions",
            scene=dict(
                xaxis=dict(showbackground=False),
                yaxis=dict(showbackground=False),
                zaxis=dict(showbackground=False)
            ),
            margin=dict(b=0, l=0, r=0, t=0)
        )
    )

    fig.show()




# Create a directed graph
G = nx.DiGraph()

# Get the list of unused numbers
unused_numbers = not_used()

# Add nodes (excluding unused numbers)
for i in range(172):
    if i not in unused_numbers:
        G.add_node(i)

# Add edges with weights
for sequence in mccp_ids:
    for i in range(len(sequence) - 1):
        if sequence[i] in unused_numbers or sequence[i + 1] in unused_numbers:
            continue
        if G.has_edge(sequence[i], sequence[i + 1]):
            # Increase weight if edge already exists
            G[sequence[i]][sequence[i + 1]]['weight'] += 1
        else:
            # Add new edge with weight 1
            G.add_edge(sequence[i], sequence[i + 1], weight=1)

# Create the 2D plot
# create_2d_plot(G)

# Create the 3D interactive plot
create_3d_interactive_plot(G)

# Create adjacency matrix
adj_matrix_sparse = nx.adjacency_matrix(G, nodelist=[i for i in range(172) if i not in unused_numbers])

# Convert to a dense matrix (NumPy array)
adj_matrix = adj_matrix_sparse.toarray()

# Print the adjacency matrix
print(adj_matrix)
