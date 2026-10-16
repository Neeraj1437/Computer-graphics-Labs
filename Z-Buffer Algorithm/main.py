import math

import glfw
from OpenGL.GL import *


WIDTH = 800
HEIGHT = 600
BACKGROUND = (13, 18, 25)

# Each shape is (name, polygon vertices, color); smaller depth is closer.
SHAPES = [
    (
        "diamond",
        ((260, 285, 0.22), (400, 155, 0.28), (545, 285, 0.24), (400, 440, 0.32)),
        (40, 205, 150),
    ),
    (
        "circle",
        tuple(
            (610 + 92 * math.cos(2 * math.pi * index / 40),
             435 + 92 * math.sin(2 * math.pi * index / 40),
             0.42)
            for index in range(40)
        ),
        (220, 85, 175),
    ),
    (
        "rectangle",
        ((320, 90, 0.56), (710, 90, 0.56), (710, 365, 0.56), (320, 365, 0.56)),
        (245, 165, 55),
    ),
    (
        "triangle",
        ((90, 100, 0.78), (410, 120, 0.78), (250, 430, 0.78)),
        (65, 130, 245),
    ),
]

draw_near_first = True
diamond_in_front = True
scene_dirty = True


def rasterize_triangle(framebuffer, depth_buffer, vertices, color):
    """Rasterize a triangle and keep only fragments nearest the viewer."""
    (x0, y0, z0), (x1, y1, z1), (x2, y2, z2) = vertices

    denominator = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
    if math.isclose(denominator, 0.0):
        return

    min_x = max(0, math.floor(min(x0, x1, x2)))
    max_x = min(WIDTH - 1, math.ceil(max(x0, x1, x2)))
    min_y = max(0, math.floor(min(y0, y1, y2)))
    max_y = min(HEIGHT - 1, math.ceil(max(y0, y1, y2)))

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            sample_x = x + 0.5
            sample_y = y + 0.5

            weight0 = (
                (y1 - y2) * (sample_x - x2)
                + (x2 - x1) * (sample_y - y2)
            ) / denominator
            weight1 = (
                (y2 - y0) * (sample_x - x2)
                + (x0 - x2) * (sample_y - y2)
            ) / denominator
            weight2 = 1.0 - weight0 - weight1

            if min(weight0, weight1, weight2) < 0.0:
                continue

            depth = weight0 * z0 + weight1 * z1 + weight2 * z2
            pixel_index = y * WIDTH + x

            if depth < depth_buffer[pixel_index]:
                depth_buffer[pixel_index] = depth
                color_index = pixel_index * 3
                framebuffer[color_index:color_index + 3] = bytes(color)


def render_scene():
    framebuffer = bytearray(BACKGROUND * (WIDTH * HEIGHT))
    depth_buffer = [float("inf")] * (WIDTH * HEIGHT)
    shapes = SHAPES if draw_near_first else reversed(SHAPES)

    for name, vertices, color in shapes:
        if not diamond_in_front:
            if name == "diamond":
                vertices = tuple((x, y, 0.88) for x, y, _ in vertices)
            elif name == "rectangle":
                vertices = tuple((x, y, 0.10) for x, y, _ in vertices)

        for index in range(1, len(vertices) - 1):
            triangle = (vertices[0], vertices[index], vertices[index + 1])
            rasterize_triangle(framebuffer, depth_buffer, triangle, color)

    indicator_color = (40, 205, 150) if diamond_in_front else (245, 165, 55)
    indicator_start = 32 if diamond_in_front else WIDTH // 2 + 8
    indicator_end = indicator_start + WIDTH // 2 - 40
    for y in range(HEIGHT - 30, HEIGHT - 14):
        for x in range(24, WIDTH - 24):
            color = indicator_color if indicator_start <= x < indicator_end else (55, 65, 78)
            pixel_index = (y * WIDTH + x) * 3
            framebuffer[pixel_index:pixel_index + 3] = bytes(color)

    return framebuffer


def key_callback(window, key, scancode, action, mods):
    global diamond_in_front, draw_near_first, scene_dirty

    if action != glfw.PRESS:
        return

    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
    elif key == glfw.KEY_SPACE:
        diamond_in_front = not diamond_in_front
        scene_dirty = True
        front_shape = "diamond" if diamond_in_front else "rectangle"
        print("Frontmost overlapping shape:", front_shape)
        update_window_title(window)
    elif key == glfw.KEY_D:
        draw_near_first = not draw_near_first
        scene_dirty = True
        order = "near-to-far" if draw_near_first else "far-to-near"
        print("Drawing order:", order)
        update_window_title(window)


def update_window_title(window):
    front_shape = "Diamond" if diamond_in_front else "Rectangle"
    order = "near-to-far" if draw_near_first else "far-to-near"
    glfw.set_window_title(window, f"Z-Buffer | {front_shape} in front | {order}")


def main():
    global scene_dirty

    if not glfw.init():
        raise RuntimeError("Could not initialize GLFW")

    glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
    window = glfw.create_window(
        WIDTH,
        HEIGHT,
        "Z-Buffer | Diamond in front | near-to-far",
        None,
        None,
    )

    if not window:
        glfw.terminate()
        raise RuntimeError("Could not create the GLFW window")

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WIDTH, 0, HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    print("Z-buffer demo: Space swaps the frontmost shape; D reverses draw order; Esc exits.")

    framebuffer = render_scene()
    scene_dirty = False
    while not glfw.window_should_close(window):
        if scene_dirty:
            framebuffer = render_scene()
            scene_dirty = False

        glClear(GL_COLOR_BUFFER_BIT)
        glRasterPos2i(0, 0)
        glDrawPixels(WIDTH, HEIGHT, GL_RGB, GL_UNSIGNED_BYTE, framebuffer)
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()