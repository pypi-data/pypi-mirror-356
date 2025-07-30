# rnadtu

A Python package for running the CIDR algorithm (originally implemented in R) for clustering single-cell RNA-seq data using `AnnData` objects.

## Features

- Run the CIDR algorithm from Python using:

  - **`cidr()`** — subprocess-based, using temporary CSV files (recommended for large datasets)
  - **`cidr_non_csv()`** — subprocess-based, using in-memory buffers (faster but memory intensive and difficult to debug)
  - **`cidr_rpy2()`** — uses the `rpy2` bridge (direct R integration, less suitable for large datasets)

- Optional configuration options:

  - `data_type`: default is `"raw"`, can be `"cpm"` (counts per million)
  - `n_cluster`: default is `None` (CIDR calculates the optimal number), or manually specify an positive integer
  - `layer`: which layer of the `AnnData` object to use for input
  - Optional output controls:
    - `pc`: store principal coordinates
    - `dissim`: store dissimilarity matrix
    - `dropout`: store dropout matrix
    - `save_clusters`: (only in cidr_rpy2) choose store cluster labels (default `True`)

- Results are saved in the `AnnData` object:

  - `obsm[layer + "_cidr_pc"]` — principal components
  - `obsm[layer + "_cidr_clusters"]` — cluster labels (if `save_clusters=True`)
  - `obsp[layer + "_cidr_dissimilarity_matrix"]` — pairwise distances
  - `uns[layer + "_cidr_variation"]`, `uns[layer + "_cidr_eigenvalues"]` — PCA variation
  - `uns[layer + "_cidr_dropout_candidates"]` — dropout data

- Generates a clustering plot in `cidr_plots.pdf`

### Installation

```bash
pip install rnadtu
```
