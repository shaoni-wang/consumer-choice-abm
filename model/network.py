# network.py
# Social network construction utilities

import random
import math
from typing import List, Tuple
from .consumer import Consumer


def build_geometric_network(consumers: List[Consumer], target_edges: int):
    """
    Build network by connecting each consumer to nearest unconnected neighbors
    until target number of edges is reached
    """
    n = len(consumers)
    edges = set()
    
    # Precompute all pairwise distances (simplified for small n)
    # For large n, use kd-tree for efficiency
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = _distance(consumers[i], consumers[j])
            distances.append((dist, i, j))
    
    # Sort by distance
    distances.sort(key=lambda x: x[0])
    
    # Add edges until target reached
    for dist, i, j in distances:
        if len(edges) >= target_edges:
            break
        if (j, i) not in edges:
            edges.add((i, j))
    
    # Build neighbor lists
    for i, j in edges:
        consumers[i].neighbors.append(consumers[j])
        consumers[j].neighbors.append(consumers[i])


def _distance(c1: Consumer, c2: Consumer) -> float:
    """Euclidean distance between two consumers"""
    dx = c1.x - c2.x
    dy = c1.y - c2.y
    return math.sqrt(dx*dx + dy*dy)


def get_adjacency_list(consumers: List[Consumer]) -> List[List[int]]:
    """Return adjacency list as list of neighbor IDs"""
    adj = []
    for c in consumers:
        adj.append([n.id for n in c.neighbors])
    return adj