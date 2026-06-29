import sys

sys.path.append('../')
#from .. import network_processing as nx
#from .. import main_pipeline as mp
import pytest
import cytoscape as ct
from network import main_pipeline as mp
from network import network_processing
import yaml
import pandas as pd

def test_test():
    assert True

def test_full_flow_genes_tf(monkeypatch):

    monkeypatch.setattr(
        mp, 'save_as_cjsn', lambda *args, **kwargs: None
     )
    monkeypatch.setattr(network_processing, 'save_graph', lambda *args, **kwargs: None)
    monkeypatch.setattr(network_processing, 'get_SVD_pathways',lambda *args, **kwargs: 1 )
    name_n = "ALDOA_test_no_save"

    with open("network/settings/metadata.yml", 'r') as file:
        config_data = yaml.safe_load(file)

    file = config_data["oNetwork"]
    path_tissue_data = config_data['path_tissue_data']
    path_dds_data = config_data['path_DDS_data']
    pathway_file = config_data['path_pathway_file']
    tf_file = config_data['path_tf_file']
    cell_type_file = config_data['path_cell_type_data']
    coefficents = config_data['coefficients']    


    import pandas as pd
    dds_df = pd.read_csv(path_dds_data, index_col=0).fillna(0)
    tissue_df = pd.read_csv(path_tissue_data, index_col=0).fillna(0)
    cell_type_df = pd.read_csv(cell_type_file, index_col=0).fillna(0)


    network, _ = mp.full_flow_genes_tf(cytoscape_network="network/test_networks/ALDOA_LDHA.cyjs",
                                    name= name_n,
                                    dds_df= dds_df,
                                    tissue_df=tissue_df,
                                    tf_file=tf_file,
                                    pathway_file=pathway_file,
                                    cell_type=cell_type_df,
                                    coefficients=coefficents,
                                    cutoff=0.5)
    print(network)
    assert len(network.nodes()) == 7, f"The test network ALDOA should have 6 genes to start and 11 mirnas."

def test_full_flow_genes_tf_2(monkeypatch):
    import pandas as pd

    yml_path = "/home/karen/Documents/GitHub/Muscle_wasting/UseCases/Sarcopenia/configurations_YML"
    networks =[]
    coefs = []
    for i in range(1,9):
        confs_yml_path = f"{yml_path}/config_{i}.yml"
        with open(confs_yml_path, 'r') as file:
            config_data = yaml.safe_load(file)
            name_n = f"Configuration_{i}"
            file = config_data["oNetwork"]
            path_tissue_data = config_data['path_tissue_data']
            path_dds_data = config_data['path_DDS_data']
            pathway_file = config_data['path_pathway_file']
            tf_file = config_data['path_tf_file']
            cell_type_file = config_data['path_cell_type_data']
            coefficents = config_data['coefficients']
            coefs.append(coefficents)

            dds_df = pd.read_csv(path_dds_data, index_col=0).fillna(0)
            tissue_df = pd.read_csv(path_tissue_data, index_col=0).fillna(0)
            cell_type_df = pd.read_csv(cell_type_file, index_col=0).fillna(0)


            network, _ = mp.full_flow_genes_tf(cytoscape_network=file,
                                            name= name_n,
                                            dds_df= dds_df,
                                            tissue_df=tissue_df,
                                            tf_file=tf_file,
                                            pathway_file=pathway_file,
                                            cell_type=cell_type_df,
                                            coefficients=coefficents,
                                            path="/home/karen/Documents/GitHub/Muscle_wasting/UseCases/Sarcopenia/output/",
                                            cutoff=0.9)
            networks.append(network)

    print(networks)
    print(coefs)
    assert not all(x==networks[0] for x in networks)
    nodes_1 = set(networks[0].nodes)
    nodes_2 = set(networks[1].nodes)
    nodes_3 = set(networks[2].nodes)
    same_networks = set(networks[1].nodes) == set(networks[2].nodes)
    same_networks = set(networks[1].nodes) == networks[2]


def test_remove_nodes(monkeypatch):

        monkeypatch.setattr(
            mp, 'save_as_cjsn', lambda *args, **kwargs: None
        )
        name_n = "ALDOA_test_no_save"

        with open("network/settings/metadata.yml", 'r') as file:
            config_data = yaml.safe_load(file)

        file = config_data["oNetwork"]
        path_tissue_data = config_data['path_tissue_data']
        path_dds_data = config_data['path_DDS_data']
        pathway_file = config_data['path_pathway_file']
        tf_file = config_data['path_tf_file']
        cell_type_file = config_data['path_cell_type_data']
        coefficents = config_data['coefficients']

        import pandas as pd
        dds_df = pd.read_csv(path_dds_data, index_col=0).fillna(0)
        tissue_df = pd.read_csv(path_tissue_data, index_col=0).fillna(0)
        cell_type_df = pd.read_csv(cell_type_file, index_col=0).fillna(0)

        network, _ = mp.full_flow_genes_tf(cytoscape_network="network/test_networks/ALDOA_LDHA.cyjs",
                                           name=name_n,
                                           dds_df=dds_df,
                                           tissue_df=tissue_df,
                                           tf_file=tf_file,
                                           pathway_file=pathway_file,
                                           cell_type=cell_type_df,
                                           coefficients=coefficents,
                                           cutoff=0.01)
        print(network)
        assert len(network.nodes()) == 17, f"The test network ALDOA should have 6 genes to start and 11 mirnas."


def test_nodes_integrity(monkeypatch):
    graph = network_processing.load_graph("network/test_networks/original_ALDOA_test.pkl")
    monkeypatch.setattr(mp, "get_cytoscape_network",  lambda *args, **kwargs: graph )
    monkeypatch.setattr(
        mp, 'save_as_cjsn', lambda *args, **kwargs: None
     )
    name_n = "ALDOA_test"
    # monkeypatch for save_graph to do nothing
    monkeypatch.setattr(
        network_processing, 'save_graph', lambda *args, **kwargs: None
    )

    with open("network/settings/metadata.yml", 'r') as file:
        config_data = yaml.safe_load(file)

    file = config_data["oNetwork"]
    path_tissue_data = config_data['path_tissue_data']
    path_dds_data = config_data['path_DDS_data']
    pathway_file = config_data['path_pathway_file']
    tf_file = config_data['path_tf_file']


    import pandas as pd
    dds_df = pd.read_csv(path_dds_data, index_col=0).fillna(0)
    tissue_df = pd.read_csv(path_tissue_data, index_col=0).fillna(0)

    network, _ = mp.full_flow_genes_tf(cytoscape_network="network/test_networks/ALDOA_LDHA.cyjs",
                                    name= name_n,
                                    dds_df= dds_df,
                                    tissue_df=tissue_df,
                                    tf_file=tf_file,
                                    pathway_file=pathway_file,
                                    cutoff=0.5)
    print(network)
    assert len(network.nodes()) == 17, f"The test network ALDOA should have 6 genes to start and 11 mirnas."

def test_read_cytoscape_json(monkeypatch):
    """
    This test will cgheck that the nodes we start with are ok having the minimun properties.
    :param monkeypatch:
    :return:
    """
    cytoscape_json = ct.read_cytoscape_json(cytoscape_file="network/test_networks/ALDOA_LDHA.cyjs")
    nodes, edges, relationships = ct.format_cytoscape_json(cytoscape_json=cytoscape_json)

    print(nodes)
    # check that nodes is len 6
    assert len(nodes) == 6, f"The test network ALDOA should have 6 nodes."
    # check that edges is len 0
    assert len(edges) == 0, f"The test network ALDOA should have 0 edges."
    # check that relationships is len 0
    assert len(relationships) == 0, f"The test network ALDOA should have 0 relationships."
    # check that the nodes have the correct properties
    for node in nodes:
        assert 'data' in node, f"The node should have a data property"
        # Data must have name, id, shared_name, SUID and selected
        assert 'name' in node['data'], f"The node should have a name property"
        assert 'id' in node['data'], f"The node should have an id property"
        assert 'name' in node['data'], f"The node should have a name property"
        assert 'type' in node, f"The node should have a type property"
        assert node['type'] in ['gene', 'mirna'], f"The node should have a type property with value gene or mirna"

def test_get_cytoscape_network(monkeypatch):
    nodes = [{'data': {'SUID': 2000278, 'id': '2000278',
                       'id_original': '6071', 'name': 'NT5E',
                       'selected': False, 'shared_name': 'NT5E'},
              'position': {'x': 185.46056354998848, 'y': 296.23009851467975},
              'selected': False, 'source': 'Cytoscape', 'type': 'gene'},
             {'data': {'SUID': 2005417, 'id': '2005417',
                       'id_original': '2645', 'name': 'ALDOA',
                       'selected': False, 'shared_name': 'ALDOA'},
              'position': {'x': 57.46056354998848, 'y': 124.04747060021452},
              'selected': False, 'source': 'Cytoscape', 'type': 'gene'}]
    edges = []
    relationship= []

    # monkeypatch to read_cytoscape_json to retun nodes, edges and relationship
    monkeypatch.setattr("cytoscape.read_cytoscape_json", lambda *args, **kwargs: (nodes, edges, relationship))

    network = network_processing.create_graph_from_dictionaries(nodes=nodes, edges=edges, relationship=relationship)
    print (network)
    assert len(network.nodes()) == 2, f"The network should have 2 nodes"
    assert len(network.edges()) == 0, f"The network should have 0 edges"
    assert network.nodes['NT5E']['type'] == 'gene', f"The node NT5E should have type gene"
    assert network.nodes['ALDOA']['type'] == 'gene', f"The node ALDOA should have type gene"

def test_add_dds_to_node():
    graph = network_processing.load_graph("network/test_networks/original_ALDOA_test.pkl")
    dds_df_dummy = pd.read_csv("network/test_networks/dummy_data/dds_file.csv", index_col=0)
    network_processing.add_DDS_data(graph=graph, dds_df=dds_df_dummy)
    test_nodes = dict(graph.nodes(data=True))
    print(test_nodes)
    for node in test_nodes:
        if node in dds_df_dummy.index:
            metadata = test_nodes[node]['data']['metadata']
            node_name = test_nodes[node]['data']['name']
            assert 'dds' in metadata, f"The node {node} should have a dds property"

            # metadata['dds'] is a dictionary
            assert type(metadata['dds']) == dict, f"The node {node} should have a dictionary as dds values"
            # metadata['dds'] should have the same values as the dds_df_dummy
            assert metadata['dds'] == dds_df_dummy.loc[node_name].to_dict(), (f"The node {node} should "
                                                              f"have the correct dds values")

def test_add_pathways_to_nodes():
    graph = network_processing.load_graph("network/test_networks/original_ALDOA_test.pkl")
    pathway_df_dummy = "network/test_networks/dummy_data/pathway_file.csv"
    network_processing.add_pathways_to_nodes(graph=graph, pathway_file=pathway_df_dummy)
    test_nodes = dict(graph.nodes(data=True))
    print(test_nodes)
    for node in test_nodes:
        if node in ['ALDOA', 'NT5E']:
            metadata = test_nodes[node]['data']['metadata']
            assert 'pathways' in metadata, f"The node {node} should have a dds property"
            assert len(metadata['pathways']) >0
            assert len(metadata['pathways']) < 3
            assert 'pathways_svd' in metadata

def test_add_TF_data_from_file():
    graph = network_processing.load_graph("network/test_networks/original_ALDOA_test.pkl")
    tf_file = "network/test_networks/dummy_data/tf_file.csv"
    tf_dummy_df = pd.read_csv(tf_file, index_col=0)
    network_processing.add_TF_data_from_file(graph=graph, tf_file=tf_file)
    test_nodes = dict(graph.nodes(data=True))
    print(test_nodes)
    for node in test_nodes:
        if node in ['ALDOA', 'NT5E']:
            metadata = test_nodes[node]['data']['metadata']
            assert 'tf' in metadata, f"The node {node} should have a TF property"
            assert metadata['tf'] == tf_dummy_df.loc[node].to_dict(), f"The node {node} should have a TF property with value True"

def test_add_other_data():
    graph = network_processing.load_graph("network/test_networks/original_ALDOA_test.pkl")
    tissue_file = "network/test_networks/dummy_data/tissue_file.csv"
    tissue_dummy_df = pd.read_csv(tissue_file, index_col=0)
    network_processing.add_other_data(graph=graph, data_df=tissue_dummy_df, name='tissue')
    test_nodes = dict(graph.nodes(data=True))
    print(test_nodes)
    for node in test_nodes:
        if node in ['ALDOA', 'NT5E']:
            metadata = test_nodes[node]['data']['metadata']
            assert 'tissue' in metadata, f"The node {node} should have a tissue property"
            assert metadata['tissue'] == tissue_dummy_df.loc[node].to_dict(), f"The node {node} should have a tissue property with value True"


def test_weight_nodes():
    graph = network_processing.load_graph("network/test_networks/mirnas_ALDOA_test.pkl")
    dds_df_dummy = pd.read_csv("network/test_networks/dummy_data/dds_file.csv", index_col=0)
    network_processing.add_DDS_data(graph=graph, dds_df=dds_df_dummy)
    patwhay_df_dummy = "network/test_networks/dummy_data/pathway_file.csv"
    network_processing.add_pathways_to_nodes(graph=graph, pathway_file=patwhay_df_dummy)
    tf_file = "network/test_networks/dummy_data/tf_file.csv"
    network_processing.add_TF_data_from_file(graph=graph, tf_file=tf_file)
    tissue_file = "network/test_networks/dummy_data/tissue_file.csv"
    tissue_dummy_df = pd.read_csv(tissue_file, index_col=0)
    network_processing.add_other_data(graph=graph, data_df=tissue_dummy_df, name='tissue')
    cell_type_file = "network/test_networks/dummy_data/cell_type_file.csv"
    cell_type_dummy_df = pd.read_csv(cell_type_file, index_col=0)
    network_processing.add_other_data(graph=graph, data_df=cell_type_dummy_df, name='cell_type')
    coeficients = {'dds': 0.5, 'pathways_svd': 0.3, 'tf': 0.1, 'tissue': 0.05, 'cell_type': 0.05, 'miR_enhancement': 1}
    network_processing.weight_nodes(graph=graph, coefficients=coeficients)
    test_nodes = dict(graph.nodes(data=True))
    print(test_nodes)
    for node in test_nodes:
        weigth = test_nodes[node]['data']['weigh']
        if node in ['ALDOA', 'NT5E']:
            assert weigth > 0
        if test_nodes[node]['type'] == 'mirna':
            assert weigth == coeficients['miR_enhancement'], f"The node {node} should have a weigh property with the correct value"

def test_weight_nodes():
    graph = network_processing.load_graph("network/test_networks/mirnas_ALDOA_test.pkl")
    dds_df_dummy = pd.read_csv("network/test_networks/dummy_data/dds_file.csv", index_col=0)
    network_processing.add_DDS_data(graph=graph, dds_df=dds_df_dummy)
    patwhay_df_dummy = "network/test_networks/dummy_data/pathway_file.csv"
    network_processing.add_pathways_to_nodes(graph=graph, pathway_file=patwhay_df_dummy)
    tf_file = "network/test_networks/dummy_data/tf_file.csv"
    network_processing.add_TF_data_from_file(graph=graph, tf_file=tf_file)
    tissue_file = "network/test_networks/dummy_data/tissue_file.csv"
    tissue_dummy_df = pd.read_csv(tissue_file, index_col=0)
    network_processing.add_other_data(graph=graph, data_df=tissue_dummy_df, name='tissue')
    cell_type_file = "network/test_networks/dummy_data/cell_type_file.csv"
    cell_type_dummy_df = pd.read_csv(cell_type_file, index_col=0)
    network_processing.add_other_data(graph=graph, data_df=cell_type_dummy_df, name='cell_type')
    coeficients = {'dds': 0.5, 'pathways_svd': 0.3, 'tf': 0.1, 'tissue': 0.05, 'cell_type': 0.05, 'miR_enhancement': 1}
    network_processing.weight_nodes(graph=graph, coefficients=coeficients)
    network_processing.weight_edges(graph=graph,node_weight='weigh', mir_enhancer=coeficients['miR_enhancement'])
    test_edges = graph.edges('hsa-miR-122-5p', data=True)
    print(test_edges)
    x = list(test_edges)
    print(x)
    score = x[0][2]['weightScore']
    assert score > 70


def test_main(monkeypatch):
    graph = network_processing.load_graph("network/test_networks/mirnas_ALDOA_test.pkl")
    monkeypatch.setattr(mp, "get_network", lambda *args, **kwargs: graph)
    with open("network/settings/metadata.yml", 'r') as file:
        config_data = yaml.safe_load(file)
    network = "/home/karen/Documents/GitHub/Muscle_wasting/network/test_networks/ALDOA_LDHA.cyjs"
    DE_data =config_data.get("path_DDS_data")
    Tissue_expression = config_data.get(
        "path_tissue_data")
    Cell_type = config_data.get("path_cell_type_data")
    Pathway_enrichment = config_data.get("path_pathway_file")
    TF_enrichment = config_data.get("path_tf_file")
    Cutoff = config_data.get("page_rank_cutoff", [0.5, 0.7])
    output = config_data.get("output")
    open_cytoscape_ = config_data.get("open_cytoscape", False)
    network = mp.main(config_data=config_data,file=network, path_dds_data=DE_data,
            path_tissue_data=Tissue_expression,
            pathway_file=Pathway_enrichment,tf_file=TF_enrichment,
            cell_type_file=Cell_type, ranks=Cutoff, open_cytoscape_=open_cytoscape_)
    hsa_edges = network.edges('hsa-miR-122-5p', data=True)
    hsa_node = network.nodes()['hsa-miR-122-5p']
    print(hsa_node)


def test_main_pathways(monkeypatch):
    graph = network_processing.load_graph("network/test_networks/dummy_data/metadata_mirnas__configuration24_cutoff_0.9.pkl")
    monkeypatch.setattr(mp, "get_network", lambda *args, **kwargs: graph)
    config_data_1 ={'coefficients':
                        {'cellular': 0, 'dds': 0, 'miR_enhancement': 0, 'pathways_svd': 0, 'tf': 0, 'tissue': 0},
                    'oNetwork': '/home/karen/Documents/GitHub/Muscle_wasting/network/Networks_CYJS/tf_network_ML_and_10_DE.cyjs',
                    'page_rank_cutoff': [0.90],
                    'path_DDS_data': '/home/karen/Documents/GitHub/Muscle_wasting/data/join_dds.csv',
                    'path_cell_type_data': '/home/karen/Documents/GitHub/Muscle_wasting/data/proportion_cell_type_div_Sarcopenia_relevant.csv',
                    'path_pathway_file': '/home/karen/Documents/GitHub/Muscle_wasting/data/join_pathway.csv',
                    'path_tf_file': '/home/karen/Documents/GitHub/Muscle_wasting/data/join_tf.csv',
                    'path_tissue_data': '/home/karen/Documents/GitHub/Muscle_wasting/data/gene_tissue_Sarcopenia_relevant.csv'}
    config_data_2 = config_data_1
    coeficients_2 = {'cellular': 0, 'dds': 0, 'miR_enhancement': 0, 'pathways_svd': 1, 'tf': 0, 'tissue':0}

    network = "/home/karen/Documents/GitHub/Muscle_wasting/network/test_networks/ALDOA_LDHA.cyjs"


    DE_data =config_data_1.get("path_DDS_data")
    Tissue_expression = config_data_1.get(
        "path_tissue_data")
    Cell_type = config_data_1.get("path_cell_type_data")
    Pathway_enrichment = config_data_1.get("path_pathway_file")
    TF_enrichment = config_data_1.get("path_tf_file")
    Cutoff = config_data_1.get("page_rank_cutoff", 0.5)
    output = config_data_1.get("output")
    open_cytoscape_ = config_data_1.get("open_cytoscape", False)

    network_1 = mp.main(config_data=config_data_1,file=network, path_dds_data=DE_data,
            path_tissue_data=Tissue_expression,
            pathway_file=Pathway_enrichment,tf_file=TF_enrichment,
            cell_type_file=Cell_type, ranks=Cutoff, open_cytoscape_=open_cytoscape_, coefficients=config_data_1['coefficients'])
    network_2 = mp.main(config_data=config_data_1, file=network, path_dds_data=DE_data,
                        path_tissue_data=Tissue_expression,
                        pathway_file=Pathway_enrichment, tf_file=TF_enrichment,
                        cell_type_file=Cell_type, ranks=Cutoff, open_cytoscape_=open_cytoscape_,
                        coefficients=coeficients_2)
    assert network_1 != network_2


def test_separate_metadata():
    graph = network_processing.load_graph("network/Networks_pkl/complete_n_tf_mirnas__ALDOA_LDHA_cutoff_0.5.pkl")

    network_processing.separate_metadata(graph)

    node_NT5E =graph.nodes()['NT5E']
    assert 'dds_yo_file' in node_NT5E['data']


def test_end():
    pass