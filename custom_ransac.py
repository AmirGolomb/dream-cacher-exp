import numpy as np
from sklearn.linear_model import RANSACRegressor
from sklearn.base import BaseEstimator, RegressorMixin
# Visualize the result
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from move_fig_to_screen_center import move_fig_to_screen_center


# Custom 3D Line Model for RANSAC
class LineModel3D(BaseEstimator, RegressorMixin):
    def fit(self, X, y=None):
        """
        Fit a line to 3D points using SVD for best-fit line.
        """
        # Center the points
        self.mean_ = np.mean(X, axis=0)
        centered_points = X - self.mean_

        # Use SVD to find the direction vector (principal axis)
        _, _, vh = np.linalg.svd(centered_points)
        self.direction_ = vh[0]  # First singular vector is the line direction
        return self

    def predict(self, X):
        """
        Project points onto the best-fit line.
        """
        direction = self.direction_
        mean = self.mean_
        projections = np.dot(X - mean, direction)[:, None] * direction + mean
        return projections

    def score(self, X, y=None):
        """
        Compute the score as the inverse of the mean squared distance to the line.
        """
        projections = self.predict(X)
        distances = np.linalg.norm(X - projections, axis=1)
        return -np.mean(distances)  # Negative because RANSAC maximizes the score


# # Example noisy 3D points
# shabash_loc_2d_and_zs = [
#     (1, 1, 80),
#     (2, 2, 83),
#     (3, 3, 85),
#     (4, 4, 77),  # A point close to z=77
#     (5, 5, 95),
#     (6, 6, 90),
#     (7, 7, 92),
#     (50, 50, 300),  # Outlier
#     (60, 60, -100),  # Outlier
# ]


def custom_ransac(shabash_loc_2d_and_zs, ground_asl):
    # Convert list to numpy array
    points = np.array(shabash_loc_2d_and_zs)

    # Apply RANSAC to fit the 3D line
    ransac = RANSACRegressor(estimator=LineModel3D(), min_samples=2, residual_threshold=5.0, random_state=42)

    # ransac.fit(points, np.zeros(points.shape[0]))  # Dummy y, not used
    ransac.fit(points, points)  # Use points themselves as the target


    # Extract the line parameters
    line_point = ransac.estimator_.mean_  # A point on the line
    direction_vector = ransac.estimator_.direction_  # Direction vector of the line
    print(f"Point on Line: {line_point}")
    print(f"Direction Vector: {direction_vector}")

    # Find intersection with z=ground_asl plane
    t = (ground_asl - line_point[2]) / direction_vector[2]
    intersection_x = line_point[0] + t * direction_vector[0]
    intersection_y = line_point[1] + t * direction_vector[1]

    print(f"Intersection with z=ground_asl at: x={intersection_x}, y={intersection_y}, z={ground_asl}")



    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Plot original points
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], color='blue', label='Data Points')

    # Plot inliers
    inlier_mask = ransac.inlier_mask_
    ax.scatter(points[inlier_mask, 0], points[inlier_mask, 1], points[inlier_mask, 2], color='green', label='Inliers')

    # Plot the fitted line
    line_t = np.linspace(-300, 300, 100)  # Parameter range for visualization
    line_x = line_point[0] + line_t * direction_vector[0]
    line_y = line_point[1] + line_t * direction_vector[1]
    line_z = line_point[2] + line_t * direction_vector[2]
    ax.plot(line_x, line_y, line_z, color='red', label='Fitted Line')

    # Highlight intersection with z=ground_asl
    ax.scatter(intersection_x, intersection_y, ground_asl, color='orange', label=f'Intersection with z={ground_asl}')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    plt.title("3D Line Fitting with RANSAC")
    # fig.canvas.manager.window.move(200, 200)
    move_fig_to_screen_center(fig)
    plt.show()

    return (intersection_x, intersection_y, ground_asl), line_point, direction_vector
