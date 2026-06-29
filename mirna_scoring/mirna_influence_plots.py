import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import seaborn as sns
import networkx as nx
from pyvis.network import Network
import math

def convert_to_int_list(lst):
    """
    This function is only for specific formating,
    the output of impact is a list as [1,1,-1,1] etc. This value can be read as a string
    when read the csv files, and this is just to convert the string to a list
    :param lst:
    :return:
    """
    if isinstance(lst, list):
        return [float(x) for x in lst]
    elif isinstance(lst, str):
        string = lst.replace('[', '').replace(']', '')
        string = string.split(',')
        if len(string) < 1:
            return []
        return [float(x) if x != '' else 0 for x in string]
    else:
        return [lst]



def plot_dotplot(df, gene_scale=0.3, mirna_scale=1.5, dot_size=10):
    """
    This take the dataframe with the lists of [1,1,-1] type, and plots a dotplot
    with the size of the dot the len of the list and the color the sum
    :param df:
    :return:
    """
    # Create new DataFrame for plotting
    plot_data = pd.DataFrame(index=df.index, columns=df.columns)
    size_data = pd.DataFrame(index=df.index, columns=df.columns)
    color_data = pd.DataFrame(index=df.index, columns=df.columns)

    for col in df.columns:
        for idx in df.index:
            int_list = convert_to_int_list(df.at[idx, col])
            size_data.at[idx, col] = len(int_list)
            color_data.at[idx, col] = sum(int_list)

    # Convert to long format for seaborn
    plot_data = pd.DataFrame({
        'Gene': np.repeat(df.index, df.shape[1]),
        'miRNA': np.tile(df.columns, df.shape[0]),
        'Paths': size_data.values.flatten(),
        'Influence': color_data.values.flatten()
    })

    # Define custom colormap
    cmap = LinearSegmentedColormap.from_list('custom', ['red', 'white', 'blue'])

    # Filter out rows where the size is 0
    plot_data = plot_data[plot_data['Paths'] > 0]

    colors = ['red', 'white', 'blue']
    n_mid = abs(min(plot_data['Influence'])) / (abs(min(plot_data['Influence'])) + max(plot_data['Influence']))
    nodes = [0, n_mid, 1]
    cmap = LinearSegmentedColormap.from_list('custom', list(zip(nodes, colors)))

    # Plot using seaborn
    n_mirna = len(size_data.columns) + 1
    n_genes = len(size_data) + 1
    print('genes', n_genes - 1)
    print('mirnas', n_mirna - 1)
    height_plot = min(655, int(n_genes * gene_scale))

    height_plot = max(10, height_plot)
    sns.set(rc={'axes.facecolor': 'lightgray'})
    x = n_mirna * mirna_scale
    y = height_plot
    fig, ax = plt.subplots(figsize=(x, y))
    ax.grid(False)

    # plt.figure(figsize=(10, height_plot))
    scatter_plot = sns.scatterplot(data=plot_data, x='miRNA', y='Gene', size='Paths', hue='Influence', palette=cmap,
                                   sizes=(x, y * dot_size))
    scatter_plot.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=1)
    if n_genes > 2:
        # Get the first two and last y-tick positions.
        miny, nexty, *_, maxy = ax.get_yticks()

        # Compute half the y-tick interval (for example).
        eps = (nexty - miny) / 2  # <-- Your choice.
        plt.xticks(rotation=45)
        # Adjust the limits.
        ax.set_ylim(maxy + eps, miny - eps)
    # plt.tight_layout()
    plt.show()
    return fig,ax


def plot_pathway_frequency(frequency_pathways):

    x = frequency_pathways.keys()
    y = frequency_pathways.values()
    plt.figure(figsize=(20,6))
    plt.xticks(rotation=90)

    plt.plot(x, y)
    plt.show()

def plot_pathways_keyword_heatmap(mir_pathway_influence_df):
    if 'participation' not in mir_pathway_influence_df:
        mir_pathway_influence_df['participation'] = mir_pathway_influence_df.drop(
            columns=["Different_pathways", "Total"]).sum(axis=1)
    mir_pathway_influence_df_n0 = mir_pathway_influence_df[mir_pathway_influence_df['participation'] > 0]
    mir_pathway_influence_df_n0 = mir_pathway_influence_df_n0.drop(
        columns=["Different_pathways", "Total", "participation"], errors='ignore')
    mir_pathway_influence_df_n0 = mir_pathway_influence_df_n0.loc[:, (mir_pathway_influence_df_n0 != 0).any(axis=0)]
    sns.heatmap(mir_pathway_influence_df_n0, cmap="YlOrBr", annot=True)


def plot_mirnas_similarirty(dist_df, save_path=None):
    """
    Plots a heatmap of the distance matrix, sorted by the mean distance of each mi
    :param dist_df: DataFrame containing the distance matrix
    :param save_path: If provided, saves the heatmap as an image file
    """
    sorted_index = dist_df.mean().sort_values().index  # Sorting by mean distance

    # Apply sorting to the DataFrame
    sorted_df = dist_df.loc[sorted_index, sorted_index]

    # Plot the sorted distance matrix as a heatmap
    n_mirnas = len(sorted_df)
    size_l = n_mirnas * 0.3
    plt.figure(figsize=(size_l, size_l))
    sns.heatmap(sorted_df, annot=False, cmap='coolwarm')  # , linewidths=0.5)#, linecolor='black')
    plt.title('Sorted Distance Matrix Heatmap')
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()


def draw_network(G, node_list, name, interactive=True, save_path='mirna_scoring/sub_plots'):
    """
    Draws a network with selected nodes.

    Parameters:
        G (networkx.Graph): The graph to visualize.
        node_list (list): List of nodes to include in the visualization.
        interactive (bool): Whether to display an interactive graph in a Jupyter Notebook.
        save_path (str, optional): If provided, saves the static graph as an image.
        :param G: NetworkX networks
        :param node_list:  The list of the names of the nodes to print
        :param save_path: The path where the network.html will be saved.
        :param interactive:
        :param name:
    """
    # Create a subgraph with only selected nodes
    subG = G.subgraph(node_list).copy()

    if interactive:
        net = Network(notebook=True, height="600px", width="100%", cdn_resources="in_line")

        for node, data in subG.nodes(data=True):
            node_color = "#FA9FB5" if data.get("type") == "mirna" else "lightblue"
            size = 40 if data.get("type") == "mirna" else 20
            net.add_node(node, label=str(node), color=node_color, size=size)
            # net.add_node(node, label=str(node), color="lightblue", size=10)
        # Remove conflicting attributes (e.g., "source", "target")
        for u, v, data in subG.edges(data=True):
            for attr in ["source", "target", "position"]:
                if attr in data:
                    del data[attr]

            weight = data.get("weight", 1)  # Use edge weight if available
            edge_color = "red" if weight == -1 else "blue"  # Color edges based on weight

            net.add_edge(u, v, color=edge_color, arrows="to", width=2)
            # net.add_edge(u, v, value=weight, arrows="to")  # <-- Ensures arrows

        # Create an interactive Pyvis graph
        net.force_atlas_2based(gravity=-100, central_gravity=0.1, spring_length=150, spring_strength=0.001, damping=0.9)

        # net.from_nx(subG)
        net.show(f"{save_path}/{name}.html", notebook=False)
        return None  # Displays inline in Jupyter

    else:
        # Static visualization using Matplotlib
        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(subG)  # Layout for positioning
        nx.draw(subG, pos, with_labels=True, node_color="skyblue", edge_color="gray", node_size=500, font_size=10)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.show()


def generate_html_table(df, table_id = "data_table"):
    """
    Generates an HTML table from the given DataFrame, dynamically adjusting to the columns.
    - Floats are rounded to 3 decimal places.
    - Integers are displayed without decimal points.
    - Values < 0.001 are displayed in scientific notation.

    Parameters:
    - df: DataFrame containing the data for the table.

    Returns:
    - A string containing the HTML table representation.
    """

    def format_value(value):
        """
        Format the value based on the given rules:
        - Round floats to 3 decimal places.
        - Display integers without decimals.
        - Use scientific notation for values < 0.001.
        """
        if isinstance(value, (int, float)):
            if abs(value) < 0.001:
                return f"{value:.1e}"  # Scientific notation
            elif isinstance(value, int):
                return f"{value}"  # No decimal places for integers
            else:
                return f"{value:.3f}"  # Round floats to 3 decimal places
        return value  # For non-numeric values, return as is

    # Start the HTML table
    table_html = f"<table id='{table_id}' border='1'><thead><tr>"

    # Add column headers dynamically from DataFrame
    for col in df.columns:
        table_html += f"<th>{col}</th>"
    table_html += "</tr></thead><tbody>"

    # Populate the table with rows from the DataFrame
    for _, row in df.iterrows():
        table_html += "<tr>"
        for col in df.columns:
            # Apply formatting to each value
            formatted_value = format_value(row[col])
            table_html += f"<td>{formatted_value}</td>"
        table_html += "</tr>"

    # Close the table
    table_html += "</tbody></table>"

    return table_html


def make_dynamic_table(table_html, table_name="Table", table_id = "data_table"):
    """
    Adds sorting functionality to the provided table HTML using DataTables.

    Parameters:
    - table_html: The HTML string of the table to which DataTables will be applied.

    Returns:
    - A string containing the HTML table with DataTables integration.
    """
    # Add DataTables library and JavaScript to enable sorting and other functionalities
    dynamic_html = f"""
    <h2>{table_name}</h2>
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css">
    <script type="text/javascript" charset="utf8" src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
    """

    # Add the table HTML and DataTable initialization script
    dynamic_html += table_html  # Append the table passed from generate_html_table
    dynamic_html += "<script type=\"text/javascript\">$(document).ready(function() {$('#"+table_id+"').DataTable();});</script>"

    return dynamic_html


def prepare_table_from_network(network, selected_nodes)-> pd.DataFrame:
    """
    :param network:
    :param selected_nodes:
    :return: dataframe
    """
    nodes_table = {}
    for node in selected_nodes:
        nodes_table[node] = {'Name': node}
        node_data = network.nodes[node]
        data = node_data['data']
        weight = data['weigh']
        nodes_table[node]['Weight'] = weight
        dds = None
        # print(data.keys())
        if 'metadata' in data and 'dds_original' in data['metadata']:
            dds = data['metadata']['dds_original']
        elif 'metadata' in data and 'dds' in data['metadata']:
            dds = data['metadata']['dds']
        if dds:
            for combination, stat in dds.items():
                nodes_table[node][combination] = stat
        if 'metadata' in data and 'pathways_svd' in data['metadata']:
            pathway_svd = data['metadata']['pathways_svd']
            nodes_table[node]['Pathway svd'] = pathway_svd
        if 'metadata' in data and 'tissue' in data['metadata']:
            sum = 0
            for _, tissue in data['metadata']['tissue'].items():
                sum += tissue
            nodes_table[node]['Tissue presence'] = sum
        else:
            nodes_table[node]['Tissue presence'] = math.nan
        if 'metadata' in data and 'cell_type' in data['metadata']:
            sum = 0
            for _, tissue in data['metadata']['cell_type'].items():
                sum += tissue
            nodes_table[node]['Cell type presence'] = sum
        else:
            nodes_table[node]['Cell type presence'] = math.nan

    nodes_data = pd.DataFrame(nodes_table).T

    return nodes_data

def add_table_to_html_network(html_file, nodes_data, table_name="Table", table_id = "data_table"):
    table_html = generate_html_table(nodes_data, table_id=table_id)
    dynamic_html = make_dynamic_table(table_html, table_name=table_name, table_id=table_id)
    with open(html_file, "r") as file:
        network_content = file.read()

    # Inject the table at the end of the HTML content
    network_content += dynamic_html

    # Save the updated HTML
    updated_html = html_file
    with open(updated_html, "w") as file:
        file.write(network_content)


def generate_html_network_report(network, selected_nodes, name,  influences=None, save_path='mirna_scoring/sub_plots'):
    nodes_data = prepare_table_from_network(network=network, selected_nodes=selected_nodes)
    draw_network(G=network, node_list=selected_nodes,
                 name=name, interactive=True, save_path=save_path)
    html_file = f"{save_path}/{name}.html"
    add_table_to_html_network(html_file=html_file, nodes_data=nodes_data, table_name="Genes relevance", table_id="data_table")
    if influences is not None:
        add_table_to_html_network(html_file=html_file, nodes_data=influences, table_name="MiRNAs influences", table_id="table_mirnas")
    print(f"Saved on {html_file}")
    return html_file

