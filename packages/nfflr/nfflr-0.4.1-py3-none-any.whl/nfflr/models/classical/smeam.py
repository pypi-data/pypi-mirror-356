from plum import dispatch
from typing import Tuple, Union, Optional, Literal
from dataclasses import dataclass

import dgl
import dgl.function as fn
from dgl.nn import AvgPooling, SumPooling

import torch
from torch import nn

from torchcubicspline import natural_cubic_spline_coeffs, NaturalCubicSpline

from nfflr.models.utils import (
    smooth_cutoff,
    autograd_forces,
    RBFExpansion,
)

from nfflr.models.abstract import AbstractModel

from nfflr.data.graph import compute_bond_cosines, periodic_radius_graph
from nfflr.atoms import _get_attribute_lookup, Atoms


@dataclass
class SMEAMConfig:
    cutoff: float = 8.0
    spline_knots: int = 7
    compute_forces: bool = True


class SMEAM(nn.Module):
    """Spline modified embedded atom method 10.1016/j.commatsci.2021.110752.

    The energy is decomposed into pairwise ϕ terms and an embedding function U
    of the electron density n around each atom.

    E = \sum_{i < j} Φᵢⱼ(rᵢⱼ) + \sum_i Uᵢ(nᵢ)
    nᵢ = \sum_{j ≠ i} ρⱼ(rᵢⱼ) + \sum_{j < k; j,k ≠ i} fⱼ(rᵢⱼ) fₖ(rᵢₖ) gⱼₖ(cos(θⱼᵢₖ))

    subscripts on functions indicate separate functions for species of each atom.
    Φ, U, ρ, f, g are modeled by cubic splines

    domains of U and g are [-1, 1]
    domains of radial functions Φ, ρ, and f are [0, cutoff]

    TODO: scale the inputs to batch all spline evaluations for better parallelism
    but, maybe terms need to be grouped carefully?

    """

    def __init__(self, config: SMEAMConfig):
        # use https://github.com/patrick-kidger/torchcubicspline
        super().__init__()
        self.config = config

        self.knots_radial = torch.torch.linspace(
            0, config.cutoff, config.spline_knots, requires_grad=False
        )
        self.f_coeffs = torch.rand(config.spline_knots, 1)

        self.knots_angular = torch.torch.linspace(
            -1, 1, config.spline_knots, requires_grad=False
        )
        self.g_coeffs = torch.rand(config.spline_knots, 1)

    def forward_at(self, x: Atoms):
        return self.forward(periodic_radius_graph(x, r=self.config.cutoff))

    def forward(self, g: dgl.DGLGraph):
        config = self.config

        g = g.local_var()

        # initial bond features: bond displacement vectors
        r = g.edata.pop("r")

        # to compute forces, take gradient wrt g.edata["r"]
        # need to add bond vectors to autograd graph
        if config.compute_forces:
            r.requires_grad_(True)

        g.edata["r"] = r

        # disable back-tracking?
        lg = g.line_graph(shared=True, backtracking=False)

        # probably do custom + builtin
        # triplet message needs to do f(|src|), f(|dst|), g(src * dst)
        # either do the triplet interactions with a builtin + custom

        f = NaturalCubicSpline(
            natural_cubic_spline_coeffs(self.knots_radial, self.f_coeffs)
        )
        g = NaturalCubicSpline(
            natural_cubic_spline_coeffs(self.knots_angular, self.g_coeffs)
        )

        def triplet_interaction(lg_edges):
            # maybe this can actually be better done with u_mul_v for f?
            r1 = -lg_edges.src["r"]
            r2 = lg_edges.dst["r"]
            l1 = torch.norm(r1, dim=1)
            l2 = torch.norm(r2, dim=1)
            bond_cosine = torch.clamp(torch.sum(r1 * r2, dim=1) / (l1 * l2), -1, 1)

            return {"m": f.evaluate(l1) * f.evaluate(l2) * g.evaluate(bond_cosine)}

        # lg.update_all(fn.u_mul_v("rnorm", "rnorm", "m"), fn.sum("m", "ft"))
        lg.update_all(fn.u_mul_v("r", "r", "m"), fn.sum("m", "ft"))
        lg.update_all(triplet_interaction, fn.sum("m", "ft"))

        # lg.apply_edges(compute_bond_cosines)
        # bond_cosines = lg.edata.pop("h")

        bondlength = torch.norm(r, dim=1)

        # evaluate pair term

        # evaluate density
        return lg
