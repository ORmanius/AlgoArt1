"""
Sine Mesh - Algorithmic Art
Creates a 3D-looking mesh deformed by sine waves
"""

import numpy as np
import matplotlib.pyplot as plt

# Parameters
GRID_SIZE = 40
WAVE_AMPLITUDE = 0.3
WAVE_FREQUENCY_X = 2
WAVE_FREQUENCY_Y = 3
TIME_PHASE = 0.5
COLORMAP = 'cool'
BACKGROUND = '#0a0a0a'
LINE_COLOR = '#ffffff'
LINE_WIDTH = 0.5
ALPHA = 0.7
DPI = 150
OUTPUT_FILE = 'sine_mesh.jpg'

def create_sine_mesh():
    """Create 3D sine wave mesh"""
    
    print("Generating sine mesh...")
    
    fig, ax = plt.subplots(figsize=(12, 12), dpi=DPI)
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)
    
    cmap = plt.get_cmap(COLORMAP)
    
    # Create grid
    x = np.linspace(-5, 5, GRID_SIZE)
    y = np.linspace(-5, 5, GRID_SIZE)
    X, Y = np.meshgrid(x, y)
    
    # Calculate Z with sine waves
    Z = (WAVE_AMPLITUDE * 
         (np.sin(WAVE_FREQUENCY_X * X + TIME_PHASE) + 
          np.sin(WAVE_FREQUENCY_Y * Y)))
    
    # Normalize Z for coloring
    Z_norm = (Z - Z.min()) / (Z.max() - Z.min())
    
    # Draw horizontal lines
    for i in range(GRID_SIZE):
        # Apply perspective: scale by Z value
        scale = 1 + Z[i, :] * 0.5
        x_scaled = X[i, :] * scale
        y_scaled = Y[i, :] * scale
        
        # Color based on Z
        colors = cmap(Z_norm[i, :])
        
        for j in range(GRID_SIZE - 1):
            ax.plot([x_scaled[j], x_scaled[j+1]], 
                   [y_scaled[j], y_scaled[j+1]], 
                   color=colors[j], linewidth=LINE_WIDTH, 
                   alpha=ALPHA)
    
    # Draw vertical lines
    for j in range(GRID_SIZE):
        scale = 1 + Z[:, j] * 0.5
        x_scaled = X[:, j] * scale
        y_scaled = Y[:, j] * scale
        
        colors = cmap(Z_norm[:, j])
        
        for i in range(GRID_SIZE - 1):
            ax.plot([x_scaled[i], x_scaled[i+1]], 
                   [y_scaled[i], y_scaled[i+1]], 
                   color=colors[i], linewidth=LINE_WIDTH, 
                   alpha=ALPHA)
    
    max_extent = 5 * 1.5
    ax.set_xlim(-max_extent, max_extent)
    ax.set_ylim(-max_extent, max_extent)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout(pad=0)
    plt.savefig(OUTPUT_FILE, dpi=DPI, bbox_inches='tight', 
                pad_inches=0, facecolor=BACKGROUND)
    print(f"Saved: {OUTPUT_FILE}")
    plt.show()

if __name__ == "__main__":
    print("Creating Sine Mesh art...")
    create_sine_mesh()
    print("Complete!")
