import numpy as np
import pandas as pd
from scipy.stats import zscore
import decoupler as dc
import os
from mirkitten.plot_GSEA_ORA import plot_ora_results

def select_extreme_rows(df, x, method='zscore'):
    """
    Selects the top x most extreme rows based on outlier detection.

    Parameters:
    df (pd.DataFrame): Input numerical dataframe (m x n)
    x (int): Number of rows to select
    method (str): 'zscore' for Z-score method, 'iqr' for IQR-based method

    Returns:
    pd.DataFrame: Subset of df with the most extreme x rows
    """
    if method == 'zscore':
        # Compute absolute Z-scores
        z_scores = np.abs(zscore(df, axis=0))
        row_scores = z_scores.sum(axis=1)  # Sum of absolute Z-scores per row

    elif method == 'iqr':
        # Compute IQR for each column
        Q1 = df.quantile(0.25)
        Q3 = df.quantile(0.75)
        IQR = Q3 - Q1

        # Count how many columns have outlier values per row
        outlier_mask = ((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR)))
        row_scores = outlier_mask.sum(axis=1)

    else:
        raise ValueError("Invalid method. Choose 'zscore' or 'iqr'.")

    # Select top x rows with highest scores
    top_x_rows = df.iloc[np.argsort(row_scores)[-x:]]
    return top_x_rows, row_scores


def select_top_ranked_rows(df, x):
    """
    Selects the top x most important rows based on column-wise ranking.

    Parameters:
    df (pd.DataFrame): Input numerical dataframe (m x n)
    x (int): Number of rows to select

    Returns:
    pd.DataFrame: Subset of df with the top ranked x rows
    """
    # Rank each column in descending order (highest value gets rank 1)
    rankings = df.rank(method='average', ascending=False)

    # Compute aggregate rank score per row (sum of ranks)
    row_scores = rankings.sum(axis=1)

    # Select top x rows with highest aggregate rank scores
    top_x_rows = df.iloc[np.argsort(row_scores)[:x]]
    return top_x_rows, row_scores


def select_top_normalized_rows(df, x):
    """
    Selects the top x most important rows by normalizing each column to [0,1] and summing values.

    Parameters:
    df (pd.DataFrame): Input numerical dataframe (m x n)
    x (int): Number of rows to select

    Returns:
    pd.DataFrame: Subset of df with the top x rows based on normalized sum
    """
    # Normalize each column to range [0,1]
    normalized_df = (df - df.min()) / (df.max() - df.min())

    # Compute row scores as sum of normalized values
    row_scores = normalized_df.sum(axis=1)

    # Select top x rows with highest scores
    top_x_rows = df.iloc[np.argsort(row_scores)[-x:]]
    return top_x_rows, row_scores

def count_de_gene(gene_node, comparisons=None, dds_threshold=0):
    """
    for each gene, count how many times it is DE (max is the amount of comparisons)
    :return:
    """
    quantity = 0
    if 'dds_original' in gene_node['data']['metadata'] :
        dds = gene_node['data']['metadata']['dds_original']
        for comparison in comparisons:
            comp = dds[comparison]
            # if comp is greater than the threshold, then it will be counted, otherwise it will be 0
            if abs(comp) > dds_threshold:
                quantity += 1
    # quantity is lower 0, max the amount of comparisons
    return quantity


def get_mirna_target_enriched(selected_genes, title, msigdb):
    enriched = dc.get_ora_df(
            df=selected_genes,
            net=msigdb,
            source='geneset',
            target='genesymbol'
        )
    pathway_df = enriched[enriched['FDR p-value'] < 0.1]
    pathway_df.index = pathway_df["Term"]
    #pathway_df.set_index("Term", inplace=True)  # Set "Term" as index
    enriched_pathways = pathway_df['Combined score']
    return plot_ora_results(pathway_df, top_n=10, figsize=(12, 6), scale_odds_ratio=.5,
                     fontsize_title=12, fontsize_subtitle=12, fontsize_text=10,title=title)
def get_mirna_target_enriched_df(selected_genes, title, msigdb):
    enriched = dc.get_ora_df(
            df=selected_genes,
            net=msigdb,
            source='geneset',
            target='genesymbol'
        )
    pathway_df = enriched[enriched['FDR p-value'] < 0.1]
    pathway_df.index = pathway_df["Term"]
    #pathway_df.set_index("Term", inplace=True)  # Set "Term" as index
    enriched_pathways = pathway_df['Combined score']
    return enriched_pathways, pathway_df