from math import pi, sin, cos, radians, degrees

def determine_line_box_clip(x, y, theta, b_width, b_height):
    a = sin(theta); b = cos(theta)
    c = (y * b - x * a)
    width = b_width; height = b_height

    if theta == 0:
        x1 = width
        y1 = (x1 * a + c) / b
    elif theta == pi/2:
        y1 = height
        x1 = (y1 * b - c) / a
    elif theta == pi:
        x1 = 0
        y1 = (x1 * a + c) / b
    elif theta == 3*pi/2:
        y1 = 0
        x1 = (y1 * b - c) / a
    else:
        if theta < pi/2:
            x1 = width
            y1 = (x1 * a + c) / b
            if y1 > height:
                y1 = height
                x1 = (y1 * b - c) / a
        elif theta < pi:
            y1 = height
            x1 = (y1 * b - c) / a
            if x1 < 0:
                x1 = 0
                y1 = (x1 * a + c) / b
        elif theta < 3*pi/2:
            x1 = 0
            y1 = (x1 * a + c) / b
            if y1 < 0:
                y1 = 0
                x1 = (y1 * b - c) / a
        elif theta < 2*pi:
            y1 = 0
            x1 = (y1 * b - c) / a
            if x1 > width:
                x1 = width
                y1 = (x1 * a + c) / b
    
    return (x1, y1)