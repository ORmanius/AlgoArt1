"""
Recursive Tree - Algorithmic Art
Creates a beautiful fractal tree using recursion with gradient coloring
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# Parameters
INITIAL_LENGTH = 5.0
MIN_LENGTH = 0.1
BRANCH_ANGLE = 25  # degrees
LENGTH_RATIO = 0.7
NUM_ITERATIONS = 10
COLORMAP = 'autumn'
BACKGROUND = '#0a0a0a'
LINE_WIDTH_BASE = 3.0
DPI = 150
OUTPUT_FILE = 'recursive_tree.jpg'

class TreeDrawer:
    def __init__(self):
        self.segments = []
        self.depths = []
    
    def draw_branch(self, x, y, angle, length, depth, max_depth):
        """Recursively draw tree branches"""
        
        if length < MIN_LENGTH or depth > max_depth:
            return
        
        # Calculate end point
        x_end = x + length * np.cos(np.radians(angle))
        y_end = y + length * np.sin(np.radians(angle))
        
        # Store segment and depth
        self.segments.append([(x, y), (x_end, y_end)])
        self.depths.append(depth)
        
        # Recurse for left and right branches
        new_length = length * LENGTH_RATIO
        
        # Left branch
        self.draw_branch(x_end, y_end, angle + BRANCH_ANGLE, 
                        new_length, depth + 1, max_depth)
        
        # Right branch
        self.draw_branch(x_end, y_end, angle - BRANCH_ANGLE, 
                        new_length, depth + 1, max_depth)
        
        # Optional: center branch (creates denser tree)
        if depth < max_depth - 2 and np.random.rand() > 0.7:
            self.draw_branch(x_end, y_end, angle, 
                           new_length * 0.8, depth + 1, max_depth)

def create_recursive_tree():
    """Create recursive tree visualization"""
    
    print("Growing recursive tree...")
    
    # Create tree
    tree = TreeDrawer()
    tree.draw_branch(0, 0, 90, INITIAL_LENGTH, 0, NUM_ITERATIONS)
    
    print(f"Generated {len(tree.segments)} branches")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 14), dpi=DPI)
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)
    
    # Get colormap
    cmap = plt.get_cmap(COLORMAP)
    
    # Normalize depths for coloring
    max_depth = max(tree.depths)
    colors = [cmap(d / max_depth) for d in tree.depths]
    
    # Calculate line widths (thicker at base, thinner at tips)
    widths = [LINE_WIDTH_BASE * (1 - d / max_depth) ** 2 + 0.3 
              for d in tree.depths]
    
    # Create line collection
    lc = LineCollection(tree.segments, colors=colors, 
                       linewidths=widths, capstyle='round')
    ax.add_collection(lc)
    
    # Calculate bounds
    all_points = np.array([pt for seg in tree.segments for pt in seg])
    x_min, x_max = all_points[:, 0].min(), all_points[:, 0].max()
    y_min, y_max = all_points[:, 1].min(), all_points[:, 1].max()
    
    # Add padding
    padding = 1.0
    ax.set_xlim(x_min - padding, x_max + padding)
    ax.set_ylim(y_min - padding, y_max + padding)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout(pad=0)
    plt.savefig(OUTPUT_FILE, dpi=DPI, bbox_inches='tight', 
                pad_inches=0, facecolor=BACKGROUND)
    print(f"Saved: {OUTPUT_FILE}")
    plt.show()

if __name__ == "__main__":
    print("Creating Recursive Tree art...")
    create_recursive_tree()
    print("Complete!")
