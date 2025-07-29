__doc__ = """This modules conatins classes to compute covariance and correlation matrices.
The covariance measures included are:
- pearson covariance (function cov): regular linear covariance
- distance covariance (function d_cov):  see for instance https://en.wikipedia.org/wiki/Distance_correlation
- Maximum information coefficient: see https://www.science.org/doi/10.1126/science.1205438

Because the distance covariance (and potentially some others) requires a lot of memory 
(goes as N^2 with N the number of samples), the input data are binned to compute all types of covariance. 
This has been found to have little effect on the computed number provided the number of bins is 
large enough (typically 50).
"""
from typing import Tuple, Union, Sequence
import numpy as np
import pandas as pd
from cms_fstyle import heatmap
from sklearn.preprocessing import QuantileTransformer
Bin = Union[Sequence, np.array, int]


def correlation_matrix(covariance: Union[np.ndarray, pd.DataFrame]) -> np.ndarray:
    """
    compute the correlation matrix from the covariance matrix
    :param covariance: covariance matrix
    :return: correlation matrix
    """
    sigma = np.sqrt(np.diag(covariance))
    return covariance / (sigma[:, np.newaxis] * sigma[np.newaxis, :])


def disp_cov(cov: Union[pd.DataFrame, np.ndarray], ax=None, nandiag=True, colorbar=False, **kwargs):
    """
    Print a covariance/correlation matrix with color background
    :param cov: covariance/correlation matrix
    :param ax: axis
    :param nandiag: for correlation matrix set the diag to nan
    :param colorbar: add a color bar for the z range

    :param kwargs: arguments to pass to the heatmap
    :return: im, colorbar
    """
    disp = pd.DataFrame(cov).copy()

    if nandiag and (np.fabs(np.diag(disp).sum() - len(disp.columns)) < 1e-5):
        # for correlation matrix remove the diag
        np.fill_diagonal(disp.values, np.nan)

    # set a default color map
    kwargs.setdefault('cmap', 'YlOrBr')
    return heatmap(disp, grid=False, text=True, colorbar=colorbar, ax=ax, **kwargs)


# --------------------------------------------------------------------------
# -- class handling covariance matrices
# --------------------------------------------------------------------------
class FCovND:
    def __init__(self, x: Union[np.ndarray, pd.DataFrame], bins: Union[int, Sequence[Bin]] = 50):
        """
        Compute covariances / correlation for n_feature
        :param x: input data (shape: (n_samples, n_features))
        :param bins: int of list of int or list of bining. Bining of the different feature as used in FCov2D
        """

        # Name of variables
        self.names = None
        if type(x) is pd.DataFrame:
            self.names = x.columns.to_numpy()
            x = x.to_numpy()
        else:
            self.names = np.array([f'X{i}' for i in range(x.shape[1])])

        if np.issubdtype(type(bins), np.integer):
            bins = np.full((x.shape[1],), bins, dtype=int)

        # FCovs 2D calculators
        self.fcov_2d = np.empty((x.shape[1], x.shape[1]), dtype=object)
        for i in range(x.shape[1] - 1):
            for j in range(i + 1, x.shape[1]):
                self.fcov_2d[i, j] = FCov2D(x[:, i], x[:, j], binsx=bins[i], binsy=bins[j])

        # Covariance matrices
        self.cov_p = None
        self.cov_d = None
        self.cov_mi = None

    def __calc_covariance(self, cov_type: str = 'pearson'):
        """
        Compute the covariance matrix for the different kind of available covariance
        :param cov_type: str. pearson (i.e. linear), distance.
        :return:
        """
        if cov_type == 'pearson' and self.cov_p is not None:
            return
        elif cov_type == 'distance' and self.cov_d is not None:
            return
        elif cov_type == 'mi' and self.cov_mi is not None:
            return

        # init the covariance matrix
        n_var = len(self.names)
        cov_to_set = np.zeros((n_var, n_var), dtype=np.float32)

        for i in range(n_var - 1):
            for j in range(i + 1, n_var):
                cov2d = None
                if cov_type == 'pearson':
                    cov2d = self.fcov_2d[i, j].cov()
                elif cov_type == 'distance':
                    cov2d = self.fcov_2d[i, j].d_cov()
                elif cov_type == 'mi':
                    cov2d = self.fcov_2d[i, j].mi_cov()
                cov_to_set[i, i] += cov2d[0, 0]
                cov_to_set[j, j] += cov2d[1, 1]
                cov_to_set[i, j] += cov2d[0, 1]
                cov_to_set[j, i] += cov2d[1, 0]

        # average the diag
        for i in range(n_var):
            cov_to_set[i, i] /= (n_var - 1)

        if cov_type == 'pearson':
            self.cov_p = cov_to_set
        elif cov_type == 'distance':
            self.cov_d = cov_to_set
        elif cov_type == 'mi':
            self.cov_mi = cov_to_set

    def cov(self) -> pd.DataFrame:
        """Pearson covariance"""
        self.__calc_covariance(cov_type='pearson')
        return pd.DataFrame(self.cov_p, columns=self.names, index=self.names)

    def cor(self) -> pd.DataFrame:
        """pearson correlation"""
        return pd.DataFrame(correlation_matrix(self.cov()), columns=self.names, index=self.names)

    def corcoef(self, x: Union[int, str], y: Union[int, str]):
        """
        Pearson correlation coefficient
        :param x: int or str, x variable
        :param y: int or str, y variable
        :return: correlation coefficient
        """
        ix, iy = self.__ivar(x, y)
        return self.fcov_2d[ix, iy].corcoef()

    def d_cov(self) -> pd.DataFrame:
        """distance covariance"""
        self.__calc_covariance(cov_type='distance')
        return pd.DataFrame(self.cov_d, columns=self.names, index=self.names)

    def d_cor(self) -> pd.DataFrame:
        """distance correlation"""
        return pd.DataFrame(correlation_matrix(self.d_cov()), columns=self.names, index=self.names)

    def d_corcoef(self, x: Union[int, str], y: Union[int, str]):
        """
        Pearson correlation coefficient
        :param x: int or str, x variable
        :param y: int or str, y variable
        :return: correlation coefficient
        """
        ix, iy = self.__ivar(x, y)
        return self.fcov_2d[ix, iy].d_corcoef()

    def mi_cov(self) -> pd.DataFrame:
        """mutual information covariance == mutual information correlation"""
        self.__calc_covariance(cov_type='mi')
        return pd.DataFrame(self.mi_cov, columns=self.names, index=self.names)

    def mi_cor(self) -> pd.DataFrame:
        """mutual information correlation"""
        return self.mi_cov()

    def mi_corcoef(self, x: Union[int, str], y: Union[int, str]):
        """
        Pearson correlation coefficient
        :param x: int or str, x variable
        :param y: int or str, y variable
        :return: correlation coefficient
        """
        ix, iy = self.__ivar(x, y)
        return self.fcov_2d[ix, iy].mutual_information()

    def __ivar(self, x: Union[int, str], y: Union[int, str]) -> Tuple[int, int]:
        """
        find the  position of the x,y variables in the cov martrix
        :param x: int or str, x variable
        :param y: int or str, y variable
        :return: tuple of (ix, iy)
        """
        if type(x) is str:
            x, _ = np.where(self.names == x)
            x = np.asscalar(x)

        if type(y) is str:
            y, _ = np.where(self.names == y)
            y = np.asscalar(y)
        return x, y

    def profile(self, x: Union[int, str], y: Union[int, str]):
        """
        Profile the y vs x variable
        :param x: int or str, x variable
        :param y: int or str, y variable
        :return:
        """
        ix, iy = self.__ivar(x, y)
        return self.fcov_2d[ix, iy].profile()

    def plot_2d(self, x: Union[int, str], y: Union[int, str], **kwargs):
        """
        plot the y vs x variable
        :param x: int or str, x variable
        :param y: int or str, y variable
        :return:
        """
        ix, iy = self.__ivar(x, y)
        self.fcov_2d[ix, iy].plot(**kwargs)


# --------------------------------------------------------------------------
# -- maximum information
# --------------------------------------------------------------------------
def mic_cor(x: Union[np.ndarray, pd.DataFrame], qt=True, n_quantiles=1000, debug=False, n_grid=7) -> pd.DataFrame:
    """
    Maximum information coefficient as described in
    https://www.science.org/doi/10.1126/science.1205438
    :param x: input dataset (shape: (n_samples, n_features))
    :param qt: Quantile Transform the input dataset (to better)
    :param n_quantiles: number of quantile in quantile transform
    :param debug: some debugging printout
    :param n_grid: number of steps in the scanning grid
    :return: dataframe with the matrix of mic coefficients
    """
    if type(x) is np.ndarray:
        x = pd.DataFrame(x, columns=[f'X{i}' for i in range(x.shape[1])])

    if qt:
        qt_scaler = QuantileTransformer(n_quantiles=n_quantiles)
        x = pd.DataFrame(qt_scaler.fit_transform(x), columns=x.columns)

    mic_coef = np.zeros((x.shape[1], x.shape[1]), dtype=np.float32)
    np.fill_diagonal(mic_coef, 1)

    # scan the grid with a log spacing
    n_evt = x.shape[0]
    b_min = 5
    b_grid = np.round(np.exp(np.linspace(np.log(b_min), np.log(n_evt**0.6/b_min), n_grid))).astype(np.uint32)
    if n_evt**0.6 < b_min:
        raise ValueError(f'Number of samples is too low, n_min = {b_min**(1./0.6)}')

    for i in range(x.shape[1] - 1):
        for j in range(i + 1, x.shape[1]):
            vx = x.columns[i]
            vy = x.columns[j]
            mis = []
            for bx in b_grid:
                for by in b_grid:
                    if bx*by > n_evt**0.6:
                        mis.append(np.nan)
                    else:
                        mis.append(FCov2D(x[vx], x[vy], binsx=bx, binsy=by).mutual_information())

            # reshape the mutual info list for debugging purpose
            mis = pd.DataFrame(np.array(mis).reshape(len(b_grid), -1), index=b_grid, columns=b_grid)

            if debug:
                print(f"cov[{vx}, {vy}] : ")
                print(mis)

            mic_coef[i, j] = mis.max().max()
            mic_coef[j, i] = mic_coef[i, j]

    return pd.DataFrame(mic_coef, index=x.columns, columns=x.columns)


# --------------------------------------------------------------------------
# -- 2D covariance
# --------------------------------------------------------------------------
class FCov2D:
    def __init__(self, x, y, binsx: Bin = 50, binsy: Bin = 50):
        """
        This class contains function to compute different covariances / correlations...
        These number are computed in a binned way some un-binned covariances requires N^2 memory: distance covariance, MPI...
        The available covariance are:
        - pearson: regular linear correlation
        - distance: see for instance https://en.wikipedia.org/wiki/Distance_correlation

        :param x: sequence or np.array, first variable
        :param y: sequence or np.array, second variable
        :param binsx:  int or sequence of scalars, number of bins or actual binning
        :param binsy:  int or sequence of scalars, number of bins or actual binning
        """
        if np.asarray(x).shape != np.asarray(y).shape:
            raise ValueError('all the input array (x, y) dimensions must be identical')

        data = pd.DataFrame(np.array([x, y]).T, columns=['x', 'y'])

        # bin the distribution
        data['ibx'], self.binsx = FCov2D.digitize(data.x, bins=binsx)
        data['iby'], self.binsy = FCov2D.digitize(data.y, bins=binsy)

        gb = data.groupby(['ibx', 'iby'])
        self.xy = gb.mean()
        self.xy['n'] = gb.size()
        self.xy.reset_index(inplace=True)

        # distance correlation
        self.cov2_d = None
        self.v2_x_d = None
        self.v2_y_d = None

        # Pearson correlation (i.e. regular linear correlation)
        self.cov_p = None
        self.v_x_p = None
        self.v_y_p = None

    @staticmethod
    def digitize(x, bins: Bin) -> Tuple[np.array, np.array]:
        """
        Associate to each x value its corresponding bin number
        :param x: data
        :param bins: int or sequence of scalars, number of bins or actual binning
        :return: a tuple with the bin number per event, the final binning
        """
        if np.issubdtype(type(bins), np.integer):
            bins = np.linspace(x.min() - 1e-10, x.max(), bins + 1)

        bins[0] -= 1e-10  # close the first bin also on the left
        return np.digitize(x, bins=bins, right=True) - 1, bins

    @staticmethod
    def center(x_ij, n_ij):
        """
        Center the 2D X_ij matrix weighting each element with its number of event contained in n_ij
        :param x_ij: 2D matrix
        :param n_ij:
        :return:
        """
        x_w = x_ij * n_ij
        return (x_ij - x_w.sum(axis=0) / n_ij.sum(axis=0)).T - x_w.sum(axis=1) / n_ij.sum(axis=1) + x_w.sum() / n_ij.sum()

    def __calc_covariance_distance(self):
        """Compute all the distance covariances (X,X), (X,Y), (Y,Y)"""
        if self.cov2_d is None:
            x_i = self.xy.x.to_numpy()
            y_i = self.xy.y.to_numpy()
            n_i = self.xy.n.to_numpy()

            x_ij = np.abs(x_i[:, np.newaxis] - x_i[np.newaxis, :])
            y_ij = np.abs(y_i[:, np.newaxis] - y_i[np.newaxis, :])
            n_ij = n_i[:, np.newaxis] * n_i[np.newaxis, :]

            x_ij = FCov2D.center(x_ij, n_ij)
            y_ij = FCov2D.center(y_ij, n_ij)

            self.cov2_d = (x_ij * y_ij * n_ij).sum() / n_ij.sum()
            self.v2_x_d = (x_ij * x_ij * n_ij).sum() / n_ij.sum()
            self.v2_y_d = (y_ij * y_ij * n_ij).sum() / n_ij.sum()
            if self.cov2_d < 0:
                self.cov2_d = 0

    def __calc_covariance_pearson(self):
        """Compute all the pearson covariances (X,X), (X,Y), (Y,Y)"""
        if self.cov_p is None:
            x_i = self.xy.x.to_numpy()
            y_i = self.xy.y.to_numpy()
            n_i = self.xy.n.to_numpy()

            x_b = (n_i * x_i).sum() / n_i.sum()
            y_b = (n_i * y_i).sum() / n_i.sum()

            self.cov_p = ((x_i - x_b) * (y_i - y_b) * n_i).sum() / n_i.sum()
            self.v_x_p = ((x_i - x_b) * (x_i - x_b) * n_i).sum() / n_i.sum()
            self.v_y_p = ((y_i - y_b) * (y_i - y_b) * n_i).sum() / n_i.sum()

    def d_cov(self):
        """Distance covariance matrix"""
        self.__calc_covariance_distance()
        return np.array([[np.sqrt(self.v2_x_d), np.sqrt(self.cov2_d)],
                         [np.sqrt(self.cov2_d), np.sqrt(self.v2_y_d)]])

    def d_cor(self):
        """Distance correlation matrix"""
        return correlation_matrix(self.d_cov())

    def d_corcoef(self):
        """Distance correlation coefficient"""
        return FCov2D.corcoef_2d(self.d_cov())

    def cov(self):
        """Pearson covariance matrix"""
        self.__calc_covariance_pearson()
        return np.array([[self.v_x_p, self.cov_p],
                         [self.cov_p, self.v_y_p]])

    def cor(self):
        """Pearson correlation matrix"""
        return correlation_matrix(self.cov())

    def corcoef(self):
        """Pearson correlation coefficient"""
        return FCov2D.corcoef_2d(self.cov())

    def mutual_information(self):
        """Normalised Mutual information for a fixed number of bins"""
        bx = len(self.binsx) - 1
        by = len(self.binsy) - 1

        n_evt = self.xy.n.sum()
        px = self.xy.groupby('ibx').n.transform('sum') / n_evt
        py = self.xy.groupby('iby').n.transform('sum') / n_evt
        pxy = self.xy.n / n_evt
        return (pxy * np.log(pxy / (px * py))).sum() / np.log(min(bx, by))

    def mi_cov(self):
        mi = self.mutual_information()
        return np.array([[1., mi],
                         [mi, 1.]])

    @staticmethod
    def corcoef_2d(cov: np.ndarray):
        """
        return the correlation coefficient of a 2D covariance matrix
        :param cov: covariance matrix
        :return:
        """
        return cov[0, 1] / np.sqrt(cov[0, 0]*cov[1, 1])

    def profile(self) -> pd.DataFrame:
        """
        Profile along the x axis
        :return: return a DataFrame with the profile info
        """
        gr_proj = self.xy.groupby('ibx')
        x_m = gr_proj.apply(lambda x: np.average(x.x, weights=x.n))
        y_m = gr_proj.apply(lambda x: np.average(x.y, weights=x.n))
        n_m = gr_proj.apply(lambda x: x.n.sum())
        std_y = gr_proj.apply(lambda x: np.sqrt(((x.y - np.average(x.y, weights=x.n))**2 * x.n).sum() / x.n.sum()))
        std_x = gr_proj.apply(lambda x: np.sqrt(((x.x - np.average(x.x, weights=x.n))**2 * x.n).sum() / x.n.sum()))

        return pd.DataFrame({'x': x_m, 'std_x': std_x, 'y': y_m, 'std_y': std_y, 'n': n_m})

    def plot(self, ax=None, cmap='coolwarm'):
        """
        plot 2D X,Y
        :param ax: axis to plot on (default = None)
        :param cmap: colormap as used in matplotlib
        :return:
        """
        c_2d = self.xy.pivot(index='iby', columns='ibx', values='n')\
            .reindex(np.arange(0, len(self.binsy) - 1), axis=0)\
            .reindex(np.arange(0, len(self.binsx) - 1), axis=1)

        prof = self.profile()

        import matplotlib.pyplot as plt
        if ax is None:
            ax = plt.gca()
        ax.pcolormesh(self.binsx, self.binsy, c_2d, cmap=cmap)
        ax.errorbar(x=prof.x, y=prof.y, xerr=prof.std_x, yerr=prof.std_y/np.sqrt(prof.n), color='k', ls='', marker='.')
        ax.set_xlim(self.binsx[0], self.binsx[-1])
