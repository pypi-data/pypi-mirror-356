s = """../adata_P1_J1J11J14.h5ad ../tmp.h5ad --obs leiden --embedding umap --size 100 --max-distances 0 1 2 3 --jobs 16 --neighbors 5"""

#!/usr/bin/env python

import warnings
warnings.filterwarnings("ignore")

import os, std
import argparse, cli
from pathlib import Path

import anndata as ad
import bonesistools as bt

import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(
    prog="knnbs",
    description=
    """
    Compute cell manifolds using k-nearest neighbors-based subclusters (knnbs) algorithm. \
    Compute the k-nearest neighbors-based graph using an embedding space, \
    compute shortest path lengths in the graph and then search for cluster related-cell manifolds \
    using knnbs algorithm. The subclusters can be computed following two methods: \
    (1) searching for cell manifolds maximizing distances to other clusters' barycenters \
    and (2) searching for cell manifolds minimizing distances to self barycenter
    """,
    usage="python knnbs_macrostates.py <FILE> <FILE> [--csv <FILE>] --obs <LITERAL> [--max-distances <LITERAL...>] [--min-distances <LITERAL...>] [<args>]"
)

parser.add_argument(
    "infile",
    type=lambda x: Path(x).resolve(),
    metavar="FILE",
    help="input file storing counts and clusters (format: h5ad)"
)

parser.add_argument(
    "outfile",
    type=lambda x: Path(x).resolve(),
    metavar="FILE",
    help="output file storing knnbs macrostates (format: h5ad)"
)

parser.add_argument(
    "--csv",
    dest="csv",
    type=lambda x: Path(x).resolve(),
    required=False,
    default=None,
    metavar="FILE",
    help="output file storing macrostates (format: csv)"
)

parser.add_argument(
    "--obs",
    dest="obs",
    type=str,
    required=True,
    metavar="LITERAL",
    help="column name in adata.obs distinguishing clusters (required)"
)

parser.add_argument(
    "--embedding",
    dest="embedding",
    type=str,
    required=False,
    default="umap",
    choices=["pca","umap","tsne"],
    metavar="[pca|umap|tsne]",
    help="embedding projection used when calculating pairwise distances (default: umap)"
)

parser.add_argument(
    "--dimension",
    dest="dimension",
    type=int,
    required=False,
    default=None,
    metavar="INT",
    help="number of embedding dimensions used when calculating pairwise distances (default: None)"
)

parser.add_argument(
    "--metric",
    dest="metric",
    action=cli.Store_metric,
    required=False,
    default="euclidean",
    help="metric used when calculating pairwise distances (default: euclidean)"
)

parser.add_argument(
    "--neighbors",
    dest="neighbors",
    type=int,
    required=False,
    default=20,
    metavar="INT",
    help="number of closest neighbors for computing k-nearest neighbors graph (default: 20)"
)

parser.add_argument(
    "--size",
    dest="size",
    type=int,
    required=False,
    default=50,
    metavar="INT",
    help="number of cells in each macrostate (default: 50)"
)

parser.add_argument(
    "--method",
    dest="method",
    type=str,
    required=False,
    choices=["dijkstra", "bellman-ford"],
    default="dijkstra",
    metavar="[dijkstra|bellman-ford]",
    help="method used for computing pairwise shortest path lengths between cells and barycenters (default: dijkstra)"
)

parser.add_argument(
    "--max-distances",
    dest="max_distances",
    type=str,
    required=False,
    nargs="+",
    default=None,
    metavar="LITERAL",
    help="list of clusters for which macrostates are computed by maximizing distances to other clusters' barycenters (default: None)"
)

parser.add_argument(
    "--min-distances",
    dest="min_distances",
    type=str,
    required=False,
    nargs="+",
    default=None,
    metavar="LITERAL",
    help="list of clusters for which macrostates are computed by minimizing distances to self barycenter (default: None)"
)

parser.add_argument(
    "--jobs",
    dest="jobs",
    type=int,
    required=False,
    default=1,
    metavar="INT",
    help="number of allocated processors"
)

args = parser.parse_args(s.split())

if args.embedding == "pca":
    embedding = "X_pca"
elif args.embedding == "umap":
    embedding = "X_umap"
elif args.embedding == "tsne":
    embedding = "X_tsne"

if not Path(os.path.dirname(args.outfile)).exists():
    os.makedirs(Path(os.path.dirname(args.outfile)))

std.print_task(f"loading file {str(args.infile)}")
adata = ad.read_h5ad(args.infile)

if adata.obs[args.obs].dtype.name != "category":
    adata.obs[args.obs] = adata.obs[args.obs].astype("category")

if args.dimension is None:
    args.dimension = adata.obsm[embedding].shape[1]

if args.max_distances:
    for cluster in args.max_distances:
        if cluster not in adata.obs[args.obs].cat.categories:
            raise argparse.ArgumentError(None, f"cluster {cluster} in argument --max-distances not found in 'adata.obs[{args.obs}]'")
if args.min_distances:
    for cluster in args.min_distances:
        if cluster not in adata.obs[args.obs].cat.categories:
            raise argparse.ArgumentError(None, f"cluster {cluster} in argument --min-distances not found in 'adata.obs[{args.obs}]'")

bt.sct.pl.set_default_params()
embedding_label = "UMAP" if args.embedding == "umap" else "t-SNE"
use_rep="X_umap" if args.embedding == "umap" else "X_tsne"
bt.sct.pl.embedding_plot(
    adata,
    obs=args.obs,
    use_rep=use_rep,
    xlabel=r"$\mathrm{{{}_{{1}}}}$".format(embedding_label),
    ylabel=r"$\mathrm{{{}_{{2}}}}$".format(embedding_label),
    zlabel=r"$\mathrm{{{}_{{3}}}}$".format(embedding_label),
    figwidth=6,
    s=5,
    alpha=1,
    add_legend=True,
    lgd_params={
        "title":args.obs,
        "ncol":1,
        "markerscale":3,
        "frameon":True,
        "edgecolor":bt.sct.pl.get_color("black"),
        "shadow":False
    },
    n_components = 3 if adata.obsm[use_rep].shape[1] > 2 else 2,
    background_visible=False,
)
plt.show()

std.print_task("estimating k-nearest neighbors-based subclusters (knnbs)")
knnbs = bt.sct.tl.Knnbs(
    n_neighbors=args.neighbors,
    use_rep=embedding,
    n_components=args.dimension,
    metric=args.metric
)

std.print_info("computing k-nearest neighbors-based graph")
knnbs.fit(
    adata,
    obs=args.obs,
    n_jobs=args.jobs
)

std.print_info("computing pairwise shortest path lengths between cells and barycenters")
std.print_warning("this may take some time.")
knnbs.shortest_path_lengths(
    method=args.method,
    n_jobs=args.jobs
)

adata.obs["knnbs"] = knnbs.find_closest_cells_to_self_barycenter(size=200, key="knnbs")
adata.obs["knnbs"] = knnbs.find_furthest_cells_to_other_barycenters(size=200, key="knnbs")

bt.sct.pl.embedding_plot(
    adata,
    obs="knnbs",
    use_rep=use_rep,
    xlabel=r"$\mathrm{{{}_{{1}}}}$".format(embedding_label),
    ylabel=r"$\mathrm{{{}_{{2}}}}$".format(embedding_label),
    zlabel=r"$\mathrm{{{}_{{3}}}}$".format(embedding_label),
    figwidth=6,
    s=5,
    alpha=1,
    add_legend=True,
    lgd_params={
        "title":"knnbs",
        "ncol":1,
        "markerscale":3,
        "frameon":True,
        "edgecolor":bt.sct.pl.get_color("black"),
        "shadow":False
    },
    n_components = 3 if adata.obsm[use_rep].shape[1] > 2 else 2,
    background_visible=False,
)
plt.show()

use_rep = "X_wnn.umap"
std.print_task("estimating k-nearest neighbors-based subclusters (knnbs)")
knnbs = bt.sct.tl.Knnbs(
    n_neighbors=args.neighbors,
    use_rep=embedding,
    n_components=args.dimension,
    metric=args.metric
)

std.print_info("computing k-nearest neighbors-based graph")
knnbs.fit(
    adata,
    obs=args.obs,
    n_jobs=args.jobs
)

std.print_info("computing pairwise shortest path lengths between cells and barycenters")
std.print_warning("this may take some time.")
knnbs.shortest_path_lengths(
    method=args.method,
    n_jobs=args.jobs
)


_barycenters = bt.sct.tl.barycenters(
    adata,
    obs="leiden",
    use_rep=use_rep,
    n_components=2
)
bt.sct.pl.embedding_plot(
    adata,
    obs="leiden",
    use_rep=use_rep,
    xlabel=r"$\mathrm{{{}_{{1}}}}$".format(embedding_label),
    ylabel=r"$\mathrm{{{}_{{2}}}}$".format(embedding_label),
    zlabel=r"$\mathrm{{{}_{{3}}}}$".format(embedding_label),
    figwidth=6,
    s=5,
    alpha=1,
    add_legend=True,
    lgd_params={
        "title":"leiden",
        "ncol":1,
        "markerscale":3,
        "frameon":True,
        "edgecolor":bt.sct.pl.get_color("black"),
        "shadow":False
    },
    n_components = 3 if adata.obsm[use_rep].shape[1] > 2 else 2,
    background_visible=False,
)
for key in _barycenters.keys():
    plt.scatter(_barycenters[key][0],_barycenters[key][1], c=bt.sct.pl.get_color("black"),s=5)
plt.show()



adata.obs["knnbs"] = knnbs.find_closest_cells_to_self_barycenter(size=200, key="knnbs")
adata.obs["knnbs"] = knnbs.find_furthest_cells_to_other_barycenters(size=200, key="knnbs")

bt.sct.pl.embedding_plot(
    adata,
    obs="knnbs",
    use_rep=use_rep,
    xlabel=r"$\mathrm{{{}_{{1}}}}$".format(embedding_label),
    ylabel=r"$\mathrm{{{}_{{2}}}}$".format(embedding_label),
    zlabel=r"$\mathrm{{{}_{{3}}}}$".format(embedding_label),
    figwidth=6,
    s=5,
    alpha=1,
    add_legend=True,
    lgd_params={
        "title":"knnbs",
        "ncol":1,
        "markerscale":3,
        "frameon":True,
        "edgecolor":bt.sct.pl.get_color("black"),
        "shadow":False
    },
    n_components = 3 if adata.obsm[use_rep].shape[1] > 2 else 2,
    background_visible=False,
)



import networkx as nx
import numpy as np
from sklearn.metrics import pairwise_distances
from itertools import combinations

self = knnbs
obs=args.obs
n_jobs = args.jobs

X = bt.sct.tl.choose_representation(adata, use_rep=self.use_rep, n_components=self.n_components)

_kneighbors_graph = bt.sct.tl.kneighbors_graph(
    adata,
    n_neighbors=self.n_neighbors,
    n_components=self.n_components,
    use_rep=use_rep,
    metric=self.metric,
    create_using=nx.Graph,
    index_or_name="name",
    n_jobs=n_jobs
)

_barycenters = bt.sct.tl.barycenters(
    adata,
    obs=obs,
    use_rep=use_rep,
    n_components=self.n_components
)
for key, value in _barycenters.items():
    barycenter_coordinate = value.reshape(1,-1)
    distances = pairwise_distances(
        X,
        barycenter_coordinate,
        metric=self.metric,
        n_jobs=n_jobs
    ).reshape(1,-1)
    _kneighbors_graph.add_node(key)
    knn_indices = list(np.argpartition(distances, kth=self.n_neighbors, axis=1)[:, :self.n_neighbors].reshape(-1))
    distances = list(distances[0,knn_indices].reshape(-1))
    for obs_name, distance in zip(adata.obs.index[knn_indices], distances):
        _kneighbors_graph.add_edge(key, obs_name, distance=distance)

nx.number_connected_components(_kneighbors_graph)





####

'J14_AAGTTCGAGCGTCTGC-1'
'J11_TTCGGTCCAGGTTACT-1'