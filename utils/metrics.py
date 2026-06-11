# metrics.py
# Utility functions for calculating metrics

from typing import List
from ..model.consumer import Consumer


def compute_herfindahl_index(consumers: List[Consumer]) -> float:
    """
    Compute Herfindahl-Hirschman Index (HHI) for market concentration
    0 = perfect competition, 1 = monopoly
    """
    n = len(consumers)
    orange_pct = sum(1 for c in consumers if c.choice == 0) / n
    blue_pct = 1 - orange_pct
    return orange_pct**2 + blue_pct**2


def compute_entropy(consumers: List[Consumer]) -> float:
    """
    Compute Shannon entropy of market shares
    Higher = more diverse, Lower = more concentrated
    """
    import math
    n = len(consumers)
    orange_pct = sum(1 for c in consumers if c.choice == 0) / n
    blue_pct = 1 - orange_pct
    
    entropy = 0.0
    for p in [orange_pct, blue_pct]:
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy


def count_switches(consumers: List[Consumer], previous_choices: List[int]) -> int:
    """Count how many consumers switched products"""
    switches = 0
    for i, c in enumerate(consumers):
        if c.choice != previous_choices[i]:
            switches += 1
    return switches