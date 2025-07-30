# monkey-patched version of https://github.com/atomicarchitects/equiformer/blob/master/nets/dp_attention_transformer.py
# relies on local editable install of https://github.com/atomicarchitects/equiformer
from nets import dp_attention_transformer

import e3nn
import torch


def forward_periodic(self, g, **kwargs) -> torch.Tensor:
    """Modified forward pass from the reference implementation

    https://github.com/atomicarchitects/equiformer/blob/master/nets/dp_attention_transformer.py
    """
    g = g.local_var()

    # initial node features: atom feature network...
    node_atom = g.ndata.pop("atomic_number").long()

    # batch indicator vector for graph pooling
    batch = torch.repeat_interleave(torch.arange(g.batch_size, device=node_atom.device), g.batch_num_nodes())

    edge_src, edge_dst = g.edges()
    edge_vec = g.edata["r"]

    edge_sh = e3nn.o3.spherical_harmonics(
        l=self.irreps_edge_attr, x=edge_vec, normalize=True, normalization="component"
        )

    atom_embedding, atom_attr, atom_onehot = self.atom_embed(node_atom)
    edge_length = edge_vec.norm(dim=1)
    edge_length_embedding = self.rbf(edge_length, None, None, None)
    edge_degree_embedding = self.edge_deg_embed(atom_embedding, edge_sh,
        edge_length_embedding, edge_src, edge_dst, batch)
    node_features = atom_embedding + edge_degree_embedding
    node_attr = torch.ones_like(node_features.narrow(1, 0, 1))

    for blk in self.blocks:
        node_features = blk(node_input=node_features, node_attr=node_attr,
            edge_src=edge_src, edge_dst=edge_dst, edge_attr=edge_sh,
            edge_scalars=edge_length_embedding,
            batch=batch)

    node_features = self.norm(node_features, batch=batch)
    if self.out_dropout is not None:
        node_features = self.out_dropout(node_features)
    outputs = self.head(node_features)
    outputs = self.scale_scatter(outputs, batch, dim=0)

    if self.scale is not None:
        outputs = self.scale * outputs

    return outputs.squeeze()

# monkey patch the equivariante transformer model
dp_attention_transformer.DotProductAttentionTransformer.forward = forward_periodic

def equiformer(irreps_in="64x0e", radius=5.0, max_atom_type=128):

    # set up model
    model = dp_attention_transformer.dot_product_attention_transformer_l2(irreps_in, radius)

    # modify atom embedding layer since equiformer initializes embedding size from global variable
    model.atom_embed = dp_attention_transformer.NodeEmbeddingNetwork(model.irreps_node_embedding, max_atom_type)

    # reinitialize weights just in case
    model.apply(model._init_weights)

    return model
