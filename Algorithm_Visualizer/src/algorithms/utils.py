def h_score(p1, p2):
    """Calculate heuristic using Manhattan distance

    Args:
        p1 (x,y): coordinates of point1
        p2 (x,y): coordinates of point2
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)