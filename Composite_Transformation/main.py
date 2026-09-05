import glfw
from OpenGL.GL import *
import math


def multiply(A, B):
    return [
        [
            sum(A[i][k] * B[k][j] for k in range(3))
            for j in range(3)
        ]
        for i in range(3)
    ]


def translation(tx, ty):
    return [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ]


def rotation(angle):
    r = math.radians(angle)
    c = math.cos(r)
    s = math.sin(r)

    return [
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1]
    ]


def scaling(sx, sy):
    return [
        [sx, 0,  0],
        [0, sy, 0],
        [0, 0,  1]
    ]


def shearing(shx, shy):
    return [
        [1,   shx, 0],
        [shy, 1,   0],
        [0,   0,   1]
    ]


def reflection_x():
    return [
        [1,  0, 0],
        [0, -1, 0],
        [0,  0, 1]
    ]


def reflection_y():
    return [
        [-1, 0, 0],
        [0,  1, 0],
        [0,  0, 1]
    ]


def transform_point(M, x, y):
    new_x = M[0][0] * x + M[0][1] * y + M[0][2]
    new_y = M[1][0] * x + M[1][1] * y + M[1][2]

    return new_x, new_y


def draw_axes():
    glColor3f(0.5, 0.5, 0.5)

    glBegin(GL_LINES)

    glVertex2f(-1, 0)
    glVertex2f(1, 0)

    glVertex2f(0, -1)
    glVertex2f(0, 1)

    glEnd()


def draw_triangle(vertices, r, g, b):
    glColor3f(r, g, b)

    glBegin(GL_TRIANGLES)

    for x, y in vertices:
        glVertex2f(x, y)

    glEnd()


def main():

    if not glfw.init():
        return

    window = glfw.create_window(
        800,
        600,
        "Experiment 4 - Composite Transformations",
        None,
        None
    )

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    triangle = [
        (-0.2, -0.2),
        (0.2, -0.2),
        (0.0, 0.3)
    ]

    T = translation(0.3, 0.2)
    R = rotation(30)
    S = scaling(0.7, 0.7)
    H = shearing(0.3, 0.0)

    M = multiply(T, multiply(R, multiply(S, H)))

    transformed_triangle = []

    for x, y in triangle:
        transformed_triangle.append(
            transform_point(M, x, y)
        )

    while not glfw.window_should_close(window):

        glClear(GL_COLOR_BUFFER_BIT)

        draw_axes()

        draw_triangle(
            triangle,
            0.0, 0.5, 1.0
        )

        draw_triangle(
            transformed_triangle,
            1.0, 0.2, 0.2
        )

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()