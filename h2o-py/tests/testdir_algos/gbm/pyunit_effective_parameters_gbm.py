from __future__ import print_function
import sys
import h2o
sys.path.insert(1,"../../../")
from tests import pyunit_utils
from h2o.estimators.gbm import H2OGradientBoostingEstimator

#testing default setup of following parameters:
#distribution (available in Deep Learning, XGBoost, GBM):
#stopping_metric (available in: GBM, DRF, Deep Learning, AutoML, XGBoost, Isolation Forest):
#histogram_type (available in: GBM, DRF)
#solver (available in: GLM) already done in hex.glm.GLM.defaultSolver()
#categorical_encoding (available in: GBM, DRF, Deep Learning, K-Means, Aggregator, XGBoost, Isolation Forest)
#fold_assignment (available in: GBM, DRF, Deep Learning, GLM, Naïve-Bayes, K-Means, XGBoost)

def test_gbm_effective_parameters():
    cars = h2o.import_file(path=pyunit_utils.locate("smalldata/junit/cars_20mpg.csv"))
    cars["economy_20mpg"] = cars["economy_20mpg"].asfactor()
    cars["year"] = cars["year"].asfactor()
    predictors = ["displacement", "power", "weight", "acceleration", "year"]
    response = "economy_20mpg"
    train, valid = cars.split_frame(ratios=[.8], seed=1234)

    gbm1 = H2OGradientBoostingEstimator(seed=1234, stopping_rounds=3)
    gbm1.train(x=predictors, y=response, training_frame=train, validation_frame=valid)

    gbm2 = H2OGradientBoostingEstimator(seed=1234, stopping_rounds=3, distribution="bernoulli", stopping_metric="logloss",
                                        histogram_type="UniformAdaptive", categorical_encoding="Enum")
    gbm2.train(x=predictors, y=response, training_frame=train, validation_frame=valid)

    assert gbm1.logloss() == gbm2.logloss()
    assert gbm1.actual_params['distribution'] == gbm2.actual_params['distribution']
    assert gbm1.actual_params['stopping_metric'] == gbm2.actual_params['stopping_metric']
    assert gbm1.actual_params['histogram_type'] == gbm2.actual_params['histogram_type']
    assert gbm1.actual_params['stopping_metric'] == gbm2.actual_params['stopping_metric']
    assert gbm1.actual_params['categorical_encoding'] == gbm2.actual_params['categorical_encoding']


    gbm1 = H2OGradientBoostingEstimator(seed = 1234, nfolds=5)
    gbm1.train(x=predictors, y=response, training_frame=train, validation_frame=valid)

    gbm2 = H2OGradientBoostingEstimator(seed = 1234, nfolds=5, fold_assignment='Random', distribution="bernoulli",
                                        histogram_type="UniformAdaptive", categorical_encoding="Enum")
    gbm2.train(x=predictors, y=response, training_frame=train, validation_frame=valid)

    assert gbm1.logloss() == gbm2.logloss()
    assert gbm1.actual_params['distribution'] == gbm2.actual_params['distribution']
    assert gbm1.actual_params['stopping_metric'] is None
    assert gbm1.actual_params['histogram_type'] == gbm2.actual_params['histogram_type']
    assert gbm1.actual_params['fold_assignment'] == gbm2.actual_params['fold_assignment']
    assert gbm1.actual_params['categorical_encoding'] == gbm2.actual_params['categorical_encoding']

    frame = h2o.import_file(path=pyunit_utils.locate("smalldata/logreg/prostate.csv"))
    frame.pop('ID')
    frame[frame['VOL'],'VOL'] = None
    frame[frame['GLEASON'],'GLEASON'] = None
    r = frame.runif()
    train = frame[r < 0.8]
    test = frame[r >= 0.8]

    gbm = H2OGradientBoostingEstimator(ntrees=5, max_depth=3)
    gbm.train(x=list(range(2,train.ncol)), y="CAPSULE", training_frame=train, validation_frame=test)

    assert gbm.actual_params['categorical_encoding'] is None

if __name__ == "__main__":
  pyunit_utils.standalone_test(test_gbm_effective_parameters)
else:
    test_gbm_effective_parameters()
