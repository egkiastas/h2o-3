from __future__ import print_function
import sys
import h2o
sys.path.insert(1,"../../../")
from tests import pyunit_utils
from h2o.estimators.isolation_forest import H2OIsolationForestEstimator

#testing default setup of following parameters:
#distribution (available in Deep Learning, XGBoost, GBM):
#stopping_metric (available in: GBM, DRF, Deep Learning, AutoML, XGBoost, Isolation Forest):
#histogram_type (available in: GBM, DRF)
#solver (available in: GLM) already done in hex.glm.GLM.defaultSolver()
#categorical_encoding (available in: GBM, DRF, Deep Learning, K-Means, Aggregator, XGBoost, Isolation Forest)
#fold_assignment (available in: GBM, DRF, Deep Learning, GLM, Naïve-Bayes, K-Means, XGBoost)


def test_isolation_forrest_effective_parameters():
    train2 = h2o.import_file(pyunit_utils.locate("smalldata/anomaly/ecg_discord_train.csv"))

    if1 = H2OIsolationForestEstimator(ntrees=7, seed=12, sample_size=5, stopping_rounds=3)
    if1.train(training_frame=train2)

    if2 = H2OIsolationForestEstimator(ntrees=7, seed=12, sample_size=5, stopping_rounds=3, stopping_metric = 'anomaly_score', categorical_encoding="Enum")
    if2.train(training_frame=train2)

    assert if1.effective_params['stopping_metric'] == if2.actual_params['stopping_metric']
    assert if1._model_json['output']['training_metrics']._metric_json['mean_score'] == if2._model_json['output']['training_metrics']._metric_json['mean_score']
    assert if1.effective_params['categorical_encoding'] == if2.effective_params['categorical_encoding']

if __name__ == "__main__":
  pyunit_utils.standalone_test(test_isolation_forrest_effective_parameters)
else:
    test_isolation_forrest_effective_parameters()
