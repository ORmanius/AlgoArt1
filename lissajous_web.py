"""
Lissajous Web - Algorithmic Art
Creates intricate web patterns using Lissajous curves
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# Parameters
NUM_CURVES = 12
POINTS_PER_CURVE = 5000
FREQUENCY_RANGE = (1, 8)
PHASE_RANGE = (0, 2 * np.pi)
AMPLITUDE = 8.0
COLORMAP = 'cool'
BACKGROUND = '#000000'
LINE_WIDTH = 0.3
ALPHA = 0.5
DPI = 150
OUTPUT_FILE = 'lissajous_web.jpg'

def create_lissajous_web():
    """Create intricate Lissajous curve patterns"""
    
    print("Generating Lissajous web...")
    
    fig, ax = plt.subplots(figsize=(12, 12), dpi=DPI)
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)
    
    cmap = plt.get_cmap(COLORMAP)
    
    # Generate multiple Lissajous curves
    for i in range(NUM_CURVES):
        # Random frequency ratios
        freq_x = np.random.uniform(*FREQUENCY_RANGE)
        freq_y = np.random.uniform(*FREQUENCY_RANGE)
        
        # Random phase shifts
        phase_x = np.random.uniform(*PHASE_RANGE)
        phase_y = np.random.uniform(*PHASE_RANGE)
        
        # Generate parametric curve
        t = np.linspace(0, 2 * np.pi, POINTS_PER_CURVE)
        x = AMPLITUDE * np.sin(freq_x * t + phase_x)
        y = AMPLITUDE * np.sin(freq_y * t + phase_y)
        
        # Create segments for gradient coloring
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        
        # Color gradient along curve
        colors = np.linspace(0, 1, len(segments))
        
        lc = LineCollection(segments, cmap=cmap, 
                           linewidth=LINE_WIDTH, alpha=ALPHA)
        lc.set_array(colors)
        ax.add_collection(lc)
    
    ax.set_xlim(-AMPLITUDE, AMPLITUDE)
    ax.set_ylim(-AMPLITUDE, AMPLITUDE)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout(pad=0)
    plt.savefig(OUTPUT_FILE, dpi=DPI, bbox_inches='tight', 
                pad_inches=0, facecolor=BACKGROUND)
    print(f"Saved: {OUTPUT_FILE}")
    plt.show()

if __name__ == "__main__":
    print("Creating Lissajous Web art...")
    create_lissajous_web()
    print("Complete!")
