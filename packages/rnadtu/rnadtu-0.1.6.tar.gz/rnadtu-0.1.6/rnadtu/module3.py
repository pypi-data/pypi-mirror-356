"""
CIDR-Clustering Integration for annData using Rpy2

This module provides a Python function for the R-based CIDR algorithm for clustering
single-cell RNA-seq data using Rpy2.

Functions
cidr_rpy2: Memory-based CIDR clustering.
"""
import numpy as np

def cidr_rpy2(a_data, layer="X", data_type="raw", n_cluster=None, pc=False, save_clusters=True):
    """
    This function performs CIDR in R using an approach based on Python's Rpy2 package which is meant to interface
    with R through C scripts.

    Args:
        a_data (annData.AnnData): The anndata object containing expression data
        layer (str, optional): Name of the layer in 'a_data' to use. If "X", uses 'a_data.X'. Defaults to "X".
        data_type (str): Type of data ("raw" or "cpm")
        n_cluster (int or None): Number of clusters. If None, this is determined by the algorithm
        pc (bool, optional): Determines whether to save the principle coordinates, proportion of variation
            and eigenvalue vectors into the annData object.
            These are saved in annData.obsm, annData.uns and annData.uns respectively. Defaults to False.
        save_clusters (bool, optional): Determines whether to return clustering coordinates for different cells to the 
            annData object. These are saved into annData.obsm. Defaults to True.

    Returns:
        None
    """
    # Runs CIDR algorithm with rpy2.
    # The lines that start with ro.r is a way of running R-code in python.

    # Import of rpy2 is set here instead on top of module, making it possible to import the package
    # without needing to install rpy2, since this package might not always compile in a windows environment.

    try:
        import rpy2.robjects as ro
        from rpy2.robjects import pandas2ri
        from rpy2.robjects.packages import importr
        from rpy2.robjects import numpy2ri
        from rpy2.robjects.conversion import localconverter
        import rpy2.robjects as ro
    except ImportError:
        raise ImportError("rpy2 must be installed to use 'cidr_rpy2'")

    # Imports the CIDR package installed in R.
    cidr = importr("cidr")

    data = a_data.X if layer == "X" else a_data.layers[layer]
    dense_matrix = _to_dense_array(data)

    with localconverter(ro.default_converter + numpy2ri.converter):
        r_matrix = ro.conversion.py2rpy(dense_matrix)

    ro.globalenv['data_matrix'] = r_matrix
    ro.r('data_object <- as.matrix(data_matrix)')
    ro.globalenv['data_type'] = data_type
    ro.r('''if (data_type == "cpm"){
            cidr_obj <- scDataConstructor(t(data_object), tagType="cpm")
            } else {
            cidr_obj <- scDataConstructor(t(data_object))
            }''')
    print("Object created (1/8)")
    ro.r('cidr_obj <- determineDropoutCandidates(cidr_obj)')
    print("Determined dropout candidates (2/8)")
    ro.r('cidr_obj <- wThreshold(cidr_obj)')
    print("Determined threshold (3/8)")
    ro.r('cidr_obj <- scDissim(cidr_obj)')
    print("Created dissimilaity matrix (4/8)")
    ro.r('pdf("cidr_plots.pdf")')
    ro.r('cidr_obj <- scPCA(cidr_obj)')
    print("Finished principal component analysis (5/8)")
    ro.r('cidr_obj <- nPC(cidr_obj)')
    print("Determined number of principal components (6/8)")

    # If n_cluster, then it chooses n_cluster as amount of clusters, otherwise
    # letting the algorithm choose.
    if n_cluster == None:
        ro.r('cidr_obj <- scCluster(cidr_obj)')
    else:
        ro.globalenv['n_cluster'] = n_cluster
        ro.r('cidr_obj <- scCluster(cidr_obj, nCluster=as.integer(n_cluster))')

    print("Finished clustering (7/8)")
    ro.r('''
    plot(cidr_obj@PC[, c(1, 2)],
      col = cidr_obj@clusters,
      pch = cidr_obj@clusters,
      main = "CIDR Clustering",
      xlab = "PC1", ylab = "PC2"
    )
    dev.off()
    ''')
    print("Plot done (8/8)")

    # If save_clusters, then the clusters are saved in the a_data object.
    if save_clusters == True:
        clusters = ro.r('as.data.frame(cidr_obj@clusters)')
    
        from rpy2.robjects.conversion import localconverter
        from rpy2.robjects import default_converter

        with localconverter(default_converter + pandas2ri.converter):
            clusters_df = ro.conversion.rpy2py(clusters)

        a_data.obsm[layer + '_cidr_clusters'] = clusters_df.values

    # If pc true in cidr function, then principal coordinates it put in a_data object.
    if pc == True:
        pcs = ro.r('as.data.frame(cidr_obj@PC)')
        variation = ro.r('as.data.frame(cidr_obj@PC)')

        from rpy2.robjects.conversion import localconverter
        from rpy2.robjects import default_converter

        with localconverter(default_converter + pandas2ri.converter):
            pcs_df = ro.conversion.rpy2py(pcs)
            variation_df = ro.conversion.rpy2py(variation)

        # Chooses the layer in which you save the principal coordinates.

        a_data.obsm[layer + '_cidr_pca'] = pcs_df.values
        a_data.uns[layer + '_variation'] = variation_df

        print("Algorithm done. Plots are in cidr_plots.pdf")

# This function should handle most data types w.r.t the annData object
def _to_dense_array(data, dtype=np.float32):
    if hasattr(data, "toarray"):
        intermediate = data.toarray()
    else:
        intermediate = data

    dense_array = np.asarray(intermediate, dtype=dtype)
    return dense_array

