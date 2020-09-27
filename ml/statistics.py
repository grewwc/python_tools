import scipy.stats as stats
import numpy as np
from collections import namedtuple
import pandas as pd
from functools import lru_cache
from python_tools.base.wwcABC import Helper
from python_tools.wwcFunctions import flatten
from copy import deepcopy


class LinearRegressionStats(Helper):
    def __init__(self, lm, X, y):
        self.lm = lm
        self.X = X
        self.y = y
        self._result = None
        self._RSS = None
        self._TSS = None
        self._RSE = None
        self._pred = None
        self._d_free = None
        self._std_squared = None
        if not hasattr(self.lm, 'intercept_'):
            self.lm.fit(X, y)
        self._params = flatten([self.lm.intercept_, *self.lm.coef_])
        self._X_add_constant = None

        # if X is pandas DataFrame, print the column names
        self._is_pandas_form = isinstance(X, pd.DataFrame)
        if self._is_pandas_form:
            self._columns = ['Intercept']
            self._columns.extend([name for name in X.columns])
        else:
            self._columns = None

    @property
    def params(self):
        return self._params

    @property
    def X_with_constant(self):
        if self._X_add_constant is None:
            self._X_add_constant = np.c_[np.ones(self.X.shape[0]), self.X]
        return self._X_add_constant

    @property
    def d_free(self):
        if self._d_free is None:
            self._d_free = self.X.shape[0] - self.X.shape[1] - 1
            return self._d_free
        else:
            return self._d_free

    @property
    def RSS(self):
        if self._RSS is None:
            self._RSS = sum((self.y-self.pred)**2)
        return self._RSS

    @property
    def pred(self):
        if self._pred is None:
            self._pred = self.lm.predict(self.X)
        return self._pred

    @property
    def TSS(self):
        if self._TSS is None:
            self._TSS = sum((self.y - self.y.mean())**2)
        return self._TSS

    @property
    def RSE(self):
        if self._RSE is None:
            self._RSE = np.sqrt(self.RSS / self.d_free)
        return self._RSE

    @property
    def std_squared(self):
        if self._std_squared is None:
            RSS_per_degree = self.RSE ** 2
            X_add_constant = self.X_with_constant
            self._std_squared = RSS_per_degree * \
                self._get_inv_matrix_helper().diagonal()

        return self._std_squared

    @property
    @lru_cache()
    def std(self):
        return np.sqrt(self.std_squared)

    @property
    @lru_cache()
    def summary(self):
        if self._result is None:
            result = namedtuple(
                'result', 'std p_values R_square t_statistic F_statistic')
            pred = self.pred
            params = self.params
            d_free = self.d_free
            y_mean = self.y.mean()
            RSS = self.RSS
            TSS = self.TSS
            RSS_per_degree = self.RSE ** 2
            t_dist = stats.t(d_free)
            std_squared = self.std_squared
            t_statistics = params / np.sqrt(std_squared)
            p_values = [2 * t_dist.sf(abs(i)) for i in t_statistics]
            f_statistics = ((TSS - RSS)/self.X.shape[1]) / RSS_per_degree
            R_square = 1 - RSS / TSS
            self._result = result(std=self.std, p_values=p_values, t_statistic=t_statistics,
                                  F_statistic=f_statistics, R_square=R_square)
        return self._result

    @lru_cache()
    def get_estimators_confidence_interval(self, conf_level=0.95):
        """
        two-sided
        """
        alpha = 1 - conf_level
        X_add_constant = self.X_with_constant
        std_squared = self.std_squared
        t_dist = stats.t(self.d_free)
        length = np.sqrt(std_squared) * t_dist.ppf(1-alpha/2)
        return list(zip(self.params, length))

    @lru_cache()
    def _get_inv_matrix_helper(self):
        inv_mat = np.linalg.inv(self.X_with_constant.T.dot(
            self.X_with_constant
        ))
        return inv_mat

    def __get_y_interval_helper(self, X, conf_level=0.95, prediction=False):
        import python_tools.wwcFunctions as wwcFunctions
        X = np.array(X).reshape(1, -1)
        X_add_constant = np.array([1, *wwcFunctions.flatten(X)]).reshape(1, -1)
        t_dist = stats.t(self.d_free)
        inv_mat = self._get_inv_matrix_helper()
        alpha = 1 - conf_level
        residual = 0 if not prediction else 1
        err = t_dist.ppf(1-alpha/2.0) * \
            self.RSE * (np.sqrt(X_add_constant.dot(
                inv_mat).dot(X_add_constant.T) + residual))
        return (*wwcFunctions.flatten(self.lm.predict(X)),
                *wwcFunctions.flatten(err))

    def get_y_confidence_interval(self, X, conf_level=0.95):
        """
        two-sided
        """
        return self.__get_y_interval_helper(X, conf_level, False)

    def get_y_prediction_inverval(self, X, conf_level=0.95):
        """
        two-sided
        """
        return self.__get_y_interval_helper(X, conf_level, True)

    def __getitem__(self, key):
        try:
            return getattr(self.summary, key)
        except AttributeError as e:
            print(e)

    def __str__(self):
        d = self.summary._asdict()
        if not self._is_pandas_form:
            test = {k: value for k, value in d.items()}
            return '\n'.join('{} : {}'.format(k, v) for k, v in d.items())
        else:
            p_values_and_t_stats = {'Estimate': self.params,
                                    'Std. Error': self.std,
                                    'p-values': self.summary.p_values,
                                    't-statistic': self.summary.t_statistic}

            res = pd.DataFrame(data=p_values_and_t_stats,
                               index=self._columns)

            return ('{stats}\n\nR^2: {R_square:.5f}\n'
                    'F-statistic: {F_statistic:.5f}').format(
                stats=res,
                R_square=self.summary.R_square,
                F_statistic=self.summary.F_statistic
            )


class LogisticRegressionStats(Helper):
    def __init__(self, model, X, y):
        self.model, self.X, self.y = model, X, y
        self._design_matrix = None
        self._std_err = None
        self._cov_matrix = None
        self._z_statistic = None
        self._p_values = None
        self._params = np.array(flatten([model.intercept_, *model.coef_]))
        self._pandas = False if not isinstance(X, pd.DataFrame) else True

    @property
    def params(self):
        return self._params

    @property
    def design_matrix(self):
        if self._design_matrix is None:
            self._design_matrix = \
                np.c_[np.ones(self.X.shape[0]), self.X]
        return self._design_matrix

    @property
    def cov_matrix(self):
        if self._cov_matrix is None:
            prob_true, prob_false =\
                self.model.predict_proba(self.X).T
            V = np.eye(self.X.shape[0]) * prob_false * prob_true
            self._cov_matrix = np.linalg.inv(self.design_matrix.T.dot(
                V).dot(self.design_matrix))
        return self._cov_matrix

    def __construct_dataframe(self, data, columns):
        return pd.DataFrame(
            data=np.c_[self._params.reshape(-1, 1), data.reshape(-1, 1)],
            columns=columns,
            index=['Intercept', *self.X.columns])

    def __get_value_from_dataframe(self, df):
        if not isinstance(df, pd.DataFrame):
            return df.reshape(-1, 1)
        return df[df.columns[1:]].values

    @property
    def std_err(self):
        if self._std_err is None:
            self._std_err = np.sqrt(self.cov_matrix.diagonal())
            if self._pandas:
                columns = ['Coefficient', 'Std. error']
                data = self._std_err
                self._std_err = self.__construct_dataframe(data, columns)
        return self._std_err

    @property
    def z_statistic(self):
        if self._z_statistic is None:
            self._z_statistic = self.params.reshape(-1, 1) / \
                self.__get_value_from_dataframe(self.std_err)
            if self._pandas:
                columns = ['Coefficient', 'Z-statistic']
                data = self._z_statistic
                self._z_statistic = self.__construct_dataframe(data, columns)
            else:
                self._z_statistic = self._z_statistic.reshape(1, -1)
        return self._z_statistic

    @property
    def p_values(self):
        if self._p_values is None:
            self.__z = stats.norm()
            z_statistic = self.__get_value_from_dataframe(self.z_statistic)
            self._p_values = \
                np.array([2 * self.__z.sf(abs(x)) for x in z_statistic])
            if self._pandas:
                data = self._p_values
                columns = ['Coefficient', 'p-values']
                self._p_values = self.__construct_dataframe(data, columns)
        return self._p_values

    @property
    def summary(self):
        if self._pandas:
            return pd.merge(self.std_err, self.z_statistic, on='Coefficient',
                            left_index=True).merge(
                self.p_values, on='Coefficient', left_index=True)
        else:
            return {'Coefficient': self.params,
                    'Std. error': self.std_err,
                    'Z-statistic': np.array(flatten(self.z_statistic)),
                    'p-values': np.array(flatten(self.p_values.reshape(1, -1)))}


class Bootstrap(Helper):
    """
    B: bootstrap times
    calculate "estimated value" and "standard error" of estimators
    """

    def __init__(self, model, X, y, B=100, random_state=None):
        self.B = B
        self.model = deepcopy(model)
        self.X = X
        self.y = y
        if random_state:
            np.random.seed(random_state)
        self.__all_samples = np.zeros((self.B, len(model.coef_)+1))

    def __get_params(self, model):
        return np.array(flatten([model.intercept_, model.coef_]))

    def __bootstrap_once(self, ith):
        args = np.random.choice(range(len(self.y)), size=len(self.y))
        cur_X, cur_y = self.X[args], self.y[args]
        self.model.fit(cur_X, cur_y)
        self.__all_samples[ith] = self.__get_params(self.model)

    @property
    @lru_cache()
    def prediction(self):
        for i in range(self.B):
            self.__bootstrap_once(i)
        return self.__all_samples.mean(axis=0)

    @property
    @lru_cache()
    def std(self):
        return np.sqrt(((self.__all_samples-self.prediction)**2).
                       sum(axis=0) / (self.B-1))

    @property
    @lru_cache()
    def summary(self):
        return {'prediction': self.prediction,
                'Std. Error': self.std}


