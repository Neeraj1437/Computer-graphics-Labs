from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# -------------------------------------------------
# Cohen-Sutherland Region Codes
# -------------------------------------------------
INSIDE = 0
LEFT = 1
RIGHT = 2
BOTTOM = 4
TOP = 8

# Clipping window
XMIN = -200
XMAX = 200
YMIN = -150
YMAX = 150


def compute_code(x, y):
    """Determine the region code for a point."""
    code = INSIDE

    if x < XMIN:
        code |= LEFT
    elif x > XMAX:
        code |= RIGHT

    if y < YMIN:
        code |= BOTTOM
    elif y > YMAX:
        code |= TOP

    return code


def cohen_sutherland_clip(x1, y1, x2, y2):
    """
    Cohen-Sutherland line clipping algorithm.

    Returns:
        (True, clipped coordinates) if line is visible
        (False, None) if line is completely outside
    """

    code1 = compute_code(x1, y1)
    code2 = compute_code(x2, y2)

    while True:

        # Case 1: Both points are inside
        if code1 == 0 and code2 == 0:
            return True, (x1, y1, x2, y2)

        # Case 2: Both points are outside in the same region
        elif (code1 & code2) != 0:
            return False, None

        # Case 3: Line needs clipping
        else:

            # Select a point outside the clipping window
            if code1 != 0:
                code_out = code1
            else:
                code_out = code2

            # Find intersection point
            if code_out & TOP:
                # Point is above the window
                x = x1 + (x2 - x1) * (YMAX - y1) / (y2 - y1)
                y = YMAX

            elif code_out & BOTTOM:
                # Point is below the window
                x = x1 + (x2 - x1) * (YMIN - y1) / (y2 - y1)
                y = YMIN

            elif code_out & RIGHT:
                # Point is to the right
                y = y1 + (y2 - y1) * (XMAX - x1) / (x2 - x1)
                x = XMAX

            elif code_out & LEFT:
                # Point is to the left
                y = y1 + (y2 - y1) * (XMIN - x1) / (x2 - x1)
                x = XMIN

            # Replace the outside point with intersection point
            if code_out == code1:
                x1, y1 = x, y
                code1 = compute_code(x1, y1)
            else:
                x2, y2 = x, y
                code2 = compute_code(x2, y2)


# -------------------------------------------------
# OpenGL Initialization
# -------------------------------------------------
def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluOrtho2D(-400, 400, -300, 300)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


# -------------------------------------------------
# Draw Clipping Window
# -------------------------------------------------
def draw_clipping_window():
    glColor3f(1.0, 1.0, 1.0)

    glBegin(GL_LINE_LOOP)
    glVertex2f(XMIN, YMIN)
    glVertex2f(XMAX, YMIN)
    glVertex2f(XMAX, YMAX)
    glVertex2f(XMIN, YMAX)
    glEnd()


# -------------------------------------------------
# Display Function
# -------------------------------------------------
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # Draw clipping rectangle
    draw_clipping_window()

    # Original line
    x1, y1 = -350, -250
    x2, y2 = 350, 250

    # Draw original line in red
    glColor3f(1.0, 0.0, 0.0)

    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

    # Perform Cohen-Sutherland clipping
    visible, result = cohen_sutherland_clip(
        x1, y1, x2, y2
    )

    # Draw clipped line in green
    if visible:
        cx1, cy1, cx2, cy2 = result

        glColor3f(0.0, 1.0, 0.0)
        glLineWidth(4.0)

        glBegin(GL_LINES)
        glVertex2f(cx1, cy1)
        glVertex2f(cx2, cy2)
        glEnd()

        glLineWidth(1.0)

    glFlush()


# -------------------------------------------------
# Keyboard Function
# -------------------------------------------------
def keyboard(key, x, y):
    if key == b'\x1b':       # ESC key
        glutLeaveMainLoop()


# -------------------------------------------------
# Main Function
# -------------------------------------------------
def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)

    glutCreateWindow(
        b"Cohen-Sutherland Line Clipping Algorithm"
    )

    init()

    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)

    glutMainLoop()


if __name__ == "__main__":
    main()