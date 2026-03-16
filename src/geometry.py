import cv2
import numpy as np

def simplify_polygon(poly: list[tuple[int, int]], epsilon_ratio: float = 0.002) -> list[tuple[int, int]]:
    """
    Simplify a polygon by approximating it with fewer points.

    Uses the Douglas-Peucker algorithm via OpenCV to reduce the number of
    vertices while preserving the overall shape.

    Args:
        poly: List of (x, y) points defining the polygon.
        epsilon_ratio: Fraction of the perimeter to use as the approximation
            epsilon (default 0.002). Higher values result in simpler polygons.

    Returns:
        List of (x, y) points defining the simplified polygon.
    """
    # Convert to numpy array and reshape for OpenCV
    pts = np.array(poly, dtype=np.int32).reshape((-1, 1, 2))

    # Calculate perimeter for epsilon scaling
    perimeter = cv2.arcLength(pts, True)
    epsilon = epsilon_ratio * perimeter

    # Approximate the polygon
    approx = cv2.approxPolyDP(pts, epsilon, True)

    # Convert back to list of tuples
    return [(int(p[0][0]), int(p[0][1])) for p in approx]


def find_space_containing_point(point: tuple[int, int], spaces):
    """
    Return the first Space whose polygon contains the point.
    Returns None if the point is not inside any space.
    """
    x, y = point

    for space in spaces:
        polygon = np.array(space.polygon, dtype=np.int32).reshape((-1, 1, 2))
        result = cv2.pointPolygonTest(polygon, (x, y), False)

        if result >= 0:
            return space

    return None