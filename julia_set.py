"""
Julia Set - Algorithmic Art
Creates beautiful Julia set fractals with various parameters
"""

import numpy as np
import matplotlib.pyplot as plt

# Parameters
WIDTH = 1200
HEIGHT = 1200
X_MIN, X_MAX = -2.0, 2.0
Y_MIN, Y_MAX = -2.0, 2.0
MAX_ITER = 256

# Julia set parameter (try different values!)
# Beautiful ones: (-0.4, 0.6), (-0.7, 0.27), (0.285, 0.01), (-0.8, 0.156)
C_REAL = -0.4
C_IMAG = 0.6

COLORMAP = 'twilight'
BACKGROUND = '#000000'
DPI = 150
OUTPUT_FILE = 'julia_set.jpg'

def calculate_julia_set(width, height, x_min, x_max, y_min, y_max, 
                       c_real, c_imag, max_iter):
    """Calculate Julia set"""
    
    print(f"Calculating Julia set with c = {c_real} + {c_imag}i...")
    
    # Create coordinate arrays
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    X, Y = np.meshgrid(x, y)
    
    # Complex plane
    Z = X + 1j * Y
    C = c_real + 1j * c_imag
    
    # Initialize arrays
    M = np.zeros(Z.shape)
    
    # Julia set iteration
    for i in range(max_iter):
        # Points that haven't escaped
        mask = np.abs(Z) <= 2
        
        # Update Z for points that haven't escaped
        Z[mask] = Z[mask]**2 + C
        
        # Record iteration count at escape
        M[mask] = i
    
    # Smooth coloring using escape time
    M = M + 1 - np.log(np.log(np.abs(Z) + 1)) / np.log(2)
    M = np.nan_to_num(M)
    
    return M

def create_julia_set():
    """Create Julia set visualization"""
    
    # Calculate Julia set
    M = calculate_julia_set(WIDTH, HEIGHT, X_MIN, X_MAX, Y_MIN, Y_MAX,
                           C_REAL, C_IMAG, MAX_ITER)
    
    print("Creating visualization...")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 12), dpi=DPI)
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)
    
    # Display with logarithmic scaling for better colors
    im = ax.imshow(np.log(M + 1), cmap=COLORMAP, 
                   extent=[X_MIN, X_MAX, Y_MIN, Y_MAX],
                   interpolation='bilinear', origin='lower')
    
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout(pad=0)
    plt.savefig(OUTPUT_FILE, dpi=DPI, bbox_inches='tight', 
                pad_inches=0, facecolor=BACKGROUND)
    print(f"Saved: {OUTPUT_FILE}")
    plt.show()

if __name__ == "__main__":
    print("Creating Julia Set art...")
    create_julia_set()
    print("Complete!")
    print("\nTry different C values:")
    print("  (-0.4, 0.6) - classic spiral")
    print("  (-0.7, 0.27) - dendrite")
    print("  (0.285, 0.01) - double spiral")
    print("  (-0.8, 0.156) - douady's rabbit")
