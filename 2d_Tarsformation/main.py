import glfw
from OpenGL.GL import *
import math


# =========================================================
# Original Triangle
# =========================================================

original = [
    (1.0, 1.0),
    (4.0, 1.0),
    (2.5, 4.0)
]

triangle = original.copy()


# =========================================================
# Homogeneous Coordinate Transformation
# =========================================================

def transform_point(matrix, point):

    x, y = point

    # Homogeneous coordinate:
    # [x, y, 1]

    new_x = (
        matrix[0][0] * x +
        matrix[0][1] * y +
        matrix[0][2]
    )

    new_y = (
        matrix[1][0] * x +
        matrix[1][1] * y +
        matrix[1][2]
    )

    return new_x, new_y


# =========================================================
# Translation Matrix
# =========================================================

def translation(tx, ty):

    return [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ]


# =========================================================
# Rotation Matrix
# =========================================================

def rotation(angle):

    theta = math.radians(angle)

    c = math.cos(theta)
    s = math.sin(theta)

    return [
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1]
    ]


# =========================================================
# Scaling Matrix
# =========================================================

def scaling(sx, sy):

    return [
        [sx, 0,  0],
        [0,  sy, 0],
        [0,  0,  1]
    ]


# =========================================================
# Reflection about X-axis
# =========================================================

def reflection_x():

    return [
        [1,  0, 0],
        [0, -1, 0],
        [0,  0, 1]
    ]


# =========================================================
# Reflection about Y-axis
# =========================================================

def reflection_y():

    return [
        [-1, 0, 0],
        [0,  1, 0],
        [0,  0, 1]
    ]


# =========================================================
# Reflection about Origin
# =========================================================

def reflection_origin():

    return [
        [-1,  0, 0],
        [0, -1, 0],
        [0,  0, 1]
    ]


# =========================================================
# Apply Transformation to Original Triangle
# =========================================================

def transform_triangle(matrix):

    global triangle

    triangle = []

    triangle.extend(
        transform_point(matrix, point)
        for point in original
    )


# =========================================================
# Keyboard Callback
# =========================================================

def key_callback(window, key, scancode, action, mods):

    global triangle

    # Execute only once per key press
    if action != glfw.PRESS:
        return


    # -----------------------------------------------------
    # 0 = Original Position
    # -----------------------------------------------------

    if key == glfw.KEY_0:

        triangle = original.copy()

        print("Original position")


    # -----------------------------------------------------
    # 1 = Translation
    # -----------------------------------------------------

    elif key == glfw.KEY_1:

        T = translation(2.0, 1.0)

        transform_triangle(T)

        print("Translation")


    # -----------------------------------------------------
    # 2 = Rotation
    # -----------------------------------------------------

    elif key == glfw.KEY_2:

        R = rotation(30)

        transform_triangle(R)

        print("Rotation")


    # -----------------------------------------------------
    # 3 = Scaling
    # -----------------------------------------------------

    elif key == glfw.KEY_3:

        S = scaling(1.2, 1.2)

        transform_triangle(S)

        print("Scaling")


    # -----------------------------------------------------
    # 4 = Reflection about X-axis
    # -----------------------------------------------------

    elif key == glfw.KEY_4:

        RX = reflection_x()

        transform_triangle(RX)

        print("Reflection about X-axis")


    # -----------------------------------------------------
    # 5 = Reflection about Y-axis
    # -----------------------------------------------------

    elif key == glfw.KEY_5:

        RY = reflection_y()

        transform_triangle(RY)

        print("Reflection about Y-axis")


    # -----------------------------------------------------
    # 6 = Reflection about Origin
    # -----------------------------------------------------

    elif key == glfw.KEY_6:

        RO = reflection_origin()

        transform_triangle(RO)

        print("Reflection about Origin")


    # -----------------------------------------------------
    # ESC = Exit
    # -----------------------------------------------------

    elif key == glfw.KEY_ESCAPE:

        glfw.set_window_should_close(window, True)


# =========================================================
# Draw Triangle
# =========================================================

def draw_triangle():

    glBegin(GL_TRIANGLES)

    for x, y in triangle:

        glVertex2f(x, y)

    glEnd()


# =========================================================
# Draw Coordinate Axes
# =========================================================

def draw_axes():

    glBegin(GL_LINES)

    # X-axis
    glVertex2f(-10, 0)
    glVertex2f(10, 0)

    # Y-axis
    glVertex2f(0, -7.5)
    glVertex2f(0, 7.5)

    glEnd()


# =========================================================
# Main Function
# =========================================================

def main():

    global triangle

    # Initialize GLFW
    if not glfw.init():

        print("GLFW initialization failed")
        return


    # Create window
    window = glfw.create_window(
        800,
        600,
        "2D Transformations using Homogeneous Coordinates",
        None,
        None
    )

    if not window:

        glfw.terminate()
        return


    glfw.make_context_current(window)


    # Register keyboard callback
    glfw.set_key_callback(
        window,
        key_callback
    )


    # -----------------------------------------------------
    # Set 2D Coordinate System
    # -----------------------------------------------------

    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()

    glOrtho(
        -10, 10,
        -7.5, 7.5,
        -1, 1
    )

    glMatrixMode(GL_MODELVIEW)


    # -----------------------------------------------------
    # Main Loop
    # -----------------------------------------------------

    while not glfw.window_should_close(window):

        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT)

        glLoadIdentity()


        # Draw axes
        glColor3f(1.0, 1.0, 1.0)

        draw_axes()


        # Draw triangle
        glColor3f(0.0, 1.0, 0.0)

        draw_triangle()


        # Draw outline
        glColor3f(1.0, 0.0, 0.0)

        glBegin(GL_LINE_LOOP)

        for x, y in triangle:

            glVertex2f(x, y)

        glEnd()


        # Update screen
        glfw.swap_buffers(window)

        glfw.poll_events()


    glfw.terminate()


# =========================================================
# Run
# =========================================================

if __name__ == "__main__":

    main()