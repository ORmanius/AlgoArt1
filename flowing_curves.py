"""
Flowing Curves - Algorithmic Art
Creates organic flowing curves using Perlin-like noise and Bezier paths
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
import matplotlib.colors as mcolors

# Parameters
NUM_CURVES = 80
POINTS_PER_CURVE = 100
NOISE_SCALE = 0.5
AMPLITUDE = 3.0
COLORMAP = 'viridis'
BACKGROUND = '#000000'
LINE_WIDTH = 1.5
ALPHA = 0.4
DPI = 150
OUTPUT_FILE = 'flowing_curves.jpg'

def generate_smooth_noise(length, scale=1.0):
    """Generate smooth random variations"""
    x = np.linspace(0, scale * 4 * np.pi, length)
    noise = np.zeros(length)
    
    # Multiple frequency components
    for freq in [1, 2, 4]:
        phase = np.random.rand() * 2 * np.pi
        noise += np.sin(freq * x + phase) / freq
    
    return noise

def create_flowing_curves():
    """Create organic flowing curve patterns"""
    
    fig, ax = plt.subplots(figsize=(14, 10), dpi=DPI)
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)
    
    # Get colormap
    cmap = plt.get_cmap(COLORMAP)
    
    # Generate curves
    for i in range(NUM_CURVES):
        # Base y position
        y_base = i * 0.15 - NUM_CURVES * 0.075
        
        # X coordinates
        x = np.linspace(-8, 8, POINTS_PER_CURVE)
        
        # Generate smooth noise for y variation
        noise = generate_smooth_noise(POINTS_PER_CURVE, NOISE_SCALE)
        
        # Add wave patterns
        wave = AMPLITUDE * np.sin(x * 0.5 + i * 0.3)
        
        # Combine for y coordinates
        y = y_base + noise * 0.3 + wave * 0.2
        
        # Color based on position
        color = cmap(i / NUM_CURVES)
        
        # Plot curve
        ax.plot(x, y, color=color, linewidth=LINE_WIDTH, 
               alpha=ALPHA, solid_capstyle='round')
    
    # Styling
    ax.set_xlim(-8, 8)
    ax.set_ylim(-NUM_CURVES * 0.075 - 2, NUM_CURVES * 0.075 + 2)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout(pad=0)
    plt.savefig(OUTPUT_FILE, dpi=DPI, bbox_inches='tight', 
                pad_inches=0, facecolor=BACKGROUND)
    print(f"Saved: {OUTPUT_FILE}")
    plt.show()

if __name__ == "__main__":
    print("Creating Flowing Curves art...")
    create_flowing_curves()
    print("Complete!")
