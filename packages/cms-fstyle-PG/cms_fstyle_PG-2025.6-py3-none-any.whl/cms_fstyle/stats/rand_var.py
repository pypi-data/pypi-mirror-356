__doc__ = """Helper module to generate random variables and their 2D correlation"""
import numpy as np


def x_uniform(n_evt, a=3.):
    return np.random.uniform(-a, a, n_evt)


def x_normal(n_evt, loc=0., std=1.):
    return np.random.normal(loc, std, n_evt)


def x_circ(n_evt, r=1., s_r=0.1):
    radius = np.random.normal(r, s_r * r, n_evt)
    theta = np.random.uniform(0, 2 * np.pi, n_evt)
    return radius*np.cos(theta)


def y_parab(x, s_y=1., coef=0.5):
    return np.array([np.random.normal(xx*xx*coef, s_y) for xx in x])


def y_parab2(x, s_y=1., coef=0.5):
    y = np.array([np.random.normal(xx * xx * coef, s_y) for xx in x])
    sign = np.random.randint(0, 2, len(x))
    y *= np.where(sign == 0, -1, 1)
    return y


def y_cos(x, s_y=1., coef=1., n_cycles=2):
    dx = x.max() - x.min()
    om = 2*np.pi / dx * n_cycles
    return np.array([np.random.normal(np.cos(xx * om) * coef, s_y) for xx in x])


def y_circ(x, s_y=0.1):
    radius = x.max()*1.001
    y = np.sqrt(radius**2 - x**2)
    y = np.array([yy + s_y*radius*np.random.uniform(-1, 1) for yy in y])
    sign = np.random.randint(0, 2, len(x))
    y *= np.where(sign == 0, -1, 1)
    return y
