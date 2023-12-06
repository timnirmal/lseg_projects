import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import plotly.graph_objects as go

from step_analyze.dataset import int_list as mccp_ids
from step_analyze.line_analysis import not_used


# Function to create 2D plot
def create_2d_plot(G):
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(G)  # Positioning the nodes
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=500, edge_color='gray')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
    plt.title("Graph of Number Transitions")
    plt.show()


# Function to create 3D interactive plot
def create_3d_interactive_plot(G, exclude_nodes=None):
    # If no list of nodes to exclude is provided, default to an empty list
    if exclude_nodes is None:
        exclude_nodes = []

    # Use a 3D spring layout algorithm
    pos = nx.spring_layout(G, dim=3)

    edge_x = []
    edge_y = []
    edge_z = []
    for edge in G.edges():
        # Check if either of the nodes in the edge should be excluded
        if edge[0] in exclude_nodes or edge[1] in exclude_nodes:
            continue
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
        if node not in exclude_nodes:
            node_x.append(pos[node][0])
            node_y.append(pos[node][1])
            node_z.append(pos[node][2])
            node_text.append('{}'.format(node))

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
        text=node_text,
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


# Function to verify adjacency matrix against graph edge weights
def verify_adjacency_matrix(G, adj_matrix, nodelist):
    is_correct = True
    for i, node_from in enumerate(nodelist):
        for j, node_to in enumerate(nodelist):
            # Check if there's an edge in the graph
            if G.has_edge(node_from, node_to):
                # Compare the weight in the graph with the matrix entry
                if G[node_from][node_to]['weight'] != adj_matrix[i, j]:
                    print(
                        f"Discrepancy found for edge ({node_from}, {node_to}): Graph weight {G[node_from][node_to]['weight']} vs Matrix entry {adj_matrix[i, j]}")
                    is_correct = False
    return is_correct


# Save the adjacency matrix to CSV
def save_adjacency_matrix_to_csv(adj_matrix, nodelist, file_name='adjacency_matrix.csv'):
    # Convert the numpy matrix to a DataFrame
    df = pd.DataFrame(data=adj_matrix, index=nodelist, columns=nodelist)

    # Save to CSV
    df.to_csv(file_name)
    print(f"Adjacency matrix saved to {file_name}")


def create_step_graph(number_of_nodes=172, unused_numbers=None, plot_2d=False, plot_3d=True, exclude_nodes=None):
    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes (excluding unused numbers)
    for i in range(number_of_nodes):
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
    if plot_2d:
        create_2d_plot(G)

    # Create the 3D interactive plot
    if plot_3d:
        create_3d_interactive_plot(G, exclude_nodes)

    return G


# Create adjacency matrix
def create_adjacency_matrix(G, number_of_nodes=172, save=True, unused_numbers=None):
    adj_matrix_sparse = nx.adjacency_matrix(G, nodelist=[i for i in range(number_of_nodes) if i not in unused_numbers])

    # Convert to a dense matrix (NumPy array)
    adj_matrix = adj_matrix_sparse.toarray()

    # Nodes list after excluding unused numbers
    nodelist = [i for i in range(number_of_nodes) if i not in unused_numbers]

    # Verify the adjacency matrix
    if verify_adjacency_matrix(G, adj_matrix, nodelist):
        print("The adjacency matrix correctly represents the number of connections between nodes.")
    else:
        print("There are discrepancies in the adjacency matrix.")

    # Save the adjacency matrix as CSV
    if save:
        save_adjacency_matrix_to_csv(adj_matrix, nodelist)

    return adj_matrix

def plot_adjacency_matrix(adj_matrix, nodelist):
    fig, ax = plt.subplots(figsize=(12, 12))
    cax = ax.matshow(adj_matrix, cmap='Oranges')

    # Set axis labels
    plt.xticks(range(len(nodelist)), nodelist, rotation=90)
    plt.yticks(range(len(nodelist)), nodelist)

    # Add colorbar to interpret the values
    fig.colorbar(cax)

    plt.title('Adjacency Matrix with Node Labels')
    plt.xlabel('Target Node')
    plt.ylabel('Source Node')

    plt.show()


number_of_nodes = 172
exclude_nodes = [92]

# Get the list of unused numbers
unused_numbers = not_used()

# Create the graph
G = create_step_graph(number_of_nodes=number_of_nodes, unused_numbers=unused_numbers, plot_2d=False, plot_3d=True,
                      exclude_nodes=exclude_nodes)

# Create the adjacency matrix
adj_matrix = create_adjacency_matrix(G, number_of_nodes=number_of_nodes, unused_numbers=unused_numbers)


# # create a plot of matrix
# plt.imshow(adj_matrix, cmap='hot', interpolation='nearest')
# plt.show()

# plot the adjacency matrix
plot_adjacency_matrix(adj_matrix, nodelist=[i for i in range(172) if i not in unused_numbers])