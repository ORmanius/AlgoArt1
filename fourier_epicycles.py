"""
Fourier Epicycles - Algorithmic Art
Visualizes Fourier series as rotating circles (epicycles)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# Parameters
SHAPE_TYPE = 'heart'  # 'heart', 'star', 'spiral', 'square'
NUM_EPICYCLES = 50
DRAWING_STEPS = 500
COLORMAP = 'twilight'
BACKGROUND = '#0a0a0a'
LINE_WIDTH = 1.5
CIRCLE_WIDTH = 0.3
SHOW_CIRCLES = True
ALPHA = 0.7
DPI = 150
OUTPUT_FILE = 'fourier_epicycles.jpg'

def get_shape_points(shape_type, num_points=200):
    """Generate points for different shapes"""
    t = np.linspace(0, 2 * np.pi, num_points)
    
    if shape_type == 'heart':
        x = 16 * np.sin(t)**3
        y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
    elif shape_type == 'star':
        r = 5 * (2 + np.sin(5 * t))
        x = r * np.cos(t)
        y = r * np.sin(t)
    elif shape_type == 'spiral':
        r = t
        x = r * np.cos(t)
        y = r * np.sin(t)
    elif shape_type == 'square':
        # Approximation of square
        x = 10 * np.sign(np.cos(t))
        y = 10 * np.sign(np.sin(t))
    
    return x + 1j * y

def compute_fourier_series(points, n_terms):
    """Compute Fourier coefficients"""
    N = len(points)
    coeffs = []
    
    for k in range(-n_terms//2, n_terms//2 + 1):
        c = np.sum(points * np.exp(-2j * np.pi * k * np.arange(N) / N)) / N
        coeffs.append((k, c))
    
    # Sort by magnitude
    coeffs.sort(key=lambda x: abs(x[1]), reverse=True)
    return coeffs[:n_terms]

def create_fourier_epicycles():
    """Create Fourier epicycles visualization"""
    
    print("Computing Fourier series...")
    
    # Get shape points
    shape_points = get_shape_points(SHAPE_TYPE)
    
    # Compute Fourier coefficients
    coeffs = compute_fourier_series(shape_points, NUM_EPICYCLES)
    
    print("Drawing epicycles...")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 12), dpi=DPI)
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)
    
    cmap = plt.get_cmap(COLORMAP)
    
    # Draw path traced by epicycles
    path = []
    
    for step in range(DRAWING_STEPS):
        t = 2 * np.pi * step / DRAWING_STEPS
        
        # Calculate position from epicycles
        pos = 0 + 0j
        for k, c in coeffs:
            pos += c * np.exp(2j * np.pi * k * t)
        
        path.append(pos)
    
    # Draw the traced path
    path = np.array(path)
    x_path = path.real
    y_path = path.imag
    
    # Create segments for gradient
    points = np.array([x_path, y_path]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    colors = np.linspace(0, 1, len(segments))
    
    lc = LineCollection(segments, cmap=COLORMAP, 
                       linewidth=LINE_WIDTH, alpha=ALPHA)
    lc.set_array(colors)
    ax.add_collection(lc)
    
    # Optionally draw epicycles at final position
    if SHOW_CIRCLES:
        t = 0  # Start position
        pos = 0 + 0j
        
        for i, (k, c) in enumerate(coeffs):
            prev_pos = pos
            radius = abs(c)
            angle = np.angle(c) + 2 * np.pi * k * t
            pos += c * np.exp(2j * np.pi * k * t)
            
            # Draw circle
            circle = plt.Circle((prev_pos.real, prev_pos.imag), radius,
                              fill=False, edgecolor=cmap(i/len(coeffs)),
                              linewidth=CIRCLE_WIDTH, alpha=0.3)
            ax.add_patch(circle)
            
            # Draw radius line
            ax.plot([prev_pos.real, pos.real], 
                   [prev_pos.imag, pos.imag],
                   color=cmap(i/len(coeffs)), linewidth=CIRCLE_WIDTH,
                   alpha=0.5)
    
    # Set limits
    margin = 1.2
    x_range = max(abs(x_path.max()), abs(x_path.min())) * margin
    y_range = max(abs(y_path.max()), abs(y_path.min())) * margin
    max_range = max(x_range, y_range)
    
    ax.set_xlim(-max_range, max_range)
    ax.set_ylim(-max_range, max_range)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout(pad=0)
    plt.savefig(OUTPUT_FILE, dpi=DPI, bbox_inches='tight', 
                pad_inches=0, facecolor=BACKGROUND)
    print(f"Saved: {OUTPUT_FILE}")
    plt.show()

if __name__ == "__main__":
    print("Creating Fourier Epicycles art...")
    create_fourier_epicycles()
    print("Complete!")
