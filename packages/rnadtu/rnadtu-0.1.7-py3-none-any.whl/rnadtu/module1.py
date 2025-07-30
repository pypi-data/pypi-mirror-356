"""
CIDR-Clustering Integration for annData

This module provides Python functions for the R-based CIDR algorithm for clustering
single-cell RNA-seq data. It supports both read/write file-based communication
between Python and R via subprocess calls.

Functions
cidr: File-based CIDR clustering
cidr_non_csv: In-memory CIDR clustering.
"""

import anndata as ad  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from scipy.sparse import csr_matrix  # type: ignore
import subprocess
import os
import tempfile
from io import StringIO

def _sparse_to_csv(sparse_matrix, csv_name):
    # Save a sparse matrix as a csv file
    array_matrix = sparse_matrix.toarray()
    df = pd.DataFrame(array_matrix)
    df.to_csv(csv_name, index=False)

def _sparse_to_csv_using_buffer(sparse_matrix):
    array_matrix = sparse_matrix.toarray()
    df = pd.DataFrame(array_matrix)
    # makes the buffer for an input stream
    in_ram = StringIO()
    df.to_csv(in_ram, index=False)
    return in_ram.getvalue()

def _make_args(data_type, n_cluster, pc, dropout, dissim, large, file_path=None, pc_path=None, var_path=None, eigen_path=None, dropout_path=None, dissim_path=None):
    # Make an argumentlist to the Rscript."
    script_path = os.path.join(os.path.dirname(__file__), "module2.R")

    return ["Rscript",
            script_path,
            str(data_type),
            str(n_cluster),
            str(pc),
            str(dropout),
            str(dissim),
            str(large),
            str(file_path),
            str(pc_path),
            str(var_path),
            str(eigen_path),
            str(dropout_path),
            str(dissim_path)]

def _handle_dropout(a_data, layer, dropout_src, buffer=False):
    read = lambda src: pd.read_csv(StringIO(src), index_col=0).to_numpy() if buffer else pd.read_csv(src, index_col=0).to_numpy()

    dropout_array = read(dropout_src)

    a_data.uns[layer + "_cidr_dropout_candidates"] = dropout_array


def _handle_dissim(a_data, layer, dissim_src, buffer=False):
    read = lambda src: pd.read_csv(StringIO(src), index_col=0).to_numpy() if buffer else pd.read_csv(src, index_col=0).to_numpy()

    dissim_array = read(dissim_src)

    a_data.obsp[layer + "_cidr_dissimilarity_matrix"] = dissim_array


def _handle_pc(a_data, layer, pc_src, var_src, eigen_src, buffer=False):
    read = lambda src: pd.read_csv(StringIO(src), index_col=0).to_numpy() if buffer else pd.read_csv(src, index_col=0).to_numpy()

    pc_array = read(pc_src)
    variation_array = read(var_src)
    eigen_array = read(eigen_src)

    a_data.obsm[layer + "_cidr_pc"] = pc_array
    a_data.uns[layer + "_cidr_variation"] = variation_array
    a_data.uns[layer + "_cidr_eigenvalues"] = eigen_array

def cidr(a_data, layer="X", data_type="raw", n_cluster=None, dropout=False, dissim=False, pc=False):
    """
    Perform CIDR on any layer of an annData object, using temporary read-write-files.
    This function is optimal if you are working with large datasets, that would otherwise
    hog a lot of RAM.

    .. warning::
        This algorithm uses temporary read-write files. These can be assumed deleted afterwards
        however, if a sudden spike in disc usage is experienced, these can be found and deleted in:
            For windows users:
            "C:\\Users\\your_user\\AppData\\Local\\Temp"
            For linux users:
            "/tmp"

    Args:
        adata (annData.AnnData): Input Anndata object containing expression data
        layer (str, optional): Name of the layer in 'a_data' to use. If "X", uses 'a_data.X'. Defaults to "X".
        data_type (str): Type of data ("raw" or "cpm")
        n_cluster (int or None): Number of clusters. If None, this is determined by the algorithm
        dropout (bool, optional): Determines whether to save dropout candidates into the annData object.
            These are saved in annData.uns. Defaults to False.
        dissim (bool, optional): Determines whether to save the dissimilarity matrix into the annData object.
            These are saved in annData.obsp. Defaults to False.
        pc (bool, optional): Determines whether to save the principle coordinates, proportion of variation
            and eigenvalue vectors into the annData object.
            These are saved in annData.obsm, annData.uns and annData.uns respectively. Defaults to False.

    Returns:
        None
    """

    # Run CIDR-clustering
    print("Algorithm Starting...")
    data = a_data.X if layer == "X" else a_data.layers[layer]
    sparse_matrix = csr_matrix(data, dtype=np.float32)

    # Creates randomly named temporary files. These are later deleted for the user.
    pc_file = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
    var_file = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
    eigen_file = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
    temp_data_file = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
    dropout_file = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
    dissim_file = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)

    # Sets path for different datafiles for use to read and write in R-script.
    data_path = temp_data_file.name
    pc_path = pc_file.name
    var_path = var_file.name
    eigen_path = eigen_file.name
    dropout_path = dropout_file.name
    dissim_path = dissim_file.name

    # Closes the files to save ram
    pc_file.close()
    var_file.close()
    eigen_file.close()
    temp_data_file.close()
    dropout_file.close()
    dissim_file.close() # garbage collection

    # Saves sparse matrix as csv and then runs the Rscript on the file.
    _sparse_to_csv(sparse_matrix, data_path)
    (subprocess.run(_make_args(data_type, n_cluster, pc, dropout, dissim,
                              True, data_path, pc_path, var_path,
                              eigen_path, dropout_path, dissim_path), check=True).stderr)

    if dropout:
        _handle_dropout(a_data, layer, dropout_path)

    if dissim:
        _handle_dissim(a_data, layer, dissim_path)

    # If pc true in cidr function, then principal coordinates is put in a_data object.
    if pc:
        _handle_pc(a_data, layer, pc_path, var_path, eigen_path)

    # Makes sure to remove the temp files
    for path in [pc_path, var_path, eigen_path, dropout_path, dissim_path, data_path]:
        try:
            os.remove(path)
        except FileNotFoundError:
            pass

    print("Algorithm done. Plots are in cidr_plots.pdf")

def cidr_non_csv(a_data, layer="X", data_type="raw", n_cluster=None, dropout=False, dissim=False, pc=False):
    """
    Perform CIDR on any layer of an annData object, using in-memory RAM.
    This function is optimal if you are working with small datasets.

    .. warning::
        .. warning::
        For very large datasets this function can possibly time-out
        it is then recommended to use 'cidr' instead

    Args:
        adata (annData.AnnData): Input Anndata object containing expression data
        layer (str, optional): Name of the layer in 'a_data' to use. If "X", uses 'a_data.X'. Defaults to "X".
        data_type (str): Type of data ("raw" or "cpm")
        n_cluster (int or None): Number of clusters. If None, this is determined by the algorithm
        dropout (bool, optional): Determines whether to save dropout candidates into the annData object.
            These are saved in annData.uns. Defaults to False.
        dissim (bool, optional): Determines whether to save the dissimilarity matrix into the annData object.
            These are saved in annData.obsp. Defaults to False.
        pc (bool, optional): Determines whether to save the principle coordinates, proportion of variation
            and eigenvalue vectors into the annData object.
            These are saved in annData.obsm, annData.uns and annData.uns respectively. Defaults to False.

    Returns:
        None
    """
    # Run CIDR-clustering
    print("Algorithm Starting...")
    data = a_data.X if layer == "X" else a_data.layers[layer]
    sparse_matrix = csr_matrix(data, dtype=np.float32)
    input_data = _sparse_to_csv_using_buffer(sparse_matrix)
    # Runs the R-Script on the input_data
    result = subprocess.run(
        _make_args(data_type, n_cluster, pc, dropout, dissim, False),
        input=input_data.encode("utf-8"),
        check=True,
        stdout=subprocess.PIPE
    )

    output = result.stdout.decode("utf-8")

    if dropout:
        dropout_str, output = output.split("---END OF DROPOUT CANDIDATES---\n")
        _handle_dropout(a_data, layer, dropout_str, buffer=True)

    if dissim:
        dissim_str, output = output.split("---END OF DISSIMILARITY---\n")
        _handle_dissim(a_data, layer, dissim_str, buffer=True)

    # If pc true in cidr function, then principal coordinates it put in a_data object.
    if pc:
        pc_str, var_str = output.split("---END OF PC---\n")
        eigen_str, output = var_str.split("---END OF VARIATION---\n")
        _handle_pc(a_data, layer, pc_str, var_str, eigen_str, buffer=True)

    print("Algorithm done. Plots are in cidr_plots.pdf")