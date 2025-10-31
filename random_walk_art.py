"""
Random Walk Art - Algorithmic Art
Creates beautiful patterns from multiple random walks with memory
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# Parameters
NUM_WALKERS = 30
STEPS_PER_WALKER = 2000
STEP_SIZE = 0.1
ATTRACTION_TO_CENTER = 0.01
REPULSION_FROM_OTHERS = 0.02
COLORMAP = 'viridis'
BACKGROUND = '#0a0a0a'
LINE_WIDTH = 1.0
ALPHA = 0.6
DPI = 150
OUTPUT_FILE = 'random_walk_art.jpg'

def create_random_walk_art():
    """Create art from interacting random walks"""
    
    print("Simulating random walks...")
    
    # Initialize walkers at random positions
    walkers = np.random.randn(NUM_WALKERS, 2) * 2
    
    # Store all trajectories
    all_trajectories = [[] for _ in range(NUM_WALKERS)]
    
    # Simulate walks
    for step in range(STEPS_PER_WALKER):
        for i in range(NUM_WALKERS):
            # Random walk component
            random_step = np.random.randn(2) * STEP_SIZE
            
            # Attraction to center
            center_force = -walkers[i] * ATTRACTION_TO_CENTER
            
            # Repulsion from other walkers
            repulsion = np.zeros(2)
            for j in range(NUM_WALKERS):
                if i != j:
                    diff = walkers[i] - walkers[j]
                    dist = np.linalg.norm(diff) + 0.1
                    if dist < 2.0:  # Only repel if close
                        repulsion += diff / dist**2 * REPULSION_FROM_OTHERS
            
            # Update position
            walkers[i] += random_step + center_force + repulsion
            
            # Store position
            all_trajectories[i].append(walkers[i].copy())
    
    print("Creating visualization...")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 12), dpi=DPI)
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)
    
    cmap = plt.get_cmap(COLORMAP)
    
    # Plot each trajectory
    for i, trajectory in enumerate(all_trajectories):
        points = np.array(trajectory)
        
        # Create line segments
        segments = []
        for j in range(len(points) - 1):
            segments.append([points[j], points[j + 1]])
        
        # Color gradient
        colors = np.linspace(0, 1, len(segments))
        
        # Color based on walker ID
        walker_color = cmap(i / NUM_WALKERS)
        
        lc = LineCollection(segments, colors=[walker_color] * len(segments),
                           linewidths=LINE_WIDTH, alpha=ALPHA)
        ax.add_collection(lc)
    
    # Calculate bounds
    all_points = np.vstack([np.array(traj) for traj in all_trajectories])
    max_range = np.max(np.abs(all_points)) * 1.1
    
    ax.set_xlim(-max_range, max_range)
    ax.set_ylim(-max_range, max_range)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout(pad=0)
    plt.savefig(OUTPUT_FILE, dpi=DPI, bbox_inches='tight', 
                pad_inches=0, facecolor=BACKGROUND)
    print(f"Saved: {OUTPUT_FILE}")
    plt.show()

if __name__ == "__main__":
    print("Creating Random Walk art...")
    create_random_walk_art()
    print("Complete!")
