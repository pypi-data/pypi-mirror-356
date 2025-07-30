"""
write_data.py
This file defines functions to write updated spatialdata objects back to the original raw VisiumHD output form.
Some libraries, like FICTURE, want the original output folder as the input.
"""
import os
import pandas as pd
from scipy.io import mmwrite

def write_2um_filtered_counts(sdata, raw_folder_path):
    """
    Function that writes the filtered/destriped 2um counts back to the original HD folder.
    This is primarily intended to run after the destriping command ONLY.
    NOTE: this assumes gene list and barcodes unmodified.

    Args:
    sdata: the updated spatialdata object
    raw_folder_path: the raw VisiumHD folder (outermost directory)
    """
    adata = sdata.tables["square_002um"] # extract data
    # define folders and file paths
    matrix_dir = os.path.join(
        raw_folder_path,
        "outs/binned_outputs/square_002um/filtered_feature_bc_matrix"
    )
    barcodes_path = os.path.join(matrix_dir, "barcodes.tsv.gz")
    features_path = os.path.join(matrix_dir, "features.tsv.gz")
    matrix_path = os.path.join(matrix_dir, "matrix.mtx")

    # Load and validate barcode/gene information
    old_barcodes = pd.read_csv(barcodes_path, sep="\t", header=None).iloc[:, 0]
    old_genes = pd.read_csv(features_path, sep="\t", header=None).iloc[:, 1]

    assert (adata.obs_names == old_barcodes.values).all(), "Barcodes do not match!"
    assert (adata.var_names == old_genes.values).all(), "Gene names do not match!"

    # Write updated count matrix
    mmwrite(matrix_path, adata.X)