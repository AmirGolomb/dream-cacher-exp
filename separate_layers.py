import numpy as np
import matplotlib.pyplot as plt

def group_heights_by_count(heights, count_threshold=30):
    """
    Group heights into sequences based on large counts.

    Parameters:
    - heights (list or np.ndarray): Array of height values.
    - count_threshold (int): Minimum count for a height to be considered large.

    Returns:
    - group_bounds (list of tuples): List of (min_height, max_height) bounds for each group.
    - groups (list of lists): List of groups of indices for the original heights.
    """
    # Get unique heights and their counts
    heights_rounded = np.round(heights)  # Round heights to the nearest integer
    unique_heights, counts = np.unique(heights_rounded, return_counts=True)

    # Filter heights with counts above the threshold
    valid_heights = unique_heights[counts >= count_threshold]

    # Identify consecutive sequences of valid heights
    groups = []
    group_bounds = []
    current_group = []

    for i, height in enumerate(valid_heights):
        if i > 0 and height != valid_heights[i - 1] + 1:
            # End of a sequence
            if current_group:
                group_bounds.append((current_group[0], current_group[-1]))
                groups.append(current_group)
            current_group = []
        current_group.append(height)

    # Handle the last group
    if current_group:
        group_bounds.append((current_group[0], current_group[-1]))
        groups.append(current_group)

    # Create the final list of indices for each group
    index_groups = []
    for bounds in group_bounds:
        min_height, max_height = bounds
        indices = [i for i, h in enumerate(heights) if min_height - 1 <= h <= max_height + 1]
        index_groups.append(indices)

    return group_bounds, index_groups




def draw_groups_in_3d(positions, index_groups):
    """
    Draw points in 3D space, coloring groups differently and ungrouped points in gray.

    Parameters:
    - heights (list or np.ndarray): Array of height values.
    - bounds (list of tuples): List of (min_height, max_height) bounds for each group.
    - index_groups (list of lists): List of groups of indices for the original heights.
    - positions (np.ndarray): 3D positions of points, shape (N, 3).

    Returns:
    - None. Displays the 3D plot.
    """
    print(f'positions={positions}')
    print(f'index_groups={index_groups}')
    # Ensure positions is a numpy array
    positions = np.array(positions)

    # Prepare a color map for the groups
    cmap = plt.cm.get_cmap('tab10', len(index_groups))  # A distinct color map for groups
    group_colors = [cmap(i) for i in range(len(index_groups))]

    # Identify indices that are not in any group
    all_grouped_indices = set(idx for group in index_groups for idx in group)
    ungrouped_indices = [i for i in range(len(positions[2])) if i not in all_grouped_indices]

    # Create a 3D plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot each group in its unique color
    for i, group_indices in enumerate(index_groups):
        group_positions = positions[:, group_indices]
        ax.scatter(group_positions[0, :], group_positions[1, :], group_positions[2, :],
                   color=group_colors[i], label=f"Group {i + 1}", s=50)

    # Plot ungrouped points in gray
    if ungrouped_indices:
        ungrouped_positions = positions[:, ungrouped_indices]
        ax.scatter(ungrouped_positions[0, :], ungrouped_positions[1, :], ungrouped_positions[2, :],
                   color='gray', label="Ungrouped", s=30, alpha=0.6)

    # Label the axes
    ax.set_xlabel("X Position")
    ax.set_ylabel("Y Position")
    ax.set_zlabel("Height")
    ax.set_title("3D Visualization of Groups")
    ax.legend()

    # Show the plot
    plt.show()


if __name__ == '__main__':
    # Example usage
    heights = np.array([100, 100, 100, 101, 101, 101, 101, 102, 103, 150, 151, 151, 151, 151, 151, 400,400,400,400, 151, 151, 152, 200, 201, 201,201,201,201,201,202,202,202,202, 203, 300, 301, 302, 400, 401])
    count_threshold = 2
    bounds, index_groups = group_heights_by_count(heights, count_threshold)
    print("Group bounds:", bounds)
    print("Index groups:", index_groups)

    positions = np.random.rand(len(heights), 3) * 100  # Random 3D positions
    print(np.shape(positions))
    positions[:,2] = heights
    draw_groups_in_3d(heights, index_groups, positions)