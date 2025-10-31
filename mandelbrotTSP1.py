"""
Mandelbrot Fractal TSP Line Drawing Generator
Creates a single-stroke path through Mandelbrot set points with gradient coloring
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from scipy.spatial.distance import cdist
import time

# ============================================================================
# PARAMETERS - Adjust these to change the output
# ============================================================================

# Mandelbrot Parameters - ZOOMED INTO LEFT SPIRAL
MANDELBROT_WIDTH = 1000          # Image width in pixels
MANDELBROT_HEIGHT = 800          # Image height in pixels
X_MIN, X_MAX = -0.8, -0.4        # Zoomed into left spiral detail
Y_MIN, Y_MAX = -0.2, 0.2         # Imaginary axis range
MAX_ITER = 512                   # Maximum iterations for Mandelbrot calculation

# Point Selection Parameters
NUM_POINTS = 3000                # Number of points to extract for TSP
BOUNDARY_THRESHOLD = 5.0         # Threshold for boundary detection
SAMPLE_METHOD = 'boundary'       # 'boundary', 'gradient', or 'random'

# TSP Parameters
TSP_METHOD = '2opt'              # 'nearest_neighbor' or '2opt'
TWO_OPT_ITERATIONS = 50          # Number of 2-opt improvements (if using 2opt)

# Visual Parameters
LINE_WIDTH = 0.7                 # Width of the drawn line
COLORMAP = 'plasma'              # Matplotlib colormap: 'twilight', 'viridis', 'plasma', 'inferno', 'magma'
COLOR_BY = 'iteration'           # 'position' (path order) or 'iteration' (Mandelbrot iterations)
BACKGROUND_COLOR = '#0a0a0a'     # Background color
DPI = 150                        # Output resolution

# Output Parameters
OUTPUT_FILENAME = 'mandelbrot_tsp_zoomed.jpg'
SHOW_PLOT = True                 # Display plot before saving

# ============================================================================
# MANDELBROT SET CALCULATION
# ============================================================================

def calculate_mandelbrot(width, height, x_min, x_max, y_min, y_max, max_iter):
    """
    Calculate the Mandelbrot set and return iteration counts for each point.
    """
    print("Calculating Mandelbrot set...")
    
    # Create coordinate arrays
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    X, Y = np.meshgrid(x, y)
    
    # Complex plane
    C = X + 1j * Y
    
    # Initialize arrays
    Z = np.zeros_like(C)
    M = np.zeros(C.shape)
    
    # Mandelbrot iteration
    for i in range(max_iter):
        # Points that haven't escaped
        mask = np.abs(Z) <= 2
        
        # Update Z for points that haven't escaped
        Z[mask] = Z[mask]**2 + C[mask]
        
        # Record iteration count at escape
        M[mask] = i
    
    print(f"Mandelbrot calculation complete. Points in set: {np.sum(M == max_iter - 1)}")
    return M, X, Y

# ============================================================================
# POINT EXTRACTION
# ============================================================================

def extract_points(M, X, Y, num_points, method='boundary', threshold=2.0):
    """
    Extract interesting points from the Mandelbrot set for TSP.
    """
    print(f"Extracting {num_points} points using '{method}' method...")
    
    if method == 'boundary':
        # Find boundary points (points near the edge of the set)
        # Calculate gradient magnitude
        grad_y, grad_x = np.gradient(M)
        gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        
        # Get points with high gradient (boundary)
        boundary_mask = gradient_magnitude > threshold
        boundary_indices = np.where(boundary_mask)
        
        if len(boundary_indices[0]) == 0:
            print("No boundary points found, falling back to gradient method")
            method = 'gradient'
        else:
            # Sample points
            total_boundary = len(boundary_indices[0])
            if total_boundary > num_points:
                sample_indices = np.random.choice(total_boundary, num_points, replace=False)
            else:
                sample_indices = np.arange(total_boundary)
                print(f"Warning: Only {total_boundary} boundary points found")
            
            points_y = boundary_indices[0][sample_indices]
            points_x = boundary_indices[1][sample_indices]
    
    if method == 'gradient':
        # Sample based on gradient probability
        grad_y, grad_x = np.gradient(M)
        gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        
        # Normalize to probability
        prob = gradient_magnitude.flatten()
        prob = prob / prob.sum()
        
        # Sample indices
        flat_indices = np.random.choice(len(prob), num_points, replace=False, p=prob)
        points_y, points_x = np.unravel_index(flat_indices, M.shape)
    
    elif method == 'random':
        # Random sampling from all points
        points_y = np.random.randint(0, M.shape[0], num_points)
        points_x = np.random.randint(0, M.shape[1], num_points)
    
    # Get actual coordinates
    points = np.column_stack([X[points_y, points_x], Y[points_y, points_x]])
    iterations = M[points_y, points_x]
    
    print(f"Extracted {len(points)} points")
    return points, iterations

# ============================================================================
# TSP SOLVER
# ============================================================================

def nearest_neighbor_tsp(points):
    """
    Solve TSP using nearest neighbor heuristic.
    Fast but not optimal.
    """
    print("Solving TSP with nearest neighbor method...")
    n = len(points)
    unvisited = set(range(n))
    path = [0]  # Start at first point
    unvisited.remove(0)
    
    current = 0
    while unvisited:
        # Find nearest unvisited point
        distances = cdist([points[current]], points[list(unvisited)])[0]
        nearest_idx = np.argmin(distances)
        nearest = list(unvisited)[nearest_idx]
        
        path.append(nearest)
        unvisited.remove(nearest)
        current = nearest
    
    return path

def two_opt(points, initial_path, iterations=100):
    """
    Improve TSP solution using 2-opt local search.
    """
    print(f"Optimizing with 2-opt ({iterations} iterations)...")
    path = initial_path.copy()
    n = len(path)
    
    improved = True
    iter_count = 0
    
    while improved and iter_count < iterations:
        improved = False
        iter_count += 1
        
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                # Calculate current distance
                current_dist = (
                    np.linalg.norm(points[path[i-1]] - points[path[i]]) +
                    np.linalg.norm(points[path[j]] - points[path[(j+1) % n]])
                )
                
                # Calculate distance after swap
                new_dist = (
                    np.linalg.norm(points[path[i-1]] - points[path[j]]) +
                    np.linalg.norm(points[path[i]] - points[path[(j+1) % n]])
                )
                
                if new_dist < current_dist:
                    # Reverse the segment
                    path[i:j+1] = path[i:j+1][::-1]
                    improved = True
        
        if iter_count % 10 == 0:
            print(f"  2-opt iteration {iter_count}/{iterations}")
    
    print(f"2-opt completed after {iter_count} iterations")
    return path

def solve_tsp(points, method='nearest_neighbor', two_opt_iter=100):
    """
    Solve TSP to find continuous path through points.
    """
    start_time = time.time()
    
    # Get initial path
    path = nearest_neighbor_tsp(points)
    
    # Optionally improve with 2-opt
    if method == '2opt':
        path = two_opt(points, path, two_opt_iter)
    
    elapsed = time.time() - start_time
    print(f"TSP solved in {elapsed:.2f} seconds")
    
    # Calculate total path length
    ordered_points = points[path]
    distances = np.linalg.norm(np.diff(ordered_points, axis=0), axis=1)
    total_distance = np.sum(distances)
    print(f"Total path length: {total_distance:.2f}")
    
    return path

# ============================================================================
# VISUALIZATION
# ============================================================================

def create_gradient_line_plot(points, path, iterations, color_by='position', 
                              colormap='twilight', linewidth=0.5, 
                              background='black', dpi=150):
    """
    Create a line plot with gradient coloring.
    """
    print("Creating visualization...")
    
    # Reorder points according to path
    ordered_points = points[path]
    ordered_iterations = iterations[path]
    
    # Create line segments
    segments = []
    for i in range(len(ordered_points) - 1):
        segments.append([ordered_points[i], ordered_points[i + 1]])
    
    segments = np.array(segments)
    
    # Determine colors
    if color_by == 'position':
        # Color by position in path
        colors = np.linspace(0, 1, len(segments))
    elif color_by == 'iteration':
        # Color by Mandelbrot iteration count
        colors = ordered_iterations[:-1]
        colors = colors / colors.max()  # Normalize
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 9), dpi=dpi)
    fig.patch.set_facecolor(background)
    ax.set_facecolor(background)
    
    # Create line collection with gradient
    lc = LineCollection(segments, cmap=colormap, linewidth=linewidth)
    lc.set_array(colors)
    
    # Add to plot
    line = ax.add_collection(lc)
    
    # Set limits
    ax.set_xlim(points[:, 0].min(), points[:, 0].max())
    ax.set_ylim(points[:, 1].min(), points[:, 1].max())
    
    # Equal aspect ratio
    ax.set_aspect('equal')
    
    # Remove axes
    ax.axis('off')
    
    # Tight layout
    plt.tight_layout(pad=0)
    
    print("Visualization created")
    return fig

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main execution function.
    """
    print("=" * 70)
    print("Mandelbrot Fractal TSP Line Drawing Generator")
    print("=" * 70)
    print()
    
    # Calculate Mandelbrot set
    M, X, Y = calculate_mandelbrot(
        MANDELBROT_WIDTH, MANDELBROT_HEIGHT,
        X_MIN, X_MAX, Y_MIN, Y_MAX,
        MAX_ITER
    )
    print()
    
    # Extract points
    points, iterations = extract_points(
        M, X, Y, NUM_POINTS,
        method=SAMPLE_METHOD,
        threshold=BOUNDARY_THRESHOLD
    )
    print()
    
    # Solve TSP
    path = solve_tsp(points, method=TSP_METHOD, two_opt_iter=TWO_OPT_ITERATIONS)
    print()
    
    # Create visualization
    fig = create_gradient_line_plot(
        points, path, iterations,
        color_by=COLOR_BY,
        colormap=COLORMAP,
        linewidth=LINE_WIDTH,
        background=BACKGROUND_COLOR,
        dpi=DPI
    )
    print()
    
    # Save output
    print(f"Saving to {OUTPUT_FILENAME}...")
    plt.savefig(OUTPUT_FILENAME, dpi=DPI, bbox_inches='tight', 
                pad_inches=0, facecolor=BACKGROUND_COLOR)
    print(f"Saved successfully!")
    print()
    
    # Show plot
    if SHOW_PLOT:
        print("Displaying plot...")
        plt.show()
    else:
        plt.close()
    
    print("=" * 70)
    print("Complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()