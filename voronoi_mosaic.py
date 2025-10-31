"""
Voronoi Mosaic - Algorithmic Art
Creates a beautiful Voronoi diagram with gradient coloring
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
from matplotlib.collections import PolyCollection

# Parameters
NUM_POINTS = 150
GRID_SIZE = 10
COLORMAP = 'twilight'
BACKGROUND = '#0a0a0a'
EDGE_COLOR = '#ffffff'
EDGE_WIDTH = 0.5
EDGE_ALPHA = 0.3
DPI = 150
OUTPUT_FILE = 'voronoi_mosaic.jpg'

def create_voronoi_mosaic():
    """Create Voronoi diagram with gradient coloring"""
    
    print("Generating Voronoi diagram...")
    
    # Generate random points
    points = np.random.uniform(-GRID_SIZE, GRID_SIZE, (NUM_POINTS, 2))
    
    # Create Voronoi diagram
    vor = Voronoi(points)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 12), dpi=DPI)
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)
    
    # Get colormap
    cmap = plt.get_cmap(COLORMAP)
    
    # Plot each Voronoi region
    for i, region_index in enumerate(vor.point_region):
        region = vor.regions[region_index]
        
        if not -1 in region and len(region) > 0:
            polygon = [vor.vertices[i] for i in region]
            
            # Calculate distance from center for color
            center_dist = np.linalg.norm(points[i])
            max_dist = GRID_SIZE * np.sqrt(2)
            color_val = center_dist / max_dist
            
            # Color based on distance from center
            color = cmap(color_val)
            
            # Plot filled polygon
            poly = plt.Polygon(polygon, facecolor=color, 
                             edgecolor=EDGE_COLOR, 
                             linewidth=EDGE_WIDTH,
                             alpha=0.8)
            ax.add_patch(poly)
    
    # Add edge lines with transparency
    for simplex in vor.ridge_vertices:
        if -1 not in simplex:
            line = [vor.vertices[i] for i in simplex]
            ax.plot([line[0][0], line[1][0]], 
                   [line[0][1], line[1][1]], 
                   color=EDGE_COLOR, 
                   linewidth=EDGE_WIDTH,
                   alpha=EDGE_ALPHA)
    
    # Styling
    ax.set_xlim(-GRID_SIZE, GRID_SIZE)
    ax.set_ylim(-GRID_SIZE, GRID_SIZE)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout(pad=0)
    plt.savefig(OUTPUT_FILE, dpi=DPI, bbox_inches='tight', 
                pad_inches=0, facecolor=BACKGROUND)
    print(f"Saved: {OUTPUT_FILE}")
    plt.show()

if __name__ == "__main__":
    print("Creating Voronoi Mosaic art...")
    create_voronoi_mosaic()
    print("Complete!")
