import math

def calculate_heading(p1, p2):
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    angle = math.atan2(y2-y1, x2-x1) * (180/math.pi)
    angle = (-angle) % 360
    return abs(angle)


def calculate_distance(point1, point2):
    x = point2[0] - point1[0]
    y = point2[1] - point1[1]
    return (math.sqrt(x*x + y*y))