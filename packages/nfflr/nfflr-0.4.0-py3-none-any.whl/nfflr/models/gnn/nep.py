"""NEP2

Neuroevolutionary potential v2 dgl implementation.
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

from nfflr.data.graph import (
    compute_bond_cosines,
    compute_bond_cosines_coincident,
    edge_coincidence_graph,
)
