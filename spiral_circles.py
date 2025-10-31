"""
Spiral Circles - Algorithmic Art
Creates a golden spiral pattern with nested circles and gradient coloring
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.colors as mcolors

# Parameters
NUM_CIRCLES = 150
GOLDEN_RATIO = (1 + np.sqrt(5)) / 2
SPIRAL_TIGHTNESS = 0.15
ROTATION_SPEED = 137.5  # Golden angle in degrees
COLORMAP = 'twilight'
BACKGROUND = '#0a0a0a'
DPI = 150
OUTPUT_FILE = 'spiral_circles.jpg'

def create_spiral_circles():
    """Create a beautiful spiral pattern with circles"""
    
    fig, ax = plt.subplots(figsize=(12, 12), dpi=DPI)
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)
    
    # Get colormap
    cmap = plt.get_cmap(COLORMAP)
    
    # Generate spiral points
    for i in range(NUM_CIRCLES):
        # Polar coordinates with golden angle
        angle = i * np.radians(ROTATION_SPEED)
        radius = SPIRAL_TIGHTNESS * np.sqrt(i)
        
        # Convert to cartesian
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        
        # Circle size decreases with distance
        circle_size = 0.5 * (1 - i / NUM_CIRCLES) + 0.1
        
        # Color based on position
        color = cmap(i / NUM_CIRCLES)
        
        # Add circle
        circle = Circle((x, y), circle_size, 
                       color=color, alpha=0.6, 
                       linewidth=1, edgecolor=color)
        ax.add_patch(circle)
    
    # Set limits and aspect
    max_radius = SPIRAL_TIGHTNESS * np.sqrt(NUM_CIRCLES) + 1
    ax.set_xlim(-max_radius, max_radius)
    ax.set_ylim(-max_radius, max_radius)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout(pad=0)
    plt.savefig(OUTPUT_FILE, dpi=DPI, bbox_inches='tight', 
                pad_inches=0, facecolor=BACKGROUND)
    print(f"Saved: {OUTPUT_FILE}")
    plt.show()

if __name__ == "__main__":
    print("Creating Spiral Circles art...")
    create_spiral_circles()
    print("Complete!")
