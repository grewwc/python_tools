from sklearn.linear_model import LinearRegression
import numpy as np
from .statistics import LinearRegressionStats
import pandas as pd 

def calc_vif(X):
    if isinstance(X, pd.DataFrame):
        X = X.values
    lm = LinearRegression()
    res = []
    for j in range(X.shape[1]):
        target = X[:, j]
        from python_tools.wwcFunctions import numpy_array_exclude
        predictors = numpy_array_exclude(X, j, axis=1)
        lm.fit(np.array(predictors), np.array(target))
        lm_stats = LinearRegressionStats(lm, predictors, target)
        R_square = lm_stats['R_square']
        res.append(1/(1-R_square))
    return res
