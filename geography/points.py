# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/02_points.ipynb.

# %% auto 0
__all__ = ['Points', 'in_hull']

# %% ../nbs/02_points.ipynb 3
import numpy as np
from scipy.spatial import ConvexHull, convex_hull_plot_2d
import functools
import collections
from fastcore.basics import patch
from typing import Literal, Optional

# %% ../nbs/02_points.ipynb 4
class Points:
    """generate binomial or poisson points in a convex set, default to unit box"""
    def __init__(self, n,d=2, seed=None, law: Literal["binomial","poisson"]="binomial", shape:Optional[ConvexHull]=None):
        assert law in ["binomial","poisson"]
        self.n = np.random.default_rng(seed).poisson(n) if law == "poisson" else n
        self.d = d
        self.shape = shape
        self.seed = seed
    
    @functools.cached_property
    def points(self):
        if self.shape is None:
            return np.random.default_rng(self.seed).uniform(size=(self.n,self.d))
        else:
            ps = []
            for _ in range(self.n):
                while True:
                    sample = np.random.default_rng().uniform(size=(self.d,))
                    if in_hull(sample, self.shape): 
                        ps.append(sample); break
            assert len(ps)==self.n
            return np.array(ps)


# %% ../nbs/02_points.ipynb 5
def in_hull(point,hull:ConvexHull,tol=1e-9):
    assert len(point)==hull.ndim, "expect point, hull in the same dimension"
    W,b = hull.equations[:,:-1], hull.equations[:,-1]
    return np.all(W@point+b<=tol)
