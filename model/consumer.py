# consumer.py
# Consumer agent class

import random
import math
from typing import List


class Consumer:
    """Individual consumer agent"""
    
    def __init__(self, consumer_id: int, init_choice: int, qualities: List[float]):
        self.id = consumer_id
        self.choice = init_choice  # 0=orange, 1=blue
        
        # State variables
        self.satisfaction = [0.0, 0.0]      # satisfaction for each product
        self.personal_exp = [0.0, 0.0]      # personal experience for each product
        self.utilities = [0.0, 0.0]         # overall utility for each product
        
        # Position for network formation （for 850x450 canvas)
        self.x = random.uniform(40, 840)   # 左右留出 40px 边距
        self.y = random.uniform(40, 440)   # 上下留出 40px 边距
        
        # Neighbors (will be set by network)
        self.neighbors = []
        
        # Reference to qualities
        self.qualities = qualities
        
        # Initialize based on choice
        if init_choice == 0:
            self.utilities = [1.0, 0.0]
        else:
            self.utilities = [0.0, 1.0]
        
        self.update_satisfaction()
    
    def update_satisfaction(self):
        """Update satisfaction based on current choice (logarithmic relationship)"""
        q = self.qualities[self.choice]
        # Logarithmic satisfaction: log10(1 + 9*q)
        self.satisfaction[self.choice] = math.log10(1 + 9 * q)
        # Linear version (alternative):
        # self.satisfaction[self.choice] = q
    
    def update_product_quality(self, new_qualities):
        """Update product qualities and recalculate satisfaction"""
        self.qualities = new_qualities
        self.update_satisfaction()

    def decide(self, explore_rate: float) -> int:
        """
        Make consumption decision based on:
        1. Satisfaction (probability to stick)
        2. Random exploration
        3. Higher utility
        """
        # Priority 1: Stick with current product if satisfied
        if random.random() < self.satisfaction[self.choice]:
            return self.choice
        
        # Priority 2: Random exploration
        if random.random() < explore_rate:
            return 1 - self.choice
        
        # Priority 3: Choose product with higher utility
        if self.utilities[0] > self.utilities[1]:
            return 0
        elif self.utilities[1] > self.utilities[0]:
            return 1
        else:
            return self.choice  # keep current if equal
    
    def get_position(self):
        """Return position as tuple"""
        return (self.x, self.y)