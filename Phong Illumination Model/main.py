import math

import glfw
from OpenGL.GL import *


WIDTH = 800
HEIGHT = 600
SPHERE_CENTER = (WIDTH // 2, HEIGHT // 2)
SPHERE_RADIUS = 220
BACKGROUND = (12, 17, 25)
MATERIAL_COLOR = (0.12, 0.62, 0.72)
LIGHT_COLOR = (1.0, 0.88, 0.72)
AMBIENT_STRENGTH = 0.20
DIFFUSE_STRENGTH = 0.85
SPECULAR_STRENGTH = 0.90
SHININESS = 64
INITIAL_LIGHT_POSITION = (0.65, 0.55, 1.35)

SHADING_MODES = {
    "Ambient Only": (True, False, False),
    "Diffuse Only": (False, True, False),
    "Specular Only": (False, False, True),
    "Full Phong": (True, True, True),
}
KEY_SHADING_MODES = {
    glfw.KEY_1: "Ambient Only",
    glfw.KEY_2: "Diffuse Only",
    glfw.KEY_3: "Specular Only",
    glfw.KEY_4: "Full Phong",
}

light_position = list(INITIAL_LIGHT_POSITION)
shading_mode = "Full Phong"
scene_dirty = True


def dot(vector_a, vector_b):
    return sum(a * b for a, b in zip(vector_a, vector_b))


def normalize(vector):
    length = math.sqrt(dot(vector, vector))
    if length == 0.0:
        return (0.0, 0.0, 0.0)
    return tuple(component / length for component in vector)


def phong_illumination(point, normal, light_position, shininess):
    """Return one RGB pixel using the ambient, diffuse, and specular terms."""
    use_ambient, use_diffuse, use_specular = SHADING_MODES[shading_mode]
    view_direction = (0.0, 0.0, 1.0)
    light_direction = normalize(
        tuple(light_position[index] - point[index] for index in range(3))
    )
    normal_dot_light = max(0.0, dot(normal, light_direction))

    ambient = [0.0, 0.0, 0.0]
    diffuse = [0.0, 0.0, 0.0]
    specular = [0.0, 0.0, 0.0]

    if use_ambient:
        ambient = [
            AMBIENT_STRENGTH * component
            for component in MATERIAL_COLOR
        ]

    if use_diffuse:
        diffuse = [
            DIFFUSE_STRENGTH * normal_dot_light * material * light
            for material, light in zip(MATERIAL_COLOR, LIGHT_COLOR)
        ]

    if use_specular and normal_dot_light > 0.0:
        reflection = tuple(
            2.0 * normal_dot_light * normal[index] - light_direction[index]
            for index in range(3)
        )
        specular_factor = max(0.0, dot(reflection, view_direction)) ** shininess
        specular = [
            SPECULAR_STRENGTH * specular_factor * light
            for light in LIGHT_COLOR
        ]

    return tuple(
        min(255, max(0, int(255 * (a + d + s))))
        for a, d, s in zip(ambient, diffuse, specular)
    )


def render_scene():
    framebuffer = bytearray(BACKGROUND * (WIDTH * HEIGHT))
    center_x, center_y = SPHERE_CENTER
    min_y = max(0, center_y - SPHERE_RADIUS)
    max_y = min(HEIGHT, center_y + SPHERE_RADIUS)
    min_x = max(0, center_x - SPHERE_RADIUS)
    max_x = min(WIDTH, center_x + SPHERE_RADIUS)

    for pixel_y in range(min_y, max_y):
        normal_y = (pixel_y + 0.5 - center_y) / SPHERE_RADIUS
        for pixel_x in range(min_x, max_x):
            normal_x = (pixel_x + 0.5 - center_x) / SPHERE_RADIUS
            distance_squared = normal_x * normal_x + normal_y * normal_y

            if distance_squared > 1.0:
                continue

            normal_z = math.sqrt(1.0 - distance_squared)
            normal = (normal_x, normal_y, normal_z)
            color = phong_illumination(
                normal,
                normal,
                light_position,
                SHININESS,
            )
            pixel_index = (pixel_y * WIDTH + pixel_x) * 3
            framebuffer[pixel_index:pixel_index + 3] = bytes(color)

    return framebuffer


def update_window_title(window):
    glfw.set_window_title(
        window,
        f"Phong Illumination | {shading_mode} | Shininess: {SHININESS}",
    )


def key_callback(window, key, scancode, action, mods):
    global light_position, scene_dirty, shading_mode

    if action not in (glfw.PRESS, glfw.REPEAT):
        return

    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
        return

    if key in KEY_SHADING_MODES:
        shading_mode = KEY_SHADING_MODES[key]
    elif key == glfw.KEY_LEFT:
        light_position[0] -= 0.12
    elif key == glfw.KEY_RIGHT:
        light_position[0] += 0.12
    elif key == glfw.KEY_UP:
        light_position[1] += 0.12
    elif key == glfw.KEY_DOWN:
        light_position[1] -= 0.12
    elif key == glfw.KEY_R:
        light_position = list(INITIAL_LIGHT_POSITION)
        shading_mode = "Full Phong"
    else:
        return

    light_position[0] = max(-1.6, min(1.6, light_position[0]))
    light_position[1] = max(-1.6, min(1.6, light_position[1]))
    scene_dirty = True
    update_window_title(window)


def main():
    global scene_dirty

    if not glfw.init():
        raise RuntimeError("Could not initialize GLFW")

    glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
    window = glfw.create_window(
        WIDTH,
        HEIGHT,
        "Phong | Full Phong | Shininess: 64",
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

    print("Phong demo: 1 ambient, 2 diffuse, 3 specular, 4 full Phong.")
    print("Use arrow keys to move the light, R to reset, and Esc to exit.")

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