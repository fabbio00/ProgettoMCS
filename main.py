import numpy as np
from scipy.io import mmread
import json
import gradiente as gr
import gauss_seidel as gs
import jacobi as ja
import gradiente_coniugato as grc

# Import Data
data = {
    "spa1": 0,
    "spa2": 0,
    "vem1": 0,
    "vem2": 0}
for x in data:
    data[x] = {
        "A": mmread("data/" + x + ".mtx").tocsr(),  # Reading A
        "x": 0,
        "b": 0,
    }
    # Create correct vector X
    data[x]["x"] = np.array([1.0]*data[x]["A"].get_shape()[0])
    data[x]["b"] = np.array(data[x]["A"].dot(
        data[x]["x"]))  # Calcolate solution b

# Tolleranze
tols = [10**(-4), 10**(-6), 10**(-8), 10**(-10)]

# Import solvers library in a dictionary
solver = {}
solver["Jacobi"] = ja
solver["Gauss-Seidel"] = gs
solver["Gradiente"] = gr
solver["Gradiente Coniugato"] = grc

# Calculate all results
resTot = {}
for metod in solver:
    resTot[metod] = {}
    for el in data:
        resTot[metod][el] = []
        for tol in tols:
            res = solver[metod].solve(
                data[el]["A"], data[el]["b"], data[el]["x"], tol)
            resTot[metod][el].append({
                "tol": tol,
                "nIter": res["nIter"],
                "time": res["time"],
                "eRel": res["eRel"]
            })
print(resTot)

out_file = open("Results.json", "w")
json.dump(resTot, out_file, indent=4)
