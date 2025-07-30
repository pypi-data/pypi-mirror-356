#!/usr/bin/env python3

"""Implement the kernel subdivision algorithm."""

import itertools

import networkx as nx
import numpy as np

from morphomath.kernel import Kernel


def classical_loss(tree: nx.MultiDiGraph, *nodes: Kernel) -> int:
    """Return the loss of this decomposition."""
    # attrs = tree.nodes[node]
    # compute loss from scratch
    all_nodes = set()
    new_predecessors = set(nodes)
    while new_predecessors:
        all_nodes |= new_predecessors
        new_predecessors = {
            n_ for n in new_predecessors for n_ in tree.predecessors(n)
        }
    return len(all_nodes) - 1  # it is the number of comparisons


def combine(kernel_1: Kernel, kernel_2: Kernel, kernel_ref: Kernel) -> tuple[tuple, Kernel]:
    """Yield all the merges of the 2 kernels that remain in the reference kernel."""
    shifts = {  # relative shift
        tuple(a2i - a1i for a1i, a2i in zip(a_1, a_2)) #  a_2 - a_1
        for a_1, a_2 in itertools.product(
            kernel_ref.anchors(kernel_1),
            kernel_ref.anchors(kernel_2),
        )
    }
    pt1 = set(map(tuple, kernel_1.points_array.tolist()))
    for shift in shifts:
        pt2 = kernel_2.points_array + np.asarray(shift)[None, :]
        points = pt1 | set(map(tuple, pt2.tolist()))
        yield shift, Kernel._from_points(points)


def remove_branch(tree: nx.MultiDiGraph, nodes: set[Kernel]):
    """Retire du graph le noeud et tous les descendants."""
    successors = nodes
    while successors := {s for n in successors for s in tree.successors(n)}:
        nodes |= successors
    tree.remove_nodes_from(nodes)


def subdivision(kernel: Kernel, loss: callable) -> nx.MultiDiGraph:
    """Yield the optimal kernel decomposition."""
    # tree initialisation
    tree = nx.MultiDiGraph(name="kernel subdivision")
    leaves = [Kernel(np.ones((1,)*kernel.dim, dtype=np.uint8))]
    tree.add_node(leaves[0])
    loss_val = len(kernel.points) - 1  # maximal loss

    # exploration
    while leaves:
        print(f"The {len(tree)}-node graph still contains {len(leaves)} unexplored leaves.")
        leaf = leaves.pop(0)
        for node, shift, new_leaf in (
            (node_, shift_, new_leaf_)
            for node_ in (n for n in list(tree.nodes) if loss(tree, n) < loss_val)
            for shift_, new_leaf_ in combine(node_, leaf, kernel)
        ):
            # premature elimination of branches doomed to failure
            if new_leaf in {node, leaf}:  # case recursive node
                continue
            new_loss = loss(tree, node, leaf) + 1
            is_solution = new_leaf == kernel
            if (not is_solution) and new_loss >= loss_val:
                continue
            # colision case
            if new_leaf in tree:
                if new_loss >= loss(tree, new_leaf):  # we keep the solution if it is better
                    continue
                tree.remove_edges_from([(p, new_leaf) for p in tree.predecessors(new_leaf)])
            # add the new node to the graph
            else:
                leaves.insert(0, new_leaf)  # faster heuristic than append
            tree.add_edge(node, new_leaf, shift=(0,)*kernel.dim)
            tree.add_edge(leaf, new_leaf, shift=shift)
            # case one solution found
            if new_leaf == kernel:
                print(f"solution with loss {new_loss}")
                yield extract_branch(tree, kernel)
                # filtering
                loss_val = new_loss
                leaves = [l for l in leaves if loss(tree, l) < loss_val]
                remove_branch(tree, {n for n in tree.nodes if loss(tree, n) >= loss_val} - {kernel})
                break


def extract_branch(tree: nx.MultiDiGraph, leaf: Kernel) -> nx.MultiDiGraph:
    """Extract the subtree of the kernel decomposition."""
    # get all predescessors
    all_nodes = set()
    new_predecessors = {leaf}
    while new_predecessors:
        all_nodes |= new_predecessors
        new_predecessors = {
            n_ for n in new_predecessors for n_ in tree.predecessors(n)
        }
    # exctract subgraph
    return tree.subgraph(all_nodes)


def save_dot(path, tree):
    """Write the graph as a .dot file."""
    def kernel_to_str(kernel: np.ndarray) -> str:
        """Convertie le kernel en str."""
        match kernel.ndim:
            case 1:
                return "".join("1" if e else "0" for e in kernel.tolist())
            case 2:
                return "\n".join(kernel_to_str(l) for l in kernel)
            case _:
                return str(kernel)
    new_tree = nx.MultiDiGraph()
    for node in tree.nodes:
        new_tree.add_node(kernel_to_str(node.tensor))
    for src, dst, idx in tree.edges:
        edge_data = tree[src][dst][idx]
        new_tree.add_edge(
            kernel_to_str(src.tensor),
            kernel_to_str(dst.tensor),
            label="\n".join(f"{k}={v}" for k, v in edge_data.items()),
            **edge_data,
        )
    nx.drawing.nx_pydot.write_dot(new_tree, path)


if __name__ == "__main__":
    ker = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    for subtree in subdivision(Kernel(ker), classical_loss):
        save_dot("/tmp/kernel_subdivision.dot", subtree)
