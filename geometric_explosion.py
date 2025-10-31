"""
Geometric Explosion - Algorithmic Art
Creates an explosive pattern of geometric shapes radiating from center
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
import matplotlib.colors as mcolors

# Parameters
NUM_SHAPES = 200
SHAPE_TYPES = ['triangle', 'square', 'pentagon', 'hexagon']
EXPLOSION_RADIUS = 10
ROTATION_CHAOS = True
COLORMAP = 'rainbow'
BACKGROUND = '#000000'
ALPHA = 0.5
EDGE_COLOR = '#ffffff'
EDGE_WIDTH = 0.5
EDGE_ALPHA = 0.2
DPI = 150
OUTPUT_FILE = 'geometric_explosion.jpg'

def create_polygon(n_sides, center, radius, rotation=0):
    """Create regular polygon vertices"""
    angles = np.linspace(0, 2 * np.pi, n_sides, endpoint=False) + rotation
    x = center[0] + radius * np.cos(angles)
    y = center[1] + radius * np.sin(angles)
    return np.column_stack([x, y])

def create_geometric_explosion():
    """Create explosive geometric pattern"""
    
    print("Creating geometric explosion...")
    
    fig, ax = plt.subplots(figsize=(14, 14), dpi=DPI)
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)
    
    cmap = plt.get_cmap(COLORMAP)
    
    # Generate shapes radiating outward
    for i in range(NUM_SHAPES):
        # Random angle and distance from center
        angle = np.random.rand() * 2 * np.pi
        distance = np.random.rand() ** 0.5 * EXPLOSION_RADIUS
        
        # Position
        x = distance * np.cos(angle)
        y = distance * np.sin(angle)
        
        # Shape size decreases with distance
        size = 0.8 * (1 - distance / EXPLOSION_RADIUS) + 0.2
        
        # Random shape type
        shape_type = np.random.choice(SHAPE_TYPES)
        
        # Rotation
        if ROTATION_CHAOS:
            rotation = np.random.rand() * 2 * np.pi
        else:
            rotation = angle  # Align with explosion direction
        
        # Color based on distance and angle
        color_val = (distance / EXPLOSION_RADIUS + angle / (2 * np.pi)) / 2
        color = cmap(color_val)
        
        # Create shape
        if shape_type == 'triangle':
            vertices = create_polygon(3, (x, y), size, rotation)
        elif shape_type == 'square':
            vertices = create_polygon(4, (x, y), size, rotation)
        elif shape_type == 'pentagon':
            vertices = create_polygon(5, (x, y), size, rotation)
        elif shape_type == 'hexagon':
            vertices = create_polygon(6, (x, y), size, rotation)
        
        # Add polygon
        poly = Polygon(vertices, facecolor=color, 
                      edgecolor=EDGE_COLOR, linewidth=EDGE_WIDTH,
                      alpha=ALPHA)
        ax.add_patch(poly)
    
    # Add central burst circle
    central_circle = Circle((0, 0), 0.5, 
                           facecolor='#ffffff', alpha=0.8)
    ax.add_patch(central_circle)
    
    ax.set_xlim(-EXPLOSION_RADIUS, EXPLOSION_RADIUS)
    ax.set_ylim(-EXPLOSION_RADIUS, EXPLOSION_RADIUS)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout(pad=0)
    plt.savefig(OUTPUT_FILE, dpi=DPI, bbox_inches='tight', 
                pad_inches=0, facecolor=BACKGROUND)
    print(f"Saved: {OUTPUT_FILE}")
    plt.show()

if __name__ == "__main__":
    print("Creating Geometric Explosion art...")
    create_geometric_explosion()
    print("Complete!")
