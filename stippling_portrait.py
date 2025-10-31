"""
Stippling Art - Algorithmic Art
Creates stippled/pointillism patterns using weighted random sampling
"""

import numpy as np
import matplotlib.pyplot as plt

# Parameters
NUM_DOTS = 10000
IMAGE_TYPE = 'radial'  # 'radial', 'spiral', 'waves'
DOT_SIZE = 1.0
DOT_SIZE_VARIATION = True
COLORMAP = 'inferno'
COLOR_BY_DENSITY = True
BACKGROUND = '#ffffff'
DPI = 150
OUTPUT_FILE = 'stippling_art.jpg'

def generate_density_field(width, height, pattern_type='radial'):
    """Generate a density field for stippling"""
    
    x = np.linspace(-1, 1, width)
    y = np.linspace(-1, 1, height)
    X, Y = np.meshgrid(x, y)
    
    if pattern_type == 'radial':
        # Radial gradient
        R = np.sqrt(X**2 + Y**2)
        density = 1 - R
        density = np.clip(density, 0, 1)
    
    elif pattern_type == 'spiral':
        # Spiral pattern
        R = np.sqrt(X**2 + Y**2)
        theta = np.arctan2(Y, X)
        density = np.sin(5 * theta + 10 * R) * 0.5 + 0.5
    
    elif pattern_type == 'waves':
        # Wave interference
        density = (np.sin(10 * X) + np.sin(10 * Y)) * 0.5 + 0.5
    
    return density

def create_stippling_art():
    """Create stippled art using density-based sampling"""
    
    print("Generating stippling pattern...")
    
    # Generate density field
    width, height = 500, 500
    density = generate_density_field(width, height, IMAGE_TYPE)
    
    # Normalize to probability
    prob = density.flatten()
    prob = prob / prob.sum()
    
    # Sample points according to density
    flat_indices = np.random.choice(len(prob), NUM_DOTS, replace=True, p=prob)
    y_indices, x_indices = np.unravel_index(flat_indices, density.shape)
    
    # Convert to coordinates
    x_coords = (x_indices / width) * 2 - 1
    y_coords = (y_indices / height) * 2 - 1
    
    # Get density at each point for coloring
    densities = density[y_indices, x_indices]
    
    print("Creating visualization...")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 12), dpi=DPI)
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)
    
    # Determine dot sizes
    if DOT_SIZE_VARIATION:
        sizes = DOT_SIZE * (densities * 2 + 0.5)
    else:
        sizes = DOT_SIZE
    
    # Determine colors
    if COLOR_BY_DENSITY:
        cmap = plt.get_cmap(COLORMAP)
        colors = cmap(densities)
        scatter = ax.scatter(x_coords, y_coords, s=sizes, 
                           c=densities, cmap=COLORMAP, alpha=0.7)
    else:
        scatter = ax.scatter(x_coords, y_coords, s=sizes, 
                           c='black', alpha=0.7)
    
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout(pad=0)
    plt.savefig(OUTPUT_FILE, dpi=DPI, bbox_inches='tight', 
                pad_inches=0, facecolor=BACKGROUND)
    print(f"Saved: {OUTPUT_FILE}")
    plt.show()

if __name__ == "__main__":
    print("Creating Stippling art...")
    create_stippling_art()
    print("Complete!")
