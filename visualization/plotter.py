# plotter.py
# Visualization utilities

import matplotlib.pyplot as plt
from typing import List, Optional


class Plotter:
    """Handle visualization of model results"""
    
    def __init__(self):
        self.fig = None
        self.axes = None
    
    def setup_figure(self):
        """Initialize figure with subplots"""
        self.fig, self.axes = plt.subplots(1, 2, figsize=(12, 5))
        self.fig.suptitle('Consumer Choice Model Simulation')
        
        # Left: Market share
        self.axes[0].set_xlabel('Time Step')
        self.axes[0].set_ylabel('Market Share (%)')
        self.axes[0].set_title('Orange Product Market Share')
        self.axes[0].grid(True, alpha=0.3)
        
        # Right: Clustering coefficient
        self.axes[1].set_xlabel('Time Step')
        self.axes[1].set_ylabel('Clustering Coefficient')
        self.axes[1].set_title('Consumer Clustering')
        self.axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
    
    def update_plots(self, history: dict, current_step: Optional[int] = None):
        """Update plots with current history"""
        if self.fig is None:
            self.setup_figure()
        
        # Clear axes
        for ax in self.axes:
            ax.clear()
        
        # Plot market share
        self.axes[0].plot(history['market_share'], 'o-', color='orange', markersize=3)
        self.axes[0].set_xlabel('Time Step')
        self.axes[0].set_ylabel('Market Share (%)')
        self.axes[0].set_title('Orange Product Market Share')
        self.axes[0].grid(True, alpha=0.3)
        self.axes[0].set_ylim(0, 100)
        
        # Plot clustering
        self.axes[1].plot(history['clustering'], 's-', color='blue', markersize=3)
        self.axes[1].set_xlabel('Time Step')
        self.axes[1].set_ylabel('Clustering Coefficient')
        self.axes[1].set_title('Consumer Clustering')
        self.axes[1].grid(True, alpha=0.3)
        self.axes[1].set_ylim(0, 1)
        
        if current_step is not None:
            self.fig.suptitle(f'Consumer Choice Model - Step {current_step}')
        
        plt.pause(0.01)
    
    def save_figure(self, filename: str):
        """Save current figure to file"""
        if self.fig:
            self.fig.savefig(filename, dpi=150, bbox_inches='tight')
            print(f"Figure saved as {filename}")
    
    def show(self):
        """Display the plot"""
        if self.fig:
            plt.show()


def plot_network_simple(consumers, ax=None):
    """Simple network visualization (optional, requires networkx)"""
    try:
        import networkx as nx
        
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 8))
        
        G = nx.Graph()
        
        # Add nodes
        for c in consumers:
            G.add_node(c.id, choice=c.choice)
        
        # Add edges
        for c in consumers:
            for n in c.neighbors:
                if c.id < n.id:  # avoid double counting
                    G.add_edge(c.id, n.id)
        
        # Colors
        node_colors = ['orange' if G.nodes[i]['choice'] == 0 else 'blue' 
                       for i in G.nodes()]
        
        # Layout
        pos = {c.id: (c.x, c.y) for c in consumers}
        
        nx.draw(G, pos, node_color=node_colors, node_size=100, 
                ax=ax, with_labels=False, edge_color='gray', alpha=0.6)
        ax.set_title('Social Network Visualization')
        
    except ImportError:
        print("networkx not installed. Install with: pip install networkx")