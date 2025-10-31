"""
Reaction-Diffusion - Algorithmic Art
Creates organic patterns using Gray-Scott reaction-diffusion model
"""

import numpy as np
import matplotlib.pyplot as plt

# Parameters
WIDTH = 400
HEIGHT = 400
STEPS = 10000
FEED_RATE = 0.055
KILL_RATE = 0.062
DIFFUSION_A = 1.0
DIFFUSION_B = 0.5
DELTA_T = 1.0
COLORMAP = 'hot'
BACKGROUND = '#000000'
DPI = 150
OUTPUT_FILE = 'reaction_diffusion.jpg'

def laplacian(grid):
    """Calculate Laplacian using convolution"""
    return (
        np.roll(grid, 1, axis=0) + 
        np.roll(grid, -1, axis=0) + 
        np.roll(grid, 1, axis=1) + 
        np.roll(grid, -1, axis=1) - 
        4 * grid
    )

def create_reaction_diffusion():
    """Create reaction-diffusion pattern"""
    
    print("Simulating reaction-diffusion system...")
    
    # Initialize grids
    A = np.ones((HEIGHT, WIDTH))
    B = np.zeros((HEIGHT, WIDTH))
    
    # Add initial perturbation (multiple spots)
    for _ in range(15):
        x, y = np.random.randint(50, WIDTH-50), np.random.randint(50, HEIGHT-50)
        size = np.random.randint(5, 15)
        B[y-size:y+size, x-size:x+size] = 1.0
    
    # Simulate
    for step in range(STEPS):
        # Calculate Laplacians
        LA = laplacian(A)
        LB = laplacian(B)
        
        # Reaction-diffusion equations
        A_new = A + (DIFFUSION_A * LA - A * B * B + FEED_RATE * (1 - A)) * DELTA_T
        B_new = B + (DIFFUSION_B * LB + A * B * B - (KILL_RATE + FEED_RATE) * B) * DELTA_T
        
        A, B = A_new, B_new
        
        if step % 1000 == 0:
            print(f"  Step {step}/{STEPS}")
    
    print("Creating visualization...")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 10), dpi=DPI)
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)
    
    # Display B concentration
    im = ax.imshow(B, cmap=COLORMAP, interpolation='bilinear')
    ax.axis('off')
    
    plt.tight_layout(pad=0)
    plt.savefig(OUTPUT_FILE, dpi=DPI, bbox_inches='tight', pad_inches=0)
    print(f"Saved: {OUTPUT_FILE}")
    plt.show()

if __name__ == "__main__":
    print("Creating Reaction-Diffusion art...")
    create_reaction_diffusion()
    print("Complete!")
