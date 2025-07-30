from plum import dispatch
from torch import nn

import nfflr

class AbstractModel(nn.Module):
    @dispatch
    def forward(self, x):
        """Fallback method"""
        print("fallback")
        self.forward(nfflr.Atoms(x))
