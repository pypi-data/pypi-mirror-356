from imputegap.recovery.imputation import Imputation
from imputegap.recovery.manager import TimeSeries
from imputegap.tools import utils

# initialize the time series object
ts = TimeSeries()
print(f"Imputation algorithms : {ts.algorithms}")

# load and normalize the dataset
ts.load_series(utils.search_path("chlorine"))
ts.normalize(normalizer="z_score")

# contaminate the time series
ts_m = ts.Contamination.mcar(ts.data)

algos = ["MPIN", "PRISTI", "GAIN", "GRIN", "BayOTIDE", "HKMF_T", "BitGraph"]
#algos = ["MeanImpute", "CDRec"]
results = []
for a in algos:
    print(f"Algorithm : {a}")
    imputer = utils.config_impute_algorithm(ts_m, a, verbose=True)
    imputer.impute()

    # compute and print the imputation metrics
    imputer.score(ts.data, imputer.recov_data)
    ts.print_results(imputer.metrics)
    results.append((a, imputer.metrics))

print("\n")
for al, r in results:
    print(f"{al}: {r}")


