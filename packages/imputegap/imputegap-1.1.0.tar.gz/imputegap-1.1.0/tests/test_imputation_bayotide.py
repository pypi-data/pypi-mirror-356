import unittest
from imputegap.recovery.imputation import Imputation
from imputegap.tools import utils
from imputegap.recovery.manager import TimeSeries

class TestBayOTIDE(unittest.TestCase):

    def test_imputation_bayotide_dft(self):
        """
        the goal is to test if only the simple imputation with BayOTIDE has the expected outcome
        """
        ts_1 = TimeSeries()
        ts_1.load_series(utils.search_path("eeg-alcohol"))
        ts_1.normalize(normalizer="min_max")

        incomp_data = ts_1.Contamination.mcar(ts_1.data)

        algo = Imputation.DeepLearning.BayOTIDE(incomp_data).impute()

        algo.score(ts_1.data)
        metrics = algo.metrics

        ts_1.print_results(algo.metrics, algo.algorithm)

        print(f"{metrics = }")

        expected_metrics = { "RMSE": 0.40144229748963356, "MAE": 0.2698883191201369, "MI": 0.2132034412544277, "CORRELATION": 0.22804454705607724 }

        self.assertTrue(abs(metrics["RMSE"] - expected_metrics["RMSE"]) < 0.2,
                       f"metrics RMSE = {metrics['RMSE']}, expected RMSE = {expected_metrics['RMSE']} ")
        self.assertTrue(abs(metrics["MAE"] - expected_metrics["MAE"]) < 0.2,
                        f"metrics MAE = {metrics['MAE']}, expected MAE = {expected_metrics['MAE']} ")
        self.assertTrue(abs(metrics["MI"] - expected_metrics["MI"]) < 0.3,
                        f"metrics MI = {metrics['MI']}, expected MI = {expected_metrics['MI']} ")
        self.assertTrue(abs(metrics["CORRELATION"] - expected_metrics["CORRELATION"]) < 0.3,
                        f"metrics CORRELATION = {metrics['CORRELATION']}, expected CORRELATION = {expected_metrics['CORRELATION']} ")


    def test_imputation_bayotide_udef(self):
        """
        the goal is to test if only the simple imputation with BayOTIDE has the expected outcome
        """
        ts_1 = TimeSeries()
        ts_1.load_series(utils.search_path("eeg-alcohol"))
        ts_1.normalize(normalizer="min_max")

        incomp_data = ts_1.Contamination.mcar(ts_1.data)

        algo = Imputation.DeepLearning.BayOTIDE(incomp_data).impute(user_def=True,
                                                                    params={"K_trend": 20, "K_season": 1, "n_season": 5,
                                                                            "K_bias": 1, "time_scale": 1, "a0": 0.6,
                                                                            "b0": 2.5,
                                                                            "v": 0.5, "tr_ratio": 0.6})
        algo.score(ts_1.data, algo.recov_data)
        metrics = algo.metrics

        ts_1.print_results(algo.metrics, algo.algorithm)

        expected_metrics = { "RMSE": 0.5262297665671618, "MAE": 0.36044004971872423, "MI": 0.14369092974417427, "CORRELATION": 0.024903849145994666 }

        self.assertTrue(abs(metrics["RMSE"] - expected_metrics["RMSE"]) < 0.2,
                       f"metrics RMSE = {metrics['RMSE']}, expected RMSE = {expected_metrics['RMSE']} ")
        self.assertTrue(abs(metrics["MAE"] - expected_metrics["MAE"]) < 0.2,
                        f"metrics MAE = {metrics['MAE']}, expected MAE = {expected_metrics['MAE']} ")
        self.assertTrue(abs(metrics["MI"] - expected_metrics["MI"]) < 0.3,
                        f"metrics MI = {metrics['MI']}, expected MI = {expected_metrics['MI']} ")
        self.assertTrue(abs(metrics["CORRELATION"] - expected_metrics["CORRELATION"]) < 0.3,
                        f"metrics CORRELATION = {metrics['CORRELATION']}, expected CORRELATION = {expected_metrics['CORRELATION']} ")
