from typing import Literal

import torch
from torch.nn.functional import softplus
import numpy as np

import dgl
import dgl.function as fn

import orthnet

import nfflr
from nfflr.nn import RBFExpansion


class GaussianSpline(torch.nn.Module):
    def __init__(
        self,
        nbasis: int = 128,
        d_model: int = 1,
        cutoff: float = 6.0,
        activation: Literal["softplus"] | None = None,
    ):
        super().__init__()
        self.nbasis = nbasis
        self.d_model = d_model
        self.cutoff = cutoff
        self.activation = torch.nn.Identity()

        ps = 0.1 * torch.ones(nbasis, d_model)
        self.phi = torch.nn.Parameter(ps)
        self.basis = RBFExpansion(vmax=cutoff, bins=nbasis)

        if activation == "softplus":
            self.activation = torch.nn.Softplus()

        # self.reset_parameters()

    def fcut(self, r):
        return (1 + torch.cos(np.pi * r / self.cutoff)) / 2

    def scale_distance(self, r, ls=5.0):
        """Distance scaling function from ACE (10.1103/PhysRevB.99.014104)."""
        return 1 - 2 * (
            torch.divide(torch.exp(-ls * ((r / self.cutoff) - 1)) - 1, np.exp(ls) - 1)
        )

    def reset_parameters(self):
        torch.nn.init.normal_(self.phi.data, 100.0, 100.0)

    def forward(self, r):
        """Evaluate radial Gaussian spline(s) at radial point `r`.

        TODO: consider sparse evaluation for EAM style models
        indexing into the coefficients rather than the radial functions
        """
        b = self.basis(r) * self.fcut(r).unsqueeze(1) / 2
        return (b.unsqueeze(-1) * self.activation(self.phi)).sum(dim=1)


class ExponentialRepulsive(torch.nn.Module):
    def __init__(self, amplitude: float = 2e5, lengthscale: float = 5.0):
        super().__init__()

        def inv_softplus(r):
            return r + np.log(-np.expm1(-r))

        self.amplitude = torch.nn.Parameter(torch.tensor(inv_softplus(amplitude)))
        self.lengthscale = torch.nn.Parameter(torch.tensor(inv_softplus(lengthscale)))

    def forward(self, r):
        return softplus(self.amplitude) * torch.exp(-softplus(self.lengthscale) * r)


class LaguerreRepulsive(torch.nn.Module):
    def __init__(self, nbasis: int = 8, cutoff: float = 6):
        super().__init__()
        self.nbasis = nbasis
        self.lengthscale = 2.0

        ps = torch.zeros(nbasis)
        self.phi = torch.nn.Parameter(ps)
        self.activation = torch.nn.functional.softplus  # torch.exp

    def forward(self, r):

        basis = orthnet.Laguerre(r.unsqueeze(1), self.nbasis - 1).tensor
        return torch.exp(-r / 2) * (self.activation(self.phi * basis)).sum(dim=1)

        # return softplus(self.amplitude) * torch.exp(self.lengthscale * r)


class PolynomialEmbeddingFunction(torch.nn.Module):
    def __init__(self, degree: int = 4, d_model: int = 1, use_sqrt_term: bool = True):
        super().__init__()
        self.degree = degree
        self.use_sqrt_term = use_sqrt_term

        # polynomial expansion terms - omit constant offset to enforce F(0) = 0
        powers = 1.0 + torch.arange(degree)

        # scale coefficients for numerical reasons
        scalefactors = 1 / 10 ** torch.cumsum(torch.log10(powers), dim=0)

        if use_sqrt_term:
            # initialize to F(rho) = sqrt(rho)
            powers = torch.hstack((0.5 * torch.ones(1), powers))
            scalefactors = torch.hstack((2 * torch.ones(1), scalefactors))
            init_weights = torch.hstack((-torch.ones(1) / 2, torch.zeros(degree)))
        else:
            # initialize to near-linear function with small curvature...
            init_weights = torch.hstack(
                (torch.tensor([-1, 0.1]), torch.zeros(degree - 2))
            )

        self.register_buffer("powers", powers)
        self.register_buffer("scalefactors", scalefactors)

        # start multivariate model with identical embedding functions
        init_weights = init_weights.unsqueeze(1).repeat(1, d_model)

        self.weights = torch.nn.Parameter(init_weights)

    def forward(self, density):
        """Evaluate polynomial."""

        basis = density.unsqueeze(-1).pow(self.powers)
        scaled_weights = self.weights * self.scalefactors.unsqueeze(1)

        # bach matrix-vector multiply basis and coefficients
        # (vmap over output channel dimension)
        f = torch.vmap(torch.matmul)(
            basis.unsqueeze(0), scaled_weights.unsqueeze(0)
        ).squeeze(0)

        return f

    def curvature(self, density):
        """Analytic curvature of embedding function for regularization."""

        # TODO: double check the broadcasting here
        # multiplicative factors from polynomial second derivatives...
        mult = (self.powers * (1 + self.powers))[:-1]

        if self.use_sqrt_term:
            mask = torch.ones(self.degree + 1, dtype=bool)
            mask[1] = 0

            # overwrite the factor for the sqrt term
            mult[0] = -1 / 4

            w = self.weights[mask]
            sf = mult * self.scalefactors[mask]
            p = self.powers[mask] - 2

        else:
            w = self.weights[1:]
            sf = mult * self.scalefactors[1:]
            p = self.powers[1:] - 2

        basis = density.unsqueeze(-1).pow(p)
        scaled_weights = w * sf.unsqueeze(1)

        # bach matrix-vector multiply basis and coefficients
        # (vmap over output channel dimension)
        curve = torch.vmap(torch.matmul)(
            basis.unsqueeze(0), scaled_weights.unsqueeze(0)
        ).squeeze(0)

        # curve = density.unsqueeze(-1).pow(p) @ (w * sf)
        return curve


class SplineEmbeddingFunction(torch.nn.Module):
    def __init__(self, nbasis: int = 8):
        super().__init__()
        self.nbasis = nbasis
        self.weights = torch.nn.Parameter(-0.1 * torch.ones(nbasis))
        self.basis = RBFExpansion(vmin=-1.0, vmax=4.0, bins=nbasis)

    def forward(self, r):
        curve = (self.weights * self.basis(r)).sum(dim=1)
        # subtract sum of parameters to shift the curve so f(0) = 0
        # z = self.weights * self.basis(torch.tensor(0).unsqueeze(1))
        return curve


class ElementalEmbeddedAtomPotential(torch.nn.Module):
    def __init__(self, nbasis: int = 128, cutoff: float = 6.0):
        super().__init__()

        self.nbasis = nbasis
        self.cutoff = cutoff

        self.density = GaussianSpline(
            nbasis=nbasis, cutoff=cutoff, activation="softplus"
        )
        # self.pair_repulsion = ExponentialRepulsive()
        self.pair_repulsion = GaussianSpline(nbasis=nbasis, cutoff=cutoff)
        self.embedding_energy = PolynomialEmbeddingFunction()

        self.transform = nfflr.nn.PeriodicRadiusGraph(self.cutoff)

    def reset_parameters(self):
        torch.nn.init.normal_(self.density.phi.data, -1.0, 0.1)

        ones = torch.ones_like(self.pair_repulsion.phi.data)
        phis = (
            ones * 10 * torch.exp(-0.1 * self.pair_repulsion.basis.centers).unsqueeze(1)
        )
        self.pair_repulsion.phi.data = phis

    def forward(self, at: nfflr.Atoms):
        if type(at) == nfflr.Atoms:
            g = self.transform(at)
        else:
            g = at

        g = g.local_var()

        # initial bond features: bond displacement vectors
        # need to add bond vectors to autograd graph
        r = g.edata.pop("r")
        r.requires_grad_(True)

        bondlen = torch.norm(r, dim=1)

        g.edata["density_ij"] = self.density(bondlen)
        g.update_all(fn.copy_e("density_ij", "m"), fn.sum("m", "local_density"))
        g.ndata["F"] = self.embedding_energy(g.ndata["local_density"])
        g.edata["pair_repulsion"] = self.pair_repulsion(bondlen) / bondlen
        potential_energy = dgl.readout_nodes(g, "F") + dgl.readout_edges(
            g, "pair_repulsion"
        )

        # potential_energy = F.sum() + pair_repulsion.sum()

        forces = nfflr.autograd_forces(potential_energy, r, g, energy_units="eV")
        return {"energy": potential_energy, "forces": forces}


class EmbeddedAtomPotential(torch.nn.Module):
    def __init__(self, species: torch.Tensor, nbasis: int = 128, cutoff: float = 6.0):
        """Multicomponent embedded atom potential."""
        super().__init__()

        self.nbasis = nbasis
        self.cutoff = cutoff

        self.atomtype = nfflr.nn.AtomType(species)
        self.pairtype = nfflr.nn.AtomPairType(species, symmetric=True)

        self.density = GaussianSpline(
            nbasis=nbasis, d_model=len(species), cutoff=cutoff, activation="softplus"
        )
        self.pair_repulsion = GaussianSpline(
            nbasis=nbasis, d_model=self.pairtype.num_classes, cutoff=cutoff
        )
        self.embedding_energy = PolynomialEmbeddingFunction(d_model=len(species))

        self.transform = nfflr.nn.PeriodicRadiusGraph(self.cutoff)

        self.reset_parameters()

    def reset_parameters(self):
        torch.nn.init.normal_(self.density.phi.data, -1.0, 0.1)

        ones = torch.ones_like(self.pair_repulsion.phi.data)
        phis = (
            ones * 10 * torch.exp(-0.1 * self.pair_repulsion.basis.centers).unsqueeze(1)
        )
        self.pair_repulsion.phi.data = phis

    def forward(self, at: nfflr.Atoms):
        if type(at) == nfflr.Atoms:
            g = self.transform(at)
        else:
            g = at

        g = g.local_var()

        # initial bond features: bond displacement vectors
        # need to add bond vectors to autograd graph
        r = g.edata.pop("r")
        r.requires_grad_(True)

        bondlen = torch.norm(r, dim=1)

        # look up atom and edge types
        atomtype = self.atomtype(g.ndata["atomic_number"])

        def types(edges):
            srctype = self.atomtype(edges.src["atomic_number"])
            pairtype = self.pairtype(
                edges.src["atomic_number"], edges.dst["atomic_number"]
            )
            return {"srctype": srctype, "pairtype": pairtype}

        g.apply_edges(types)

        srctype = g.edata.pop("srctype")
        pairtype = g.edata.pop("pairtype")

        g.edata["density_ij"] = torch.take(self.density(bondlen), srctype)
        g.update_all(fn.copy_e("density_ij", "m"), fn.sum("m", "local_density"))
        F = self.embedding_energy(g.ndata["local_density"])
        g.ndata["F"] = torch.take(F, atomtype)

        # g.ndata["F"] = torch.take(
        #     self.embedding_energy(g.ndata["local_density"]), atomtype
        # )

        g.edata["pair_repulsion"] = (
            torch.take(self.pair_repulsion(bondlen), pairtype) / bondlen
        )
        potential_energy = dgl.readout_nodes(g, "F") + dgl.readout_edges(
            g, "pair_repulsion"
        )

        # potential_energy = F.sum() + pair_repulsion.sum()

        forces = nfflr.autograd_forces(potential_energy, r, g, energy_units="eV")
        return {"energy": potential_energy, "forces": forces}


class ExponentialDensity(torch.nn.Module):
    def __init__(self, amplitude: float = 3.0, lengthscale: float = 1.5):
        super().__init__()

        def inv_softplus(r):
            return r + np.log(-np.expm1(-r))

        self.amplitude = torch.nn.Parameter(torch.tensor(inv_softplus(amplitude)))
        self.lengthscale = torch.nn.Parameter(torch.tensor(inv_softplus(lengthscale)))

    def forward(self, r):
        return softplus(self.amplitude) * torch.exp(-softplus(self.lengthscale) * r)


class SqrtEmbedding(torch.nn.Module):
    def __init__(self, amplitude: float = 3.0, lengthscale: float = 1.0):
        super().__init__()

        def inv_softplus(r):
            return r + np.log(-np.expm1(-r))

        self.amplitude = torch.nn.Parameter(torch.tensor(inv_softplus(amplitude)))
        # self.lengthscale = torch.nn.Parameter(torch.tensor(inv_softplus(lengthscale)))

    def forward(self, density):
        return -softplus(self.amplitude) * torch.sqrt(density)


class SimpleEmbeddedAtomPotential(torch.nn.Module):
    def __init__(self, cutoff: float = 6.0):
        super().__init__()
        self.cutoff = cutoff
        self.transform = nfflr.nn.PeriodicRadiusGraph(self.cutoff)

        # self.density = ElectronDensity(nbasis=128, cutoff=cutoff)
        self.density = ExponentialDensity()
        self.pair_repulsion = ExponentialRepulsive(amplitude=10.0)
        self.embedding_energy = SqrtEmbedding()

    def forward(self, at: nfflr.Atoms):
        if type(at) == nfflr.Atoms:
            g = self.transform(at)
        else:
            g = at

        g = g.local_var()

        # initial bond features: bond displacement vectors
        # need to add bond vectors to autograd graph
        r = g.edata.pop("r")
        r.requires_grad_(True)

        bondlen = torch.norm(r, dim=1)

        g.edata["density_ij"] = self.density(bondlen)
        g.update_all(fn.copy_e("density_ij", "m"), fn.sum("m", "local_density"))
        g.ndata["F"] = self.embedding_energy(g.ndata["local_density"])
        g.edata["pair_repulsion"] = self.pair_repulsion(bondlen)  # / bondlen

        potential_energy = dgl.readout_nodes(g, "F") + dgl.readout_edges(
            g, "pair_repulsion"
        )
        # potential_energy = F.sum() + pair_repulsion.sum()

        forces = nfflr.autograd_forces(potential_energy, r, g, energy_units="eV")
        return {"energy": potential_energy, "forces": forces}

        return
