import dgl
import torch

import ase.neighborlist

import nfflr
from nfflr.data.graph import (
    periodic_radius_graph,
    periodic_adaptive_radius_graph,
    periodic_kshell_graph,
    periodic_sann_graph,
    sort_edges_by_dst,
)

from nfflr.nn.layers.atomfeatures import CovalentRadius


class PeriodicRadiusGraph(torch.nn.Module):
    """Periodic radius graph transform."""

    def __init__(
        self, cutoff: float = 5.0, dtype=torch.float, sort_edges: bool = False
    ):
        super().__init__()
        self.cutoff = cutoff
        self.dtype = dtype
        self.sort_edges = sort_edges

    def forward(self, x: nfflr.Atoms):
        """Compute periodic radius graph."""
        g = periodic_radius_graph(x, r=self.cutoff, dtype=self.dtype)
        if self.sort_edges:
            g = sort_edges_by_dst(g)
        return g


class PeriodicAdaptiveRadiusGraph(torch.nn.Module):
    """Adaptive periodic radius graph transform."""

    def __init__(self, cutoff: float = 5.0, dtype=torch.float):
        super().__init__()
        self.cutoff = cutoff
        self.dtype = dtype

    def forward(self, x: nfflr.Atoms):
        return periodic_adaptive_radius_graph(x, r=self.cutoff, dtype=self.dtype)


class PeriodicSolidAngleGraph(torch.nn.Module):
    """Periodic Solid Angle Nearest Neighbor graph transform."""

    def __init__(
        self,
        max_neighbors: int = 32,
        cutoff_radius: float = 10.0,
        bond_tol: float = 0.15,
        dtype=torch.get_default_dtype(),
    ):
        super().__init__()
        self.max_neighbors = max_neighbors
        self.cutoff_radius = cutoff_radius
        self.bond_tol = bond_tol
        self.dtype = dtype

    def forward(self, x: nfflr.Atoms):
        return periodic_sann_graph(
            x,
            max_neighbors=self.max_neighbors,
            cutoff_radius=self.cutoff_radius,
            bond_tol=self.bond_tol,
            dtype=self.dtype,
        )


class PeriodicNaturalRadiusGraph(torch.nn.Module):
    """Periodic radius graph transform based on covalent radii.

    A thin wrapper around ase.neighborlist.neighbor_list
    with natural cutoff radii
    """

    def __init__(self, mult: float = 1.0, dtype=None, sort_edges: bool = False):
        super().__init__()
        self.mult = mult
        self.dtype = dtype if dtype is not None else torch.get_default_dtype()
        self.sort_edges = sort_edges
        self.forward = self.forward_dgl
        self.covalent_radii = CovalentRadius()

    def forward_ase(self, x: nfflr.Atoms):
        at = nfflr.to_ase(x)
        # per-atom cutoffs
        cutoffs = ase.neighborlist.natural_cutoffs(at, mult=self.mult)
        i, j, D = ase.neighborlist.neighbor_list("ijD", at, cutoffs)
        g = dgl.graph((j, i), num_nodes=len(at))
        g.ndata["coord"] = x.positions
        g.edata["r"] = torch.from_numpy(D).type(self.dtype)
        g.ndata["atomic_number"] = x.numbers.type(torch.int)

        if self.sort_edges:
            g = sort_edges_by_dst(g)

        return g

    def forward_dgl(self, x: nfflr.Atoms):

        # per-atom cutoffs
        radii = self.covalent_radii(x.numbers)

        # construct fixed radius graph
        global_cutoff = self.mult * 2 * radii.max()
        g = periodic_radius_graph(x, r=global_cutoff, dtype=self.dtype)

        # calculate natural cutoffs
        cutoffs = self.mult * dgl.ops.u_add_v(g, radii, radii)
        rs = g.edata["r"].norm(dim=1)

        # drop edges - don't drop isolated nodes, discard edge info
        g = dgl.edge_subgraph(g, rs <= cutoffs, relabel_nodes=False, store_ids=False)

        if self.sort_edges:
            g = sort_edges_by_dst(g)

        return g


class PeriodicKShellGraph(torch.nn.Module):
    """Periodic k-neighbor shell graph construction.

    Parameters
    ----------
    k : int
        neighbor index defining radius of the shell graph
    cutoff : float
        maximum radial distance to consider
    dtype : torch.float
        dtype of the resulting graph features

    Returns
    -------
    dgl.DGLGraph

    """

    def __init__(
        self,
        k: int = 12,
        cutoff: float = 15.0,
        dtype=torch.float,
        sort_edges: bool = False,
    ):
        super().__init__()
        self.k = k
        self.cutoff = cutoff
        self.dtype = dtype
        self.sort_edges = sort_edges

    def forward(self, x: nfflr.Atoms):
        g = periodic_kshell_graph(x, k=self.k, r=self.cutoff, dtype=self.dtype)
        if self.sort_edges:
            g = sort_edges_by_dst(g)
        return g
