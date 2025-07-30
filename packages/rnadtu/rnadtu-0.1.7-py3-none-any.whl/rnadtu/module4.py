import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from scipy.sparse import csr_matrix  # type: ignore
import pyarrow as py
import subprocess
import os
from io import StringIO

run_state = {}

def _sparse_to_csv_using_buffer(sparse_matrix):
    array_matrix = sparse_matrix.toarray()
    df = pd.DataFrame(array_matrix)
    in_ram = StringIO()
    df.to_csv(in_ram, index=False)
    return in_ram.getvalue()

def _args_all(func_name, adata_id, layer_name, **kwargs):
    # Make an argumentlist to the R-script."
    script_path = os.path.join(os.path.dirname(__file__), "module5.R")

    args = ["Rscript",
            script_path,
            str(func_name),
            str(adata_id),
            str(layer_name)]

    for k, v in kwargs.items():
        args.append(f"--{k}={v}")

    return args


def _get_state(adata_id, layer):
    return run_state.setdefault((adata_id, layer), {
        "scDataConstructor": False,
        "determineDropoutCandidates": False,
        "wThreshold": False,
        "scDissim": False,
        "scPCA": False,
        "nPC": False,
        "nCluster": False,
        "scCluster": False
    })

CIDR_DEPENDENCIES = {
    "scDataConstructor": [],
    "determineDropoutCandidates": ["scDataConstructor"],
    "wThreshold": ["determineDropoutCandidates"],
    "scDissim": ["wThreshold"],
    "scPCA": ["scDissim"],
    "nPC": ["scPCA"],
    "nCluster": ["nPC"],
    "scCluster": ["nCluster"]
}

DEFAULT_ARGS = {
    "scDataConstructor": {
        "tagType": "raw"},
    "determineDropoutCandidates": {
        "min1": 3, "min2": 8, "N": 2000, "alpha": 0.1, "fast": True, "zerosOnly": False, "bw_adjust": 1},
    "wThreshold": {
        "cutoff": 0.5, "plotTornado": False},
    "scDissim": {
        "correction": False, "threads": 0, "useStepFunction": True},
    "scPCA": {
        "plotPC": True},
    "nCluster": {
        "n": None, "nPC": None, "cMethod": "ward.D2"},
    "scCluster": {
        "n": None, "nCluster": None, "nPC": None, "cMethod": "ward.D2"}
}

def _run_cidr_step(step, adata, layer="X",force=False, **kwargs):
    adata_id = id(adata)
    state = _get_state(adata_id, layer)

    for dep in CIDR_DEPENDENCIES.get(step, []):
        _run_cidr_step(dep, adata, layer)

    # Skip if the prevoius layerwas ran and it isn't foricng a rerun
    if state[step] and not force:
        return

    step_args = DEFAULT_ARGS.get(step, {}).copy()
    step_args.update(kwargs)

    input_data = None

    if step == "scDataConstructor":
        data = adata.X if layer == "X" else adata.layers[layer]
        input_data = _sparse_to_csv_using_buffer(csr_matrix(data, dtype=np.float32)).encode("utf-8")

    subprocess.run(
        _args_all(step, adata_id, layer, **step_args),
        input = input_data,
        check = True,
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT
    )

    state[step] = True
    _save_to_adata(adata, layer, step)

def _save_to_adata(adata, layer, step):
    if "cidr" not in adata.uns:
        adata.uns["cidr"] = {}
    if layer not in adata.uns["cidr"]:
        adata.uns["cidr"][layer] = {"steps_run": [], "results":{}}

    step_results = {}

    for file_name in os.listdir():
        if file_name.endswith(".parquet"):
            key = file_name.replace(".parquet", "")
            try:
                df = pd.read_parquet(file_name)

                if df.shape[1] > 1:
                    value = df.values

                elif df.shape[1] == 1:
                    value = df.iloc[:, 0].tolist()

                else:
                    value = df

                step_results[key] = value

                os.remove(file_name)

            except Exception as e:
                print(f"Could not read {file_name}: {e}")

    adata.uns["cidr"][layer]["results"][step] = step_results

    adata.uns["cidr"][layer]["steps_run"].append(step)

def cidr_scDataConstructor(a_data, layer="X", **kwargs):
    _run_cidr_step("scDataConstructor", a_data, layer=layer, **kwargs)

def cidr_determineDropoutCandidates(a_data, layer="X", **kwargs):
    _run_cidr_step("determineDropoutCandidates", a_data, layer=layer, **kwargs)

def cidr_wThreshold(a_data, layer="X", **kwargs):
    _run_cidr_step("wThreshold", a_data, layer=layer, **kwargs)

def cidr_scDissim(a_data, layer="X", **kwargs):
    _run_cidr_step("scDissim", a_data, layer=layer, **kwargs)


def cidr_scPCA(a_data, layer="X", **kwargs):
    _run_cidr_step("scPCA", a_data, layer=layer, **kwargs)


def cidr_nPC(a_data, layer="X", **kwargs):
    _run_cidr_step("nPC", a_data, layer=layer, **kwargs)


def cidr_nCluster(a_data, layer="X", **kwargs):
    _run_cidr_step("nCluster", a_data, layer=layer, **kwargs)


def cidr_scCluster(a_data, layer="X", **kwargs):
    _run_cidr_step("scCluster", a_data, layer=layer, **kwargs)
