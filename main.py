# main.py
# Main entry point for running the simulation

import sys
import os

# Add parent directory to path if needed
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from model.abm_model import ABM_Model
from visualization.plotter import Plotter


def run_simulation(visualize=True):
    """
    Run the consumer choice simulation
    
    Args:
        visualize: Whether to show real-time plots
    """
    print("=" * 50)
    print("Consumer Choice ABM Simulation")
    print("=" * 50)
    print(f"Parameters:")
    print(f"  - Number of consumers: {Config.NUM_CONSUMERS}")
    print(f"  - Avg connections: {Config.AVG_CONNECTIONS}")
    print(f"  - Quality (orange/blue): {Config.QUALITY_ORANGE}/{Config.QUALITY_BLUE}")
    print(f"  - Norm influence: {Config.NORM_INFLUENCE}")
    print(f"  - Info exchange: {Config.INFO_EXCHANGE}")
    print(f"  - Exploration rate: {Config.EXPLORATION}")
    print("=" * 50)
    
    # Initialize model
    model = ABM_Model(Config)
    model.setup()
    
    print(f"\nInitial market share (orange): {model.get_market_share():.1f}%")
    
    # Setup visualization
    if visualize:
        plotter = Plotter()
        plotter.setup_figure()
    
    # Run simulation
    print("\nRunning simulation...")
    for step in range(Config.NUM_STEPS):
        model.step()
        
        if visualize and step % 10 == 0:
            plotter.update_plots(model.history, step)
            print(f"  Step {step:3d}: Orange share = {model.get_market_share():5.1f}%, "
                  f"Clustering = {model.history['clustering'][-1]:.3f}")
    
    # Final results
    print("\n" + "=" * 50)
    print("SIMULATION COMPLETE")
    print("=" * 50)
    final_share = model.get_market_share()
    final_clustering = model.history['clustering'][-1]
    print(f"Final orange market share: {final_share:.1f}%")
    print(f"Final clustering coefficient: {final_clustering:.3f}")
    
    # Save plot if visualization was used
    if visualize:
        plotter.update_plots(model.history, Config.NUM_STEPS)
        plotter.save_figure("simulation_results.png")
        print("\nPlot saved as 'simulation_results.png'")
        
        # Optionally show interactive plot
        response = input("\nShow interactive plot? (y/n): ")
        if response.lower() == 'y':
            plotter.show()
    
    return model


def run_batch_experiments():
    """Run multiple simulations with different parameters"""
    results = []
    
    # Test different norm influence values
    norm_values = [0.0, 0.3, 0.6, 1.0]
    
    print("Running batch experiments...")
    for norm in norm_values:
        Config.NORM_INFLUENCE = norm
        model = ABM_Model(Config)
        model.setup()
        
        for _ in range(Config.NUM_STEPS):
            model.step()
        
        final_share = model.get_market_share()
        results.append((norm, final_share))
        print(f"  Norm influence = {norm}: Final share = {final_share:.1f}%")
    
    return results


if __name__ == "__main__":
    # Run standard simulation with visualization
    model = run_simulation(visualize=True)
    
    # Uncomment to run batch experiments instead:
    # results = run_batch_experiments()