from sklearn.linear_model import RANSACRegressor
import numpy as np



def ransac_find_shabash(shabash_loc_2d_and_zs, ground_asl):

    # Extract x, y, z
    points = np.array(shabash_loc_2d_and_zs)
    X = points[:, :2]  # x, y
    Z = points[:, 2]  # z

    # Fit robust regression
    ransac = RANSACRegressor().fit(X, Z)

    # Get coefficients of the line
    coef = ransac.estimator_.coef_
    intercept = ransac.estimator_.intercept_

    # Intersection with z = ground_asl
    t = (ground_asl - intercept) / coef[1]
    intersection_x = X[0][0] + coef[0] * t
    intersection_y = X[0][1] + coef[1] * t

    print(f"Intersection at: ({intersection_x}, {intersection_y}, {ground_asl})")
    return (intersection_x, intersection_y, ground_asl), coef, intercept
