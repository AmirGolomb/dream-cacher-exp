import numpy as np

from find_shabash_2d import find_shabash_2d
from find_shabash_2d_bins import find_shabash_2d_bins

# Set random seed for reproducibility
np.random.seed(42)

# Number of points to generate
num_points = 100

# Generate random 2D points within the 10x10 square
x_history = np.random.uniform(0, 10, num_points)
y_history = np.random.uniform(0, 10, num_points)

# Fixed point (2, 4)
fixed_point = np.array([2, 4])

# Calculate the Euclidean distance to the fixed point for each (x, y) pair
distances = np.sqrt((x_history - fixed_point[0])**2 + (y_history - fixed_point[1])**2)

# Generate evodif_history based on the distance, adding some noise
# Let's say the relationship between distance and evodif is roughly inversely proportional
# with added noise. The base value will be between 50 and -30.
evodif_history = 5 * (10 - distances) + np.random.normal(0, 1, num_points)

# Ensure the evodif values are within the range [-30, 50]
evodif_history = np.clip(evodif_history, -30, 50)

# Printing first few values as a check
print("x_history:", x_history[:50])
print("y_history:", y_history[:50])
print("evodif_history:", evodif_history[:50])

source = find_shabash_2d_bins(x_history, y_history, evodif_history)
print(f'source={source}')
