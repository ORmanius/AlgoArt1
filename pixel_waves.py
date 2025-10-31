"""
Pixel Waves - Algorithmic Art
Creates wave interference patterns using pixel manipulation
"""

import numpy as np
import matplotlib.pyplot as plt

# Parameters
WIDTH = 800
HEIGHT = 800
NUM_WAVE_SOURCES = 5
WAVE_FREQUENCY = 0.05
AMPLITUDE = 1.0
COLORMAP = 'twilight'
DPI = 150
OUTPUT_FILE = 'pixel_waves.jpg'

def create_pixel_waves():
    """Create wave interference pattern"""
    
    print("Calculating wave interference...")
    
    # Create coordinate grid
    x = np.linspace(-10, 10, WIDTH)
    y = np.linspace(-10, 10, HEIGHT)
    X, Y = np.meshgrid(x, y)
    
    # Initialize wave field
    wave_field = np.zeros((HEIGHT, WIDTH))
    
    # Generate random wave sources
    sources = []
    for i in range(NUM_WAVE_SOURCES):
        sx = np.random.uniform(-5, 5)
        sy = np.random.uniform(-5, 5)
        freq = WAVE_FREQUENCY * np.random.uniform(0.5, 2.0)
        phase = np.random.uniform(0, 2 * np.pi)
        sources.append((sx, sy, freq, phase))
    
    # Calculate interference pattern
    for sx, sy, freq, phase in sources:
        # Distance from source
        distance = np.sqrt((X - sx)**2 + (Y - sy)**2)
        
        # Wave contribution
        wave = AMPLITUDE * np.sin(2 * np.pi * freq * distance + phase)
        
        # Add to field
        wave_field += wave
    
    # Normalize
    wave_field = (wave_field - wave_field.min()) / (wave_field.max() - wave_field.min())
    
    print("Creating visualization...")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 10), dpi=DPI)
    
    # Display wave field
    im = ax.imshow(wave_field, cmap=COLORMAP, interpolation='bilinear',
                   extent=[-10, 10, -10, 10], origin='lower')
    
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout(pad=0)
    plt.savefig(OUTPUT_FILE, dpi=DPI, bbox_inches='tight', pad_inches=0)
    print(f"Saved: {OUTPUT_FILE}")
    plt.show()

if __name__ == "__main__":
    print("Creating Pixel Waves art...")
    create_pixel_waves()
    print("Complete!")
