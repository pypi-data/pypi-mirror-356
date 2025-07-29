from typing import TypedDict, TypeVar

from networkx import Graph

from heirarchical_leiden.leiden import leiden
from heirarchical_leiden.quality_functions import QualityFunction
from heirarchical_leiden.utils import Partition

T = TypeVar("T")


class HierarchicalPartition(TypedDict):
    partition: Partition
    level: int
    children: dict[int, "HierarchicalPartition"]


def hierarchical_leiden(
    G: Graph,
    𝓗: QualityFunction[T],
    𝓟: Partition[T] | None = None,
    θ: float = 0.3,
    γ: float = 0.05,
    weight: str | None = None,
    partition_max_size: int = 64,
    level: int = 0,
) -> HierarchicalPartition:
    """
    Perform the Leiden algorithm for community detection.

    Parameters
    ----------
    G : Graph
        The graph / network to process.
    𝓗 : QualityFunction[T]
        A quality function to optimize.
    𝓟 : Partition[T], optional
        A partition to use as basis, leave at the default of `None` when none is available.
    θ : float, optional
        The θ parameter of the Leiden method, which determines the randomness in the refinement phase of the Leiden
        algorithm, default value of 0.3.
    γ : float, optional
        The γ parameter of the Leiden method, default value of 0.05.
    weight : str | None, optional
        The edge weight attribute to use, default value of None.
    partition_max_size : int, optional
        The maximum size of a partition. If the partition is larger than this size, it will be split into smaller partitions.
        Default value of 64.
    level : int, optional
        The current level in the hierarchy, default value of 0.

    :returns: A HierarchicalPartition of G into communities.
    """
    # Apply Leiden algorithm to get the partition
    partition = leiden(G, 𝓗, 𝓟, θ, γ, weight)

    # Initialize the hierarchical partition
    children: dict[int, HierarchicalPartition] = {}

    # Process each community
    for idx, community in enumerate(partition.communities):
        community: set[T]

        # If the community is larger than the maximum size, recursively partition it
        if len(community) > partition_max_size:
            # Create a subgraph for this community
            subgraph = G.subgraph(community).copy()

            # Recursively apply hierarchical Leiden to the subgraph
            child_partition = hierarchical_leiden(subgraph, 𝓗, None, θ, γ, weight, partition_max_size, level + 1)
            children[idx] = child_partition

    # Create and return the hierarchical partition
    result: HierarchicalPartition = {"partition": partition, "level": level, "children": children}

    return result
