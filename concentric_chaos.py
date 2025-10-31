"""
Concentric Chaos - Algorithmic Art
Creates chaotic concentric circles with noise-based deformations
"""

import numpy as np
import matplotlib.pyplot as plt

# Parameters
NUM_CIRCLES = 100
POINTS_PER_CIRCLE = 500
NOISE_AMPLITUDE = 0.3
NOISE_FREQUENCY = 8
COLORMAP = 'magma'
BACKGROUND = '#0a0a0a'
LINE_WIDTH = 0.8
ALPHA = 0.6
DPI = 150
OUTPUT_FILE = 'concentric_chaos.jpg'

def create_concentric_chaos():
    """Create chaotic concentric circle patterns"""
    
    print("Generating concentric chaos...")
    
    fig, ax = plt.subplots(figsize=(12, 12), dpi=DPI)
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)
    
    cmap = plt.get_cmap(COLORMAP)
    
    # Generate deformed circles
    for i in range(NUM_CIRCLES):
        radius = 0.1 + i * 0.09
        
        # Parametric angle
        theta = np.linspace(0, 2 * np.pi, POINTS_PER_CIRCLE)
        
        # Add multiple noise frequencies
        noise = 0
        for freq in range(1, NOISE_FREQUENCY):
            phase = np.random.rand() * 2 * np.pi
            amplitude = NOISE_AMPLITUDE / freq
            noise += amplitude * np.sin(freq * theta + phase)
        
        # Apply noise to radius
        r = radius * (1 + noise)
        
        # Convert to Cartesian
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        # Color based on circle index
        color = cmap(i / NUM_CIRCLES)
        
        # Plot
        ax.plot(x, y, color=color, linewidth=LINE_WIDTH, alpha=ALPHA)
    
    max_radius = 0.1 + NUM_CIRCLES * 0.09 + NOISE_AMPLITUDE
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
    print("Creating Concentric Chaos art...")
    create_concentric_chaos()
    print("Complete!")
