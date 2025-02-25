### This file is the mail pipeline for my priject
import pandas as pd
import pytest

import Constants
import cytoscape as ct
import network_processing as ntp
import os.path
from os import path
import py4cytoscape as py4
import node_evaluation as ne


def get_cytoscape_network(file_name):
    cytoscape_json = ct.read_cytoscape_json(cytoscape_file=file_name)
    nodes, edges_metadata, relationship = ct.format_cytoscape_json(cytoscape_json=cytoscape_json)
    the_network = ntp.create_graph_from_dictionaries(nodes=nodes, edges=edges_metadata, relationship=relationship)
    return the_network


def add_mirnas_n_select(cytoscape_network, name, use_prefix=True, add_mirnas=True, cutoff=0.5):
    """

    :param cytoscape_network: str Name of the network saved as cyjs
    :param name: str Name to save the graph and subproducts
    :param use_prefix: Bool
    :param add_mirnas: Bool
    :return:
    """
    if use_prefix:
        px1 = "graph0_"
        px2 = "graph1_"
    else:
        px1 = px2 = ""
    if not os.path.exists(f"{px1}{name}.pkl"):
        the_network = get_cytoscape_network(cytoscape_network)
        ntp.save_graph(the_network, f"{px1}{name}.pkl")
    else:
        the_network = ntp.load_graph(f"{px1}{name}.pkl")
    if add_mirnas:
        if not os.path.exists(f"{px2}{name}.pkl"):
            ntp.add_mirna_relationships(the_network)
            ntp.save_graph(the_network, f"{px2}{name}.pkl")
        else:
            the_network = ntp.load_graph(f"{px2}{name}.pkl")

    network = ntp.remove_nodes_low_centrality(graph=the_network, cutoff=cutoff)
    ntp.set_positions(network)
    ntp.save_graph(network, f"{px2}_filtered_{name}.pkl")
    save_as_cjsn(network, f'{px2}{name}.cyjs')
    return network


def add_mirnas_n_tissues(cytoscape_network, name, use_prefix=True, add_mirnas=True, add_tissues=True, add_system=True):
    """
    :param add_system: Bool
    :param cytoscape_network: str Name of the network saved as cyjs
    :param name: str Name to save the graph and subproducts
    :param use_prefix: Bool
    :param add_mirnas: Bool
    :param add_tissues: Bool
    :return:
    """
    if use_prefix:
        px1 = "graph0_"
        px2 = "graph1_"
    else:
        px1 = px2 = ""
    the_network = get_network(px1, px2, cytoscape_network)
    if add_tissues:
        ntp.add_tissue_relationship(the_network)
    if add_system:
        ntp.add_organ_system_relationship(the_network)
    the_network.remove_nodes_from(['Tnf'])
    ntp.set_positions(the_network)
    ne.evaluate_nodes(the_network)
    # ne.remove_nodes(the_network, threshold=0.85)
    ntp.save_graph(the_network, f"{px2}{name}.pkl")
    save_as_cjsn(the_network, f'{px2}{name}.cyjs')


def save_as_cjsn(network, name):
    """
    This function will take a network and save it for cytoscape use
    :return:
    """
    json_network = ntp.convert_to_json(network)
    ct.save_cytoscape_json(json_network, cytoscape_file_name=name)


def get_network(px1, px2, cytoscape_network, save_name, add_mirnas=True):
    """
    This function will get the network, first is going to check if it already
    constructed it or if it has to calculate it.
    :param px1: the prefix of the first buiid
    :param px2: the prefix of the network with the microRNAS
    :param cytoscape_network: The name of the file that holds the cjsn of the network
    :param save_name: The name from which the network is saved
    :param add_mirnas: If we shoul add mirnas or not
    :return:
    """
    if not os.path.exists(f"{px1}{save_name}.pkl"):
        the_network = get_cytoscape_network(cytoscape_network)
        ntp.save_graph(the_network, f"{px1}{save_name}.pkl")
    else:
        the_network = ntp.load_graph(f"{px1}{save_name}.pkl")
    if add_mirnas:
        if not os.path.exists(f"{px2}{save_name}.pkl"):
            ntp.add_mirna_relationships(the_network)
            ntp.save_graph(the_network, f"{px2}{save_name}.pkl")
        else:
            the_network = ntp.load_graph(f"{px2}{save_name}.pkl")
    return the_network


def full_flow_pageRank(cytoscape_network, name, use_prefix=True, cutoff=0.5):
    """
    :param cytoscape_network: str Name of the network saved as cyjs
    :param name: str Name to save the graph and subproducts
    :param use_prefix: Bool
    :param cutoff:

    :return:
    """
    if use_prefix:
        px1 = "graph0_"
        px2 = "graph1_"
    else:
        px1 = px2 = ""
    the_network = get_network(px1, px2, cytoscape_network, save_name=name)

    network = ntp.remove_nodes_low_centrality_pageRank(graph=the_network, cutoff=cutoff)
    network = ntp.set_positions(network)
    ntp.save_graph(network, f"Networks_pkl/pageRank_{px2}_{name}.pkl")
    save_as_cjsn(network, f'Networks_CYJS(out)/pageRank_{px2}_{name}.cyjs')

    return network


def full_flow_genes_tf(cytoscape_network, name, use_prefix=True, dds_df=None, tissue_df=None, cutoff=0.5):
    """
    :param cytoscape_network: str Name of the network saved as cyjs
    :param name: str Name to save the graph and subproducts
    :param use_prefix: Bool
    :param cutoff:

    :return:
    """
    if use_prefix:
        px1 = "original_"
        px2 = "mirnas_"
    else:
        px1 = px2 = ""
    if not os.path.exists(f"Networks_pkl/metadata_{px2}_{name}.pkl"):
        network = get_network(px1, px2, cytoscape_network, save_name=name)
        ntp.add_pathways_to_nodes(graph=network,
                                  pathway_file="data/enr_pvals_RNAseq_abundances_adjusted_combat_inmose_young.vs"
                                               ".old_filtered.csv")
        ntp.mark_TF_nodes_from_file(graph=network, TF_file="data/tf_actsRNAseq_abundances_adjusted_combat_inmose_young.vs"
                                                           ".old.csv")
        ntp.add_tissue_to_nodes(graph=network,
                                tissues_df=tissue_df)
        ntp.mark_miR_nodes(graph=network)
        if dds_df is not None:
            ntp.add_DDS_data(network, dds_df=dds_df)

        ntp.weight_nodes(graph=network)
        ntp.save_graph(network, f"Networks_pkl/metadata_{px2}_{name}.pkl")
    else:
        network = ntp.load_graph(f"Networks_pkl/metadata_{px2}_{name}.pkl")
    network = ntp.set_positions(network)

    network = ntp.remove_nodes_low_centrality_pageRank(graph=network, weigth='weigh', cutoff=cutoff)
    n_mirnas = ntp.get_n_mirs(network)
    #network = nx.get_interest_genes_and_neighbors(n_neighbors=2, graph= network)
    ntp.save_graph(network, f"Networks_pkl/complete_n_tf_{px2}_{name}.pkl")
    save_as_cjsn(network, f'Networks_CYJS(out)/complete_n_tf_{px2}_{name}.cyjs')

    return network


def open_cytoscape(file_name):
    py4.open_session(file_name)


if __name__ == '__main__':
    # file = "/home/karen/Documents/GitHub/Muscle_wasting/cytoscape/Sarcopenia.cyjs"
    # name = "Analysis_Sarcopenia_cut"
    # add_mirnas_n_tissues(file, name, add_tissues=False, add_system=False)
    # add_mirnas_n_select(file, "GSE38718_w_mirnas")
    # add_mirnas_n_select(name + ".cyjs", name + "2")

    import pathlib
    import os

    file = pathlib.Path("/home/karen/Documents/GitHub/Muscle_wasting/network/Networks_CYJS/tf_network_ML_and_10_DE.cyjs")
    path_DDS_data = "/home/karen/Documents/GitHub/Muscle_wasting/data/normalize_DDS.csv"
    path_tissue_data = "/home/karen/Documents/GitHub/Muscle_wasting/data/gene_tissue.csv"
    dds_df = pd.read_csv(path_DDS_data, index_col=0).fillna(0)
    tissue_df = pd.read_csv(path_tissue_data, index_col=0).fillna(0)
    file_name = os.path.basename(file)
    for n in [0.5, 0.7]:
        name = file_name.split(".")[0] + f"_cutoff_{n}"
        full_flow_genes_tf(file, name, dds_df=dds_df, tissue_df=tissue_df, cutoff=n)
