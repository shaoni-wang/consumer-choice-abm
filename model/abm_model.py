import random
import math
from typing import List, Dict
from .consumer import Consumer
from .network import build_geometric_network


class ABM_Model:
    """Main model for consumer choice simulation"""
    
    def __init__(self, config):
        self.config = config
        self.consumers: List[Consumer] = []
        self.qualities = config.get_quality_list()
        self.step_count = 0
        self.history = {
            'market_share': [],
            'clustering': []
        }
        
        # Set random seed for reproducibility
        random.seed(config.SEED)
    
    def setup(self):
        """Initialize model: create consumers and build network"""
        self._create_consumers()
        self._build_network()
        self.step_count = 0
        self.history = {'market_share': [], 'clustering': []}
        self._record_stats()
    
    def _create_consumers(self):
        """Create consumer agents with initial choices"""
        self.consumers = []
        n = self.config.NUM_CONSUMERS
        init_orange_pct = self.config.INIT_ORANGE_PCT

        for i in range(n):
            # Random initial choice based on percentage
            if random.random() < init_orange_pct / 100:
                choice = 0  # orange
            else:
                choice = 1  # blue
            
            consumer = Consumer(i, choice, self.qualities)
            self.consumers.append(consumer)

    def _build_network(self):
        """Build social network between consumers"""
        target_edges = int(self.config.AVG_CONNECTIONS * self.config.NUM_CONSUMERS / 2)
        build_geometric_network(self.consumers, target_edges)
    
    def update_parameters(self, params):
        """Update model parameters dynamically"""
        self.config.NORM_INFLUENCE = params.get('norm_influence', self.config.NORM_INFLUENCE)
        self.config.INFO_EXCHANGE = params.get('info_exchange', self.config.INFO_EXCHANGE)
        self.config.EXPLORATION = params.get('exploration', self.config.EXPLORATION)
        self.config.QUALITY_ORANGE = params.get('quality_orange', self.config.QUALITY_ORANGE)
        self.config.QUALITY_BLUE = params.get('quality_blue', self.config.QUALITY_BLUE)
        
        # Update qualities list
        self.qualities = [self.config.QUALITY_ORANGE, self.config.QUALITY_BLUE]
        
        # Update all consumers' quality references
        for consumer in self.consumers:
            consumer.qualities = self.qualities
            # Recalculate satisfaction with new quality
            consumer.update_satisfaction()

    def step(self):
        """Execute one simulation step"""
        self._consume_phase()
        self._update_utilities()
        self.step_count += 1
        self._record_stats()
    
    def _consume_phase(self):
        """All consumers make their consumption decisions"""
        for consumer in self.consumers:
            new_choice = consumer.decide(self.config.EXPLORATION)
            if new_choice != consumer.choice:
                consumer.choice = new_choice
                consumer.update_satisfaction()
    
    def _update_utilities(self):
        """Update utilities based on personal experience and neighbor information"""
        for consumer in self.consumers:
            for option in [0, 1]:
                # 1. Update personal experience if this product is used
                if consumer.choice == option:
                    consumer.personal_exp[option] = self.qualities[option]
                
                # 2. Get information from neighbors (probabilistic)
                neighbor_info = 0.0
                if random.random() < self.config.INFO_EXCHANGE:
                    if any(n.choice == option for n in consumer.neighbors):
                        neighbor_info = self.qualities[option]
                
                # 3. Calculate norm utility (proportion of neighbors choosing option)
                norm_util = 0.0
                if consumer.neighbors:
                    same = sum(1 for n in consumer.neighbors if n.choice == option)
                    norm_util = same / len(consumer.neighbors)
                
                # 4. Combine personal experience and neighbor info
                self_info = consumer.personal_exp[option]
                prod_util = (self_info + neighbor_info) / 2.0
                
                # 5. Final utility with norm influence weight
                norm_w = self.config.NORM_INFLUENCE
                consumer.utilities[option] = norm_w * norm_util + (1 - norm_w) * prod_util
    
    def _record_stats(self):
        """Record current model statistics"""
        # Market share of orange product (choice=0)
        orange_count = sum(1 for c in self.consumers if c.choice == 0)
        market_share = orange_count / self.config.NUM_CONSUMERS * 100
        self.history['market_share'].append(market_share)
        
        # Clustering coefficient
        clustering = self._compute_clustering()
        self.history['clustering'].append(clustering)
    
    def _compute_clustering(self) -> float:
        """Compute average proportion of neighbors with same choice"""
        cluster_sum = 0.0
        for c in self.consumers:
            if not c.neighbors:
                cluster_sum += 0.0
            else:
                same = sum(1 for n in c.neighbors if n.choice == c.choice)
                cluster_sum += same / len(c.neighbors)
        return cluster_sum / self.config.NUM_CONSUMERS
    
    def get_market_share(self) -> float:
        """Return current market share of orange product (%)"""
        orange_count = sum(1 for c in self.consumers if c.choice == 0)
        return orange_count / self.config.NUM_CONSUMERS * 100
    
    def get_summary(self) -> Dict:
        """Return summary statistics"""
        return {
            'step': self.step_count,
            'market_share': self.history['market_share'][-1] if self.history['market_share'] else 0,
            'clustering': self.history['clustering'][-1] if self.history['clustering'] else 0
        }