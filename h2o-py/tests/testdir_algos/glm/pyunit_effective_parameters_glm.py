from __future__ import print_function
import sys
import h2o
import random
sys.path.insert(1,"../../../")
from tests import pyunit_utils
from h2o.estimators.glm import H2OGeneralizedLinearEstimator

#testing default setup of following parameters:
#distribution (available in Deep Learning, XGBoost, GBM):
#stopping_metric (available in: GBM, DRF, Deep Learning, AutoML, XGBoost, Isolation Forest):
#histogram_type (available in: GBM, DRF)
#solver (available in: GLM) already done in hex.glm.GLM.defaultSolver()
#categorical_encoding (available in: GBM, DRF, Deep Learning, K-Means, Aggregator, XGBoost, Isolation Forest)
#fold_assignment (available in: GBM, DRF, Deep Learning, GLM, Naïve-Bayes, K-Means, XGBoost)


def test_glm_effective_parameters():
    cars = h2o.import_file(path=pyunit_utils.locate("smalldata/junit/cars_20mpg.csv"))
    predictors = ["displacement","power","weight","acceleration","year"]
    response_col = "economy_20mpg"
    family = "binomial"
    cars[response_col] = cars[response_col].asfactor()
    nfolds = random.randint(3,10)

    glm = H2OGeneralizedLinearEstimator(nfolds=nfolds, family=family)
    glm.train(x=predictors, y=response_col, training_frame=cars)
    assert glm.effective_params['fold_assignment'] == "Random"

if __name__ == "__main__":
  pyunit_utils.standalone_test(test_glm_effective_parameters)
else:
    test_glm_effective_parameters()
