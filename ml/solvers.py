import numpy as np
from python_tools.base.wwcABC import Helper
from python_tools.ml.errors.OperationException import OperationError
from python_tools.wwcFunctions import flatten
import sys


class BaseSolver(Helper):
    def __init__(self, lr=1e-3, num_epochs=100):
        self.lr = lr
        self.num_epochs = num_epochs
        self._fitted = False
        self._theta = None

    def fit(self, X, y):
        return NotImplemented

    def predict(self, X):
        if not self._fitted:
            raise OperationError('not fit yet')
        X = self._add_const_x(self._to_column_vec(X))
        return X.dot(self.theta)

    def _reshape_X_y(self):
        self.X = self._add_const_x(self._to_column_vec(self.X))
        self.y = self._to_column_vec(self.y)

    def gradient(self, X, y, theta=None):
        if theta is None:
            theta = self._theta
        return X.T.dot(X.dot(theta) - y) / len(y)

    @property
    def theta(self):
        '''
        each "row" represents a set of parameters
        '''
        if self._theta.shape[1] == 1:
            return np.array(flatten(self._theta))
        return self._theta


class GradientDescent(BaseSolver):
    def __init__(self, lr=1e-3, num_epochs=100):
        super().__init__(lr=lr, num_epochs=num_epochs)
        self._theta = None

    def __set_data(self, X, y):
        self.X, self.y = X.copy(), y.copy()
        self._reshape_X_y()
        self._theta = np.random.randn(self.X.shape[1]).reshape(-1, 1)
        self.X_t = self.X.T

    def gradient(self):
        delta = self.X_t.dot(self.X.dot(self._theta) - self.y)
        return delta / len(self.y)

    def _update(self):
        delta = self.gradient()
        self._theta -= self.lr * delta
        return None

    @property
    def theta(self):
        return super().theta

    def fit(self, X, y):
        self.__set_data(X, y)
        i = 0
        max_delta_elem = self._update()
        for i in range(self.num_epochs):
            self._update()
        self._fitted = True


class SGD(BaseSolver):
    def __init__(self, lr=1e-3, batch_size=1, num_epochs=100):
        super().__init__(lr=lr, num_epochs=num_epochs)
        self.batch_size = batch_size

    def _get_mini_batches(self):
        X, y = self.X, self.y
        if (self.batch_size is None) or (self.batch_size > X.shape[0]):
            self.batch_size = X.shape[0]
        bs = self.batch_size
        y_len = len(y)
        shuffled_index = np.random.choice(y_len, y_len, replace=False)
        X_shuffled, y_shuffled = X[shuffled_index], y[shuffled_index]
        return ((X_shuffled[i:i+bs, :], y_shuffled[i:i+bs, :])
                for i in range(0, y_len, bs))

    def _update(self, X, y):
        dL_dw = self.gradient(X, y)
        self._theta -= self.lr * dL_dw
        return None

    def fit(self, X, y):
        self.X, self.y = X.copy(), y.copy()
        self._reshape_X_y()
        X, y = self.X, self.y
        self._theta = np.random.randn(X.shape[1], y.shape[1])\
            / np.sqrt(X.shape[1])
        for cur_epoch in range(self.num_epochs):
            mini_batches = self._get_mini_batches()
            for X_batch, y_batch in mini_batches:
                self._update(X_batch, y_batch)
        self._fitted = True


class SGDMomentum(SGD):
    def __init__(self, lr=1e-3, alpha=0.9, batch_size=10,
                 num_epochs=100):
        """
        V(t) = alpha * V(t-1) + (1-alpha) * dL/dW(t-1)
        W = W - lr * V(t) 
        where L is "Loss function"
        """
        super().__init__(lr=lr, num_epochs=num_epochs, batch_size=batch_size)
        self.alpha = alpha
        self._velocity = None

    def _update(self, X, y):
        dL_dw = self.gradient(X, y)
        alpha = self.alpha
        if self._velocity is None:
            self._velocity = np.zeros_like(self._theta)

        self._velocity = alpha * self._velocity + (1-alpha) * dL_dw
        self._theta -= self.lr * self._velocity
        return None


class NAG(SGD):
    def __init__(self, lr=0.001, alpha=0.9, batch_size=10, num_epochs=100):
        """
        V(t) = alpha * V(t-1) - (1-alpha) * dL/dW(t)
        W = W + lr * V(t) 

        where L is "Loss function"
        """
        super().__init__(lr=lr, batch_size=batch_size, num_epochs=num_epochs)
        self.alpha = alpha
        self._velocity = None

    def _update(self, X, y):
        if self._velocity is None:
            self._velocity = np.zeros_like(self._theta)
        alpha = self.alpha
        dL_dw = self.gradient(X, y)
        next_theta = self._theta + self.lr * self._velocity
        dL_dw = self.gradient(X, y, next_theta)
        self._velocity = alpha * self._velocity - (1-alpha) * dL_dw
        self._theta += self.lr * self._velocity
        return None


class AdaGrad(SGD):
    def __init__(self, lr=0.001, eps=1e-8, batch_size=10, num_epochs=100):
        """
        W = W - lr/sqrt(eps+(dL/dW)^2) * dL/dW

        Note: dL/dW is a vector, same size with theta(predictors)
        """
        super().__init__(lr=lr, batch_size=batch_size, num_epochs=num_epochs)
        self.eps = eps
        self._acceleration_square_sum = None

    def _update(self, X, y):
        if self._acceleration_square_sum is None:
            self._acceleration_square_sum = np.zeros_like(self._theta)
        dL_dw = self.gradient(X, y)
        self._acceleration_square_sum += dL_dw**2
        self._theta -= self.lr * dL_dw / \
            np.sqrt(self.eps + self._acceleration_square_sum)
        return None


class RMSprop(SGD):
    def __init__(self, lr=0.001, eps=1e-8, batch_size=1,
                 num_epochs=100, gamma=0.9):
        """
        Eg = gamma * Eg + (1-gamma) * (dL/dW)**2
        W = W - lr / sqrt(eps + Eg) * dL/dW
        """
        super().__init__(lr=lr, batch_size=batch_size, num_epochs=num_epochs)
        self.eps = eps
        self._A = None
        self.gamma = gamma

    def _update(self, X, y):
        if self._A is None:
            self._A = np.zeros_like(self._theta)
        dL_dw = self.gradient(X, y)
        gamma = self.gamma
        self._A = gamma * self._A + (1-gamma) * dL_dw**2
        self._theta -= self.lr * dL_dw / np.sqrt(self.eps + self._A)
        return None


class Adam(SGD):
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8, batch_size=1, num_epochs=100):
        """
        以后再说
        """
        super().__init__(lr=lr, batch_size=batch_size, num_epochs=num_epochs)
        self.beta1, self.beta2 = beta1, beta2
        self._M, self._A = None, None
        self._t = 0
        self.eps = eps

    def _update(self, X, y):
        self._t += 1
        if self._M is None:
            self._M = np.zeros_like(self._theta)
        if self._A is None:
            self._A = np.zeros_like(self._theta)
        beta1, beta2 = self.beta1, self.beta2
        dL_dw = self.gradient(X, y)
        self._M = beta1*self._M + (1-beta1)*dL_dw
        self._A = beta2*self._A + (1-beta2)*dL_dw**2
        self._M_correct = self._M/(1-beta1**self._t)
        self._A_correct = self._A/(1-beta2**self._t)
        self._theta -= self.lr/np.sqrt(
            self._A_correct+self.eps) * self._M_correct
        return None
