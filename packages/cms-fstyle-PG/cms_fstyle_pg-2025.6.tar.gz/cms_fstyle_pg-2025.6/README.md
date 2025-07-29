# CMS F-style

This package provides a matplolib mplstyle file to easily get decent plots with matplotlib.
It also includes a few functions to draw histograms or graph "à la ROOT" and decorate the axis.

## Package installation

### basic install
It can be installed via pip with:
```shell
pip install git+ssh://git@gitlab.cern.ch:7999/fcouderc/cms_fstyle.git
```

### adding fitter and/or stat capabilities
cms_fstyle provides some fitting tool and stat toots (distance covariance etc..) 
based on scikit-learn which is not installed by default. 
To enable this extra capability, the installation procedure is as follows:
```shell
pip install git+ssh://git@gitlab.cern.ch:7999/fcouderc/cms_fstyle.git[fitter]
```


## Plotting example
An example can be found in the [test.py file](https://gitlab.cern.ch/fcouderc/cms_fstyle/-/blob/master/test.py)
 included in the package or by running the set of following commands:
```python
import matplotlib.pyplot as plt
import numpy as np
import cms_fstyle as plotting # automatically import the rcp-style file 


plt.figure(figsize=[8, 6])

# -- histogram plotting example
data1 = np.random.normal(0, 1, 1000)
data2 = np.random.normal(1, 2, 1000)
bins = np.linspace(-5, 5, 51)
hist1, _ = np.histogram(data1, bins=bins)
hist2, _ = np.histogram(data2, bins=bins)

plotting.draw(x=bins, y=hist1, legend='hist 1', option='fill')
plotting.draw(x=bins, y=hist2, yerr=np.sqrt(hist2), legend='hist 2', option='E')
    
# -- graph plotting example
x = np.linspace(-5, 5, 20)
y = np.random.randint(0, 50, 20)
yerr = np.sqrt(y)
plotting.draw(x=x, y=y, yerr=yerr, legend='graph', option='E1')

# -- polishing the axis
plotting.polish_axis(x_title='(A.U.)', y_title="(A.U.)", 
                     x_range=(-6, 6), y_range=(0,), 
                     leg_title='sample plot', cms=True)
plotting.show()
```
which should give something like ![sample image](cms_fstyle/resources/sample.png)

## Stat covariances
The package includes several helper to compute covariances and correlation 
between random variables (linear-cov, distance-cov).
- Pearson's covariance: regular linear covariance
- Distance covariance: https://en.wikipedia.org/wiki/Distance_correlation
- Mutual information (normalised): https://en.wikipedia.org/wiki/Mutual_information
- Maximum information coefficient (MIC): https://www.science.org/doi/10.1126/science.1205438


### 2D covariance
A test of 2D covariance can be found in  
[test.py file](https://gitlab.cern.ch/fcouderc/cms_fstyle/-/blob/master/test.py)
 included in the package or by running the set of following commands:

```python
import matplotlib.pyplot as plt
import cms_fstyle as plotting
from cms_fstyle.stats import FCov2D
import cms_fstyle.stats.rand_var as gene

n_evt = 100000
fig, axes = plt.subplots(2, 4, figsize=[12, 8], sharex=True, sharey=True)
x_unif = gene.x_uniform(n_evt, a=4)
x_norm = gene.x_normal(n_evt)

samples = [[(x_norm, gene.y_parab(x_norm, s_y=0.1)), (x_unif, gene.y_circ(x_unif, s_y=0.05)),
            (x_norm, gene.y_parab2(x_norm, s_y=0.1)), (x_unif, gene.y_cos(x_unif, s_y=0.10))],
           [(x_norm, gene.y_parab(x_norm, s_y=0.8)), (x_unif, gene.y_circ(x_unif, s_y=0.20)),
            (x_norm, gene.y_parab2(x_norm, s_y=0.8)), (x_unif, gene.y_cos(x_unif, s_y=1.0))]]

covar = None
for i in range(2):
    for j in range(4):
        x, y = samples[i][j]
        covar = FCov2D(x, y)
        covar.plot(ax=axes[i, j])
        l_cor = covar.corcoef()    # linear correlation
        d_cor = covar.d_corcoef()  # distance correlation
        mi_cor = covar.mutual_information()  # normalized mutual information
        t_str = f'L-corr = {l_cor:>3.2f}\nD-corr = {d_cor:>3.2f}\nMI = {mi_cor:>3.2f}'
        tt = axes[i, j].text(-2, -4.5, t_str, fontsize=15, color='k')
        tt.set_bbox({'facecolor': 'w', 'alpha': 0.8, 'edgecolor': 'none'})
        axes[i, j].set_ylim(-5, 5)
        axes[i, j].set_xlim(-4, 4)

plotting.show()
```
which should give something like ![covariance image](cms_fstyle/resources/covariance.png)

One can see that the distance correlation captures the correlation while the regular 
Pearson correlation coefficient (linear correlation) is zero. A distance-correlation definition can be found in 
 https://en.wikipedia.org/wiki/Distance_correlation.


### ND covariance
A test of NxN covariance/correlation can be found in  
[test.py file](https://gitlab.cern.ch/fcouderc/cms_fstyle/-/blob/master/test.py)
 included in the package or by running the set of following commands:

```python
import matplotlib.pyplot as plt
import numpy as np
import cms_fstyle as plotting
from cms_fstyle.stats import FCovND, disp_cov, mic_cor
import cms_fstyle.stats.rand_var as gene

n_evt = 1000000
x = gene.x_uniform(n_evt, 3)
y = gene.y_circ(x, s_y=0.10)
z = gene.y_cos(y, s_y=0.4)

fig1, axes = plt.subplots(2, 2, figsize=[8, 8])
covar = FCovND(np.array([x, y, z]).T)

for i in range(3):
    for j in range(i+1, 3):
        covar.plot_2d(i, j, ax=axes[i, j-1])
        plotting.polish_axis(axes[i, j-1], x_title=covar.names[i], y_title=covar.names[j])

fig2, axes = plt.subplots(1, 3, figsize=[9, 3])

disp_cov(covar.cor(), ax=axes[0], vmin=0, vmax=0.5)
disp_cov(covar.d_cor(), ax=axes[1], vmin=0, vmax=0.5)
disp_cov(mic_cor(np.array([x, y, z]).T, qt=True), ax=axes[2], vmin=0, vmax=0.5, colorbar=True)

axes[0].set_title('linear corr.')
axes[1].set_title('distance corr.')
axes[2].set_title('MIC')

plotting.show()
```
which should give something like 
![covariance projection](cms_fstyle/resources/covariance_proj.png)

as well as the comparison of the linear correlation matrix vs the distance correlation matrix 
and the maximum information coefficients.
![correlation](cms_fstyle/resources/correlation.png). 
