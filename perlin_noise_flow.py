"""
Perlin Noise Flow Field - Algorithmic Art
Creates flowing lines following a Perlin noise field
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# Parameters
GRID_SIZE = 50
NUM_PARTICLES = 300
STEPS_PER_PARTICLE = 200
NOISE_SCALE = 0.1
STEP_SIZE = 0.15
COLORMAP = 'viridis'
BACKGROUND = '#0a0a0a'
LINE_WIDTH = 0.8
ALPHA = 0.5
DPI = 150
OUTPUT_FILE = 'perlin_noise_flow.jpg'

def simple_noise(x, y, seed=42):
    """Simple pseudo-noise function"""
    np.random.seed(int((x * 12.9898 + y * 78.233) * 43758.5453) % 2**31)
    return np.random.rand()

def interpolate(a, b, t):
    """Smooth interpolation"""
    return a + (b - a) * (3 - 2 * t) * t * t

def perlin_noise(x, y, scale=1.0):
    """Simplified Perlin-like noise"""
    x = x * scale
    y = y * scale
    
    # Grid coordinates
    x0 = int(np.floor(x))
    x1 = x0 + 1
    y0 = int(np.floor(y))
    y1 = y0 + 1
    
    # Interpolation weights
    sx = x - x0
    sy = y - y0
    
    # Get corner values
    n00 = simple_noise(x0, y0)
    n10 = simple_noise(x1, y0)
    n01 = simple_noise(x0, y1)
    n11 = simple_noise(x1, y1)
    
    # Interpolate
    nx0 = interpolate(n00, n10, sx)
    nx1 = interpolate(n01, n11, sx)
    return interpolate(nx0, nx1, sy)

def create_flow_field(grid_size, scale):
    """Generate flow field from noise"""
    field = np.zeros((grid_size, grid_size))
    
    for i in range(grid_size):
        for j in range(grid_size):
            angle = perlin_noise(i, j, scale) * 2 * np.pi * 2
            field[i, j] = angle
    
    return field

def create_perlin_noise_flow():
    """Create flow field art"""
    
    print("Generating Perlin noise flow field...")
    
    # Create flow field
    flow_field = create_flow_field(GRID_SIZE, NOISE_SCALE)
    
    print("Simulating particle flows...")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 12), dpi=DPI)
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)
    
    cmap = plt.get_cmap(COLORMAP)
    
    # Generate particles
    for p in range(NUM_PARTICLES):
        # Random starting position
        x = np.random.rand() * GRID_SIZE
        y = np.random.rand() * GRID_SIZE
        
        path = [(x, y)]
        
        # Follow flow field
        for step in range(STEPS_PER_PARTICLE):
            # Get flow angle at current position
            i = int(x) % GRID_SIZE
            j = int(y) % GRID_SIZE
            angle = flow_field[i, j]
            
            # Move particle
            x += np.cos(angle) * STEP_SIZE
            y += np.sin(angle) * STEP_SIZE
            
            # Wrap around boundaries
            x = x % GRID_SIZE
            y = y % GRID_SIZE
            
            path.append((x, y))
        
        # Draw path
        path = np.array(path)
        points = path.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        
        # Color gradient
        colors = np.linspace(0, 1, len(segments))
        
        lc = LineCollection(segments, cmap=COLORMAP,
                           linewidth=LINE_WIDTH, alpha=ALPHA)
        lc.set_array(colors)
        ax.add_collection(lc)
        
        if (p + 1) % 50 == 0:
            print(f"  Drawn {p + 1}/{NUM_PARTICLES} particles")
    
    ax.set_xlim(0, GRID_SIZE)
    ax.set_ylim(0, GRID_SIZE)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout(pad=0)
    plt.savefig(OUTPUT_FILE, dpi=DPI, bbox_inches='tight', 
                pad_inches=0, facecolor=BACKGROUND)
    print(f"Saved: {OUTPUT_FILE}")
    plt.show()

if __name__ == "__main__":
    print("Creating Perlin Noise Flow art...")
    create_perlin_noise_flow()
    print("Complete!")
