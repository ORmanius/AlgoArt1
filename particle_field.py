"""
Particle Field - Algorithmic Art
Simulates particles moving through a dynamic force field
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# Parameters
NUM_PARTICLES = 200
NUM_STEPS = 150
FIELD_COMPLEXITY = 3
PARTICLE_SPEED = 0.05
COLORMAP = 'plasma'
BACKGROUND = '#0a0a0a'
LINE_WIDTH = 0.8
ALPHA = 0.6
DPI = 150
OUTPUT_FILE = 'particle_field.jpg'

def force_field(x, y, t, complexity=3):
    """Calculate force field at position (x, y) and time t"""
    fx = 0
    fy = 0
    
    # Multiple rotating force centers
    for i in range(complexity):
        angle = (i / complexity) * 2 * np.pi + t * 0.1
        cx = 5 * np.cos(angle)
        cy = 5 * np.sin(angle)
        
        dx = x - cx
        dy = y - cy
        dist = np.sqrt(dx**2 + dy**2) + 0.1
        
        # Vortex-like force
        fx += -dy / dist**2
        fy += dx / dist**2
    
    return fx, fy

def create_particle_field():
    """Create particle field visualization"""
    
    print("Simulating particle field...")
    
    # Initialize particles randomly
    particles_x = np.random.uniform(-10, 10, NUM_PARTICLES)
    particles_y = np.random.uniform(-10, 10, NUM_PARTICLES)
    
    # Store trajectories
    trajectories = [[(particles_x[i], particles_y[i])] for i in range(NUM_PARTICLES)]
    
    # Simulate particle movement
    for step in range(NUM_STEPS):
        for i in range(NUM_PARTICLES):
            # Get force at current position
            fx, fy = force_field(particles_x[i], particles_y[i], step, FIELD_COMPLEXITY)
            
            # Update position
            particles_x[i] += fx * PARTICLE_SPEED
            particles_y[i] += fy * PARTICLE_SPEED
            
            # Wrap around boundaries
            particles_x[i] = np.clip(particles_x[i], -10, 10)
            particles_y[i] = np.clip(particles_y[i], -10, 10)
            
            # Store position
            trajectories[i].append((particles_x[i], particles_y[i]))
    
    print("Creating visualization...")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 12), dpi=DPI)
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)
    
    # Get colormap
    cmap = plt.get_cmap(COLORMAP)
    
    # Plot trajectories
    for i, trajectory in enumerate(trajectories):
        points = np.array(trajectory)
        
        # Create line segments
        segments = []
        for j in range(len(points) - 1):
            segments.append([points[j], points[j + 1]])
        
        # Color gradient along trajectory
        colors = np.linspace(0, 1, len(segments))
        
        # Create line collection
        lc = LineCollection(segments, colors=cmap(colors), 
                           linewidths=LINE_WIDTH, alpha=ALPHA)
        ax.add_collection(lc)
    
    # Styling
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout(pad=0)
    plt.savefig(OUTPUT_FILE, dpi=DPI, bbox_inches='tight', 
                pad_inches=0, facecolor=BACKGROUND)
    print(f"Saved: {OUTPUT_FILE}")
    plt.show()

if __name__ == "__main__":
    print("Creating Particle Field art...")
    create_particle_field()
    print("Complete!")
