from __future__ import print_function
import sys
sys.path.insert(1,"../../../")
from tests import pyunit_utils
from h2o.estimators.xgboost import *

#testing default setup of following parameters:
#distribution (available in Deep Learning, XGBoost, GBM):
#stopping_metric (available in: GBM, DRF, Deep Learning, AutoML, XGBoost, Isolation Forest):
#histogram_type (available in: GBM, DRF)
#solver (available in: GLM) already done in hex.glm.GLM.defaultSolver()
#categorical_encoding (available in: GBM, DRF, Deep Learning, K-Means, Aggregator, XGBoost, Isolation Forest)
#fold_assignment (available in: GBM, DRF, Deep Learning, GLM, Naïve-Bayes, K-Means, XGBoost)

def test_xgboost_effective_parameters():
    assert H2OXGBoostEstimator.available()

    prostate_frame = h2o.import_file(pyunit_utils.locate('smalldata/prostate/prostate.csv'))
    x = ['RACE']
    y = 'CAPSULE'
    prostate_frame[y] = prostate_frame[y].asfactor()
    prostate_frame.split_frame(ratios=[0.75], destination_frames=['prostate_training', 'prostate_validation'], seed=1)
    training_frame = h2o.get_frame('prostate_training')
    test_frame = h2o.get_frame('prostate_validation')

    xgb1 = H2OXGBoostEstimator(training_frame=training_frame, learn_rate=0.7, booster='gbtree', seed=1, ntrees=2, stopping_rounds=5)
    xgb1.train(x=x, y=y, training_frame=training_frame, validation_frame=test_frame)

    xgb2 = H2OXGBoostEstimator(training_frame=training_frame, learn_rate=0.7, booster='gbtree', seed=1, ntrees=2, distribution="bernoulli",
                               categorical_encoding="OneHotInternal", stopping_rounds =5, stopping_metric='logloss')
    xgb2.train(x=x, y=y, training_frame=training_frame, validation_frame=test_frame)

    assert xgb1.actual_params['distribution'] == xgb2.actual_params['distribution']
    assert xgb1.logloss() == xgb2.logloss()
    assert xgb1.actual_params['stopping_metric'] == xgb2.actual_params['stopping_metric']
    assert xgb1.actual_params['categorical_encoding'] == xgb2.actual_params['categorical_encoding']
    assert xgb1.actual_params['fold_assignment'] is None


    xgb1 = H2OXGBoostEstimator(training_frame=training_frame, learn_rate=0.7, booster='gbtree', seed=1, ntrees=2, nfolds=5)
    xgb1.train(x=x, y=y, training_frame=training_frame)

    xgb2 = H2OXGBoostEstimator(training_frame=training_frame, learn_rate=0.7, booster='gbtree', seed=1, ntrees=2, distribution="bernoulli",
                               categorical_encoding="OneHotInternal", nfolds=5, fold_assignment="Random")
    xgb2.train(x=x, y=y, training_frame=training_frame)

    assert xgb1.actual_params['distribution'] == xgb2.actual_params['distribution']
    assert xgb1.logloss() == xgb2.logloss()
    assert xgb1.actual_params['stopping_metric'] is None
    assert xgb1.actual_params['categorical_encoding'] == xgb2.actual_params['categorical_encoding']
    assert xgb1.actual_params['fold_assignment'] == xgb2.actual_params['fold_assignment']

if __name__ == "__main__":
  pyunit_utils.standalone_test(test_xgboost_effective_parameters)
else:
    test_xgboost_effective_parameters()
