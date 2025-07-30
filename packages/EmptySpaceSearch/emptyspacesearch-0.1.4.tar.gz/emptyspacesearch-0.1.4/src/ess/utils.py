import logging
import numpy as np


logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def calculate_grid_coverage(points, bounds, grid):
    """
    Calculates grid-based coverage of N-dimensional points.

    Args:
        points (np.ndarray): A 2D NumPy array of shape (N_points, N_dims)
        where N_points is the number of points, and N_dims is the number of dimensions.
        
        bounds (np.ndarray): A 2D array of shape (N_dims,2) specifying 
        the minimum and maximum coordinate for each dimension of the grid.
        
        grid (int or tuple or list): The number of bins (cells)
        along each dimension. If int, it's used for all N_dims.
        If tuple/list (res1, res2, ..., resN), specifies bins for each dimension.

    Returns:
        percentage_coverage (float): The percentage of the total grid area (volume) covered.
    """
    num_dims = points.shape[1]

    if isinstance(grid, int):
        bins = [grid] * num_dims
    elif len(grid) != num_dims:
        raise ValueError(f"grid_resolutions must be an int or a list/tuple of length {num_dims}")
    else:
        bins = list(grid)

    # Define bin edges for each dimension
    # np.histogramdd expects a list of 1D arrays for bin edges
    bin_edges = []
    for d in range(num_dims):
        bin_edges.append(np.linspace(bounds[d, 0], bounds[d, 1], bins[d] + 1))

    # Use np.histogramdd to count points in each N-dimensional bin
    # The output 'H' is an N-dimensional array where H[i, j, k, ...]
    # is the number of points in the corresponding N-dim cell.
    H, _ = np.histogramdd(points, bins=bin_edges)

    # Create the coverage map: 1 if cell has points, 0 otherwise
    coverage_map = (H > 0).astype(int)

    # Calculate metrics
    total_covered_cells = np.sum(coverage_map)
    
    total_grid_cells = np.prod(bins) # Product of resolutions for total cells

    if total_grid_cells == 0: # Avoid division by zero if no cells are defined
        percentage_coverage = 0.0
    else:
        percentage_coverage = (total_covered_cells / total_grid_cells)

    # Calculate cell hyper-volume
    #cell_dimensions = [(max_coords[d] - min_coords[d]) / bins[d] for d in range(num_dims)]
    #cell_volume = np.prod(cell_dimensions)

    return percentage_coverage