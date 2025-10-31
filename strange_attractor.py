"""
Strange Attractor - Algorithmic Art
Visualizes chaotic attractors (Lorenz, Rossler, etc.)
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import LineCollection

# Parameters
ATTRACTOR_TYPE = 'lorenz'  # 'lorenz', 'rossler', 'aizawa'
NUM_STEPS = 50000
DT = 0.01
COLORMAP = 'plasma'
BACKGROUND = '#000000'
LINE_WIDTH = 0.3
ALPHA = 0.6
VIEW_3D = False  # Set True for 3D view
DPI = 150
OUTPUT_FILE = 'strange_attractor.jpg'

def lorenz(x, y, z, sigma=10, rho=28, beta=8/3):
    """Lorenz attractor equations"""
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return dx, dy, dz

def rossler(x, y, z, a=0.2, b=0.2, c=5.7):
    """Rossler attractor equations"""
    dx = -y - z
    dy = x + a * y
    dz = b + z * (x - c)
    return dx, dy, dz

def aizawa(x, y, z, a=0.95, b=0.7, c=0.6, d=3.5, e=0.25, f=0.1):
    """Aizawa attractor equations"""
    dx = (z - b) * x - d * y
    dy = d * x + (z - b) * y
    dz = c + a * z - (z**3 / 3) - (x**2 + y**2) * (1 + e * z) + f * z * x**3
    return dx, dy, dz

def create_strange_attractor():
    """Generate and visualize strange attractor"""
    
    print(f"Simulating {ATTRACTOR_TYPE} attractor...")
    
    # Initial conditions
    x, y, z = 0.1, 0.0, 0.0
    
    # Store trajectory
    xs, ys, zs = [x], [y], [z]
    
    # Select attractor
    if ATTRACTOR_TYPE == 'lorenz':
        attractor_func = lorenz
    elif ATTRACTOR_TYPE == 'rossler':
        attractor_func = rossler
    elif ATTRACTOR_TYPE == 'aizawa':
        attractor_func = aizawa
    
    # Simulate
    for _ in range(NUM_STEPS):
        dx, dy, dz = attractor_func(x, y, z)
        x += dx * DT
        y += dy * DT
        z += dz * DT
        xs.append(x)
        ys.append(y)
        zs.append(z)
    
    print("Creating visualization...")
    
    # Create figure
    if VIEW_3D:
        fig = plt.figure(figsize=(12, 12), dpi=DPI)
        fig.patch.set_facecolor(BACKGROUND)
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor(BACKGROUND)
        
        # Plot 3D
        points = np.array([xs, ys, zs]).T.reshape(-1, 1, 3)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        
        colors = np.linspace(0, 1, len(segments))
        
        # Note: 3D LineCollection is tricky, using plot instead
        cmap = plt.get_cmap(COLORMAP)
        for i in range(0, len(xs)-1, 50):
            color = cmap(i / len(xs))
            ax.plot(xs[i:i+50], ys[i:i+50], zs[i:i+50], 
                   color=color, linewidth=LINE_WIDTH, alpha=ALPHA)
        
        ax.axis('off')
        ax.grid(False)
    else:
        # 2D projection
        fig, ax = plt.subplots(figsize=(12, 12), dpi=DPI)
        fig.patch.set_facecolor(BACKGROUND)
        ax.set_facecolor(BACKGROUND)
        
        # Create line segments for gradient
        points = np.array([xs, ys]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        
        colors = np.linspace(0, 1, len(segments))
        
        lc = LineCollection(segments, cmap=COLORMAP, 
                           linewidth=LINE_WIDTH, alpha=ALPHA)
        lc.set_array(colors)
        ax.add_collection(lc)
        
        ax.set_xlim(min(xs), max(xs))
        ax.set_ylim(min(ys), max(ys))
        ax.set_aspect('equal')
        ax.axis('off')
    
    plt.tight_layout(pad=0)
    plt.savefig(OUTPUT_FILE, dpi=DPI, bbox_inches='tight', 
                pad_inches=0, facecolor=BACKGROUND)
    print(f"Saved: {OUTPUT_FILE}")
    plt.show()

if __name__ == "__main__":
    print("Creating Strange Attractor art...")
    create_strange_attractor()
    print("Complete!")
