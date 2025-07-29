import numpy as np
import scipy.optimize as scipyfitter
from scipy.optimize import approx_fprime


#  useful function
def gauss(x, *p):
    return p[2] * np.exp(-0.5 * ((x - p[0]) / p[1]) ** 2)


# fitter class
class FFitter:
    def __init__(self, method='chi2', p0=None, p_range=None, minimizer='BFGS'):
        self.p0 = p0
        self.p_range = p_range
        self.method = method
        self.minimizer = minimizer

        if minimizer == 'BFGS' and self.p_range is not None:
            self.minimizer = 'L-BFGS-B'

        if minimizer == 'BFGS' and self.p_range is None:
            print('[histFitter] BFGS w/o constraints does not converge properly (???), switch to simplex')
            self.minimizer = 'Nelder-Mead'

        # result storage
        self.par = None
        self.cov = None
        self.xfun = None
        self.yfun = None

        # hessian matrix
        self.hessian = None
        self.success = -1

    def hess(self, cost_func, epsilon=1.e-4):
        """
        Numerically compute the hessian matrix to estimate the error
        :param cost_func:
        :param epsilon:
        :return:
        """
        epsilons = np.where(np.abs(self.par) < 1, epsilon, epsilon * np.abs(self.par))
        # Allocate space for the hessian
        n = self.par.shape[0]
        self.hessian = np.zeros((n, n))

        xx = self.par
        for j in range(n):
            xx0 = xx[j]  # Store initial value
            xx[j] = xx0 + epsilons[j]
            fp1 = approx_fprime(xx, cost_func, epsilons)
            xx[j] = xx0 - epsilons[j]
            fm1 = approx_fprime(xx, cost_func, epsilons)
            self.hessian[:, j] = (fp1 - fm1) / (2 * epsilons[j])
            xx[j] = xx0  # Restore initial value

    # def fit_hist(self, hist, func, x_range=None):
    #     x = hist.binCenter[not hist.emptybins]
    #     y = hist.hist[not hist.emptybins]
    #     err = hist.err[not hist.emptybins]
    #     return self.fit(x, y, err, func, x_range)

    def fit(self, x, y, yerr, func, x_range=None):
        eps_float = np.finfo(float).eps
        xs_to_use = np.full((y.size,), True)
        xs_to_use = xs_to_use & (~np.isnan(y))

        if x_range is not None:
            xs_to_use = xs_to_use & (x >= x_range[0]) & (x <= x_range[1])

        eps = 1e-3
        if self.method == 'chi2':
            # to be coeherent with ROOT fitsx
            sigma = np.where(yerr > eps_float, yerr, 1)

            def chi2(par):
                ypred = func(x, *par)
                dchi = np.where(xs_to_use, (ypred - y) / sigma, 0)
                return np.sum(dchi ** 2)

            result = scipyfitter.minimize(chi2, self.p0, bounds=self.p_range, method=self.minimizer)
            self.success = result.success
            self.par = result.x
            self.hess(chi2, epsilon=eps)

        if self.method == 'mlh':
            def negllh(par):
                ypred = func(x, *par)
                xs_loc = xs_to_use & (ypred > eps_float)
                ypred = np.where(xs_loc, ypred, 1)
                dlog = np.where(xs_loc, -ypred + y * np.log(ypred), 0)
                return -2 * np.sum(dlog)

            result = scipyfitter.minimize(negllh, self.p0, bounds=self.p_range, method=self.minimizer)
            self.success = result.success
            self.par = result.x
            self.hess(negllh, epsilon=eps)

        if self.success and self.hessian is not None:
            try:
                self.cov = np.linalg.inv(0.5 * self.hessian)
            except np.linalg.LinAlgError:
                print('[FFitter WARNING] covariance matrix calculation failed, returning cov = None')
                self.cov = None

            # for plotting purpose
            if x_range is None:
                x_range = [x[0], x[-1]]
            self.xfun = np.linspace(x_range[0], x_range[1], 500)
            self.yfun = func(self.xfun, *self.par)

        else:
            self.par = self.cov = None
        return self.par, self.cov

    def curve(self):
        return self.xfun, self.yfun
