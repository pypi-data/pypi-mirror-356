"""Atomistic LIne Graph Neural Network.

A crystal line graph network dgl implementation.
"""
from plum import dispatch
from typing import Tuple, Union, Optional, Literal, Callable
from dataclasses import dataclass

import torch
from torch import nn

import dgl
import dgl.function as fn
from dgl.nn import AvgPooling, SumPooling

import nfflr
from nfflr.nn import (
    RBFExpansion,
    MLPLayer,
    ALIGNNConv,
    EdgeGatedGraphConv,
    AttributeEmbedding,
    PeriodicRadiusGraph,
    Cosine,
)

from nfflr.data.graph import (
    compute_bond_cosines,
    compute_bond_cosines_coincident,
    edge_coincidence_graph,
)


@dataclass
class ALIGNNFFConfig:
    """Hyperparameters for alignn force field"""

    transform: Callable = PeriodicRadiusGraph(cutoff=5.0)
    triplet_style: Literal["line_graph", "coincident"] = "line_graph"
    cutoff: torch.nn.Module = Cosine(5.0)
    local_cutoff: float = 4.0
    alignn_layers: int = 4
    gcn_layers: int = 4
    atom_features: str = "cgcnn"
    edge_input_features: int = 80
    triplet_input_features: int = 40
    embedding_features: int = 64
    hidden_features: int = 256
    output_features: int = 1
    compute_forces: bool = True
    energy_units: Literal["eV", "eV/atom"] = "eV"
    reference_energies: Optional[Literal["fixed", "trainable"]] = None


class ALIGNNFF(nn.Module):
    """Atomistic Line graph network.

    Chain alternating gated graph convolution updates on crystal graph
    and atomistic line graph.
    """

    def __init__(self, config: ALIGNNFFConfig = ALIGNNFFConfig()):
        """Initialize class with number of input features, conv layers."""
        super().__init__()
        self.config = config
        self.cutoff = config.cutoff
        self.neighbor_transform = self.config.transform

        if config.atom_features == "embedding":
            self.atom_embedding = nn.Embedding(108, config.hidden_features)
        else:
            self.atom_embedding = AttributeEmbedding(
                config.atom_features, d_model=config.hidden_features
            )

        if config.reference_energies is not None:
            self.reference_energy = nfflr.nn.AtomicReferenceEnergy(
                requires_grad=config.reference_energies == "trainable"
            )

        self.edge_embedding = nn.Sequential(
            RBFExpansion(vmin=0, vmax=8.0, bins=config.edge_input_features),
            MLPLayer(config.edge_input_features, config.embedding_features),
            MLPLayer(config.embedding_features, config.hidden_features),
        )
        self.angle_embedding = nn.Sequential(
            RBFExpansion(vmin=-1, vmax=1.0, bins=config.triplet_input_features),
            MLPLayer(config.triplet_input_features, config.embedding_features),
            MLPLayer(config.embedding_features, config.hidden_features),
        )

        width = config.hidden_features
        self.alignn_layers = nn.ModuleList()
        for idx in range(1, config.alignn_layers + 1):
            skipnorm = idx == config.alignn_layers
            self.alignn_layers.append(ALIGNNConv(width, width, skip_last_norm=skipnorm))

        self.gcn_layers = nn.ModuleList()
        for idx in range(1, config.gcn_layers + 1):
            skipnorm = idx == config.gcn_layers
            self.gcn_layers.append(
                EdgeGatedGraphConv(width, width, skip_edgenorm=skipnorm)
            )

        if self.config.energy_units == "eV/atom":
            self.readout = AvgPooling()
        elif self.config.energy_units == "eV":
            self.readout = SumPooling()

        self.fc = nn.Linear(config.hidden_features, config.output_features)

        self.reset_atomic_reference_energies()

    def reset_atomic_reference_energies(self, values: Optional[torch.Tensor] = None):
        if hasattr(self, "reference_energy"):
            self.reference_energy.reset_parameters(values=values)

    def get_line_graph(self, g):
        return edge_coincidence_graph(g, shared=True, cutoff=self.config.local_cutoff)

    def transform(self, a: nfflr.Atoms):
        """Neighbor list and bond pair graph construction.

        Does not share features to facilitate autograd.
        """
        g = self.config.transform(a)
        lg = self.get_line_graph(g)
        return g, lg

    @dispatch
    def forward(self, x):
        print("convert")
        return self.forward(nfflr.Atoms(x))

    @dispatch
    def forward(self, x: nfflr.Atoms):
        device = next(self.parameters()).device
        return self.forward(self.neighbor_transform(x).to(device))

    @dispatch
    def forward(
        self,
        g: Union[Tuple[dgl.DGLGraph, dgl.DGLGraph], dgl.DGLGraph],
    ):
        """ALIGNN : start with `atom_features`.

        x: atom features (g.ndata)
        y: bond features (g.edata and lg.ndata)
        z: angle features (lg.edata)
        """
        # print("forward")
        config = self.config

        if isinstance(g, dgl.DGLGraph):
            lg = None
        else:
            g, lg = g

        g = g.local_var()

        # to compute forces, take gradient wrt g.edata["r"]
        # need to add bond vectors to autograd graph
        if config.compute_forces:
            g.edata["r"].requires_grad_(True)

        # initial node features: atom feature network...
        atomic_number = g.ndata.pop("atomic_number").int()
        x = self.atom_embedding(atomic_number)

        # initial bond features
        bondlength = torch.norm(g.edata["r"], dim=1)
        y = self.edge_embedding(bondlength)
        g.edata["y"] = y

        if config.cutoff is not None:
            # save cutoff function value for application in EdgeGatedGraphconv
            g.edata["cutoff_value"] = self.config.cutoff(bondlength)

        if len(self.alignn_layers) > 0:
            if lg is None:
                lg = self.get_line_graph(g)

            lg.ndata["r"] = g.edata["r"]

            # compute angle features (don't break autograd graph with precomputed lg)
            if self.config.triplet_style == "line_graph":
                lg.apply_edges(compute_bond_cosines)
            elif self.config.triplet_style == "coincident":
                lg.apply_edges(compute_bond_cosines_coincident)

            z = self.angle_embedding(lg.edata.pop("h"))

            # add triplet cutoff
            lg.apply_edges(fn.u_sub_v("r", "r", "r_kj"))
            fcut_kj = self.cutoff(torch.norm(lg.edata["r_kj"], dim=1, keepdim=False))
            lg.ndata["fcut"] = g.edata["cutoff_value"]
            lg.apply_edges(fn.u_mul_v("fcut", "fcut", "fcut_pair"))
            fcut_kj = fcut_kj * lg.edata["fcut_pair"]
            lg.edata["cutoff_value"] = fcut_kj

        # ALIGNN updates: update node, edge, triplet features
        for alignn_layer in self.alignn_layers:
            x, y, z = alignn_layer(g, lg, x, y, z)

        # gated GCN updates: update node, edge features
        for gcn_layer in self.gcn_layers:
            x, y = gcn_layer(g, x, y)

        # predict per-atom energy contribution (in eV)
        atomwise_energy = self.fc(x)
        if hasattr(self, "reference_energy"):
            atomwise_energy += self.reference_energy(atomic_number)

        # total energy prediction
        # if config.energy_units = eV/atom, mean reduction
        output = torch.squeeze(self.readout(g, atomwise_energy))

        if config.compute_forces:
            forces, virial = nfflr.autograd_forces(
                output,
                g.edata["r"],
                g,
                energy_units=config.energy_units,
                compute_virial=True,
            )

            return dict(
                energy=output,
                forces=forces,
                virial=virial,
            )

        return output
