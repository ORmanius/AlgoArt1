"""
Dragon Curve - Algorithmic Art
Creates the famous Heighway Dragon fractal curve
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# Parameters
ITERATIONS = 15  # Higher values = more detail (try 10-16)
COLORMAP = 'rainbow'
BACKGROUND = '#0a0a0a'
LINE_WIDTH = 0.5
ALPHA = 0.8
COLOR_BY = 'order'  # 'order' or 'position'
DPI = 150
OUTPUT_FILE = 'dragon_curve.jpg'

def generate_dragon_curve(iterations):
    """Generate dragon curve using L-system"""
    
    print(f"Generating dragon curve (iteration {iterations})...")
    
    # Start with simple sequence
    sequence = 'FX'
    
    # L-system rules:
    # X -> X+YF+
    # Y -> -FX-Y
    for i in range(iterations):
        new_sequence = ''
        for char in sequence:
            if char == 'X':
                new_sequence += 'X+YF+'
            elif char == 'Y':
                new_sequence += '-FX-Y'
            else:
                new_sequence += char
        sequence = new_sequence
        print(f"  Iteration {i+1}/{iterations} - Length: {len(sequence)}")
    
    return sequence

def draw_dragon_curve(sequence):
    """Convert L-system to coordinates"""
    
    print("Converting to coordinates...")
    
    x, y = 0, 0
    angle = 0
    step = 1
    
    points = [(x, y)]
    
    for i, char in enumerate(sequence):
        if char == 'F':
            # Move forward
            x += step * np.cos(np.radians(angle))
            y += step * np.sin(np.radians(angle))
            points.append((x, y))
        elif char == '+':
            # Turn right 90 degrees
            angle -= 90
        elif char == '-':
            # Turn left 90 degrees
            angle += 90
        
        if (i + 1) % 10000 == 0:
            print(f"  Processed {i+1}/{len(sequence)} commands")
    
    return np.array(points)

def create_dragon_curve():
    """Create dragon curve visualization"""
    
    # Generate sequence
    sequence = generate_dragon_curve(ITERATIONS)
    
    # Draw curve
    points = draw_dragon_curve(sequence)
    
    print("Creating visualization...")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 12), dpi=DPI)
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)
    
    # Create segments
    segments = []
    for i in range(len(points) - 1):
        segments.append([points[i], points[i + 1]])
    
    segments = np.array(segments)
    
    # Color gradient
    if COLOR_BY == 'order':
        colors = np.linspace(0, 1, len(segments))
    else:  # position
        # Color by spatial position
        colors = np.sqrt(segments[:, 0, 0]**2 + segments[:, 0, 1]**2)
        colors = (colors - colors.min()) / (colors.max() - colors.min())
    
    # Create line collection
    lc = LineCollection(segments, cmap=COLORMAP,
                       linewidth=LINE_WIDTH, alpha=ALPHA)
    lc.set_array(colors)
    ax.add_collection(lc)
    
    # Set limits
    x_min, x_max = points[:, 0].min(), points[:, 0].max()
    y_min, y_max = points[:, 1].min(), points[:, 1].max()
    
    margin = 0.05 * max(x_max - x_min, y_max - y_min)
    ax.set_xlim(x_min - margin, x_max + margin)
    ax.set_ylim(y_min - margin, y_max + margin)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout(pad=0)
    plt.savefig(OUTPUT_FILE, dpi=DPI, bbox_inches='tight', 
                pad_inches=0, facecolor=BACKGROUND)
    print(f"Saved: {OUTPUT_FILE}")
    plt.show()

if __name__ == "__main__":
    print("Creating Dragon Curve art...")
    create_dragon_curve()
    print("Complete!")
