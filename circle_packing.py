"""
Circle Packing - Algorithmic Art
Creates densely packed circles that don't overlap
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Parameters
NUM_CIRCLES = 1000
MIN_RADIUS = 0.02
MAX_RADIUS = 0.3
CANVAS_SIZE = 10
MAX_ATTEMPTS = 1000
COLORMAP = 'hsv'
COLOR_BY = 'size'  # 'size', 'position', or 'random'
BACKGROUND = '#0a0a0a'
EDGE_COLOR = None  # None or color like '#ffffff'
EDGE_WIDTH = 0.5
ALPHA = 0.8
DPI = 150
OUTPUT_FILE = 'circle_packing.jpg'

def check_collision(x, y, r, circles):
    """Check if new circle collides with existing ones"""
    for cx, cy, cr in circles:
        dist = np.sqrt((x - cx)**2 + (y - cy)**2)
        if dist < r + cr:
            return True
    return False

def create_circle_packing():
    """Create circle packing art"""
    
    print("Packing circles...")
    
    circles = []
    attempts = 0
    
    while len(circles) < NUM_CIRCLES and attempts < NUM_CIRCLES * MAX_ATTEMPTS:
        # Random position
        x = np.random.uniform(-CANVAS_SIZE/2, CANVAS_SIZE/2)
        y = np.random.uniform(-CANVAS_SIZE/2, CANVAS_SIZE/2)
        
        # Start with max radius and shrink if needed
        r = np.random.uniform(MIN_RADIUS, MAX_RADIUS)
        
        # Check if it fits
        if not check_collision(x, y, r, circles):
            circles.append((x, y, r))
            if len(circles) % 100 == 0:
                print(f"  Packed {len(circles)} circles...")
        
        attempts += 1
    
    print(f"Successfully packed {len(circles)} circles")
    print("Creating visualization...")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 12), dpi=DPI)
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)
    
    cmap = plt.get_cmap(COLORMAP)
    
    # Draw circles
    for i, (x, y, r) in enumerate(circles):
        # Determine color
        if COLOR_BY == 'size':
            color_val = (r - MIN_RADIUS) / (MAX_RADIUS - MIN_RADIUS)
        elif COLOR_BY == 'position':
            dist = np.sqrt(x**2 + y**2)
            color_val = dist / (CANVAS_SIZE / 2)
        else:  # random
            color_val = np.random.rand()
        
        color = cmap(color_val)
        
        circle = Circle((x, y), r, facecolor=color, 
                       edgecolor=EDGE_COLOR if EDGE_COLOR else color,
                       linewidth=EDGE_WIDTH, alpha=ALPHA)
        ax.add_patch(circle)
    
    ax.set_xlim(-CANVAS_SIZE/2, CANVAS_SIZE/2)
    ax.set_ylim(-CANVAS_SIZE/2, CANVAS_SIZE/2)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout(pad=0)
    plt.savefig(OUTPUT_FILE, dpi=DPI, bbox_inches='tight', 
                pad_inches=0, facecolor=BACKGROUND)
    print(f"Saved: {OUTPUT_FILE}")
    plt.show()

if __name__ == "__main__":
    print("Creating Circle Packing art...")
    create_circle_packing()
    print("Complete!")
