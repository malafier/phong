import numpy as np
import pygame as pg
from numba import jit

from config import SCREEN_WIDTH, SCREEN_HEIGHT, Colour, MOVEMENT_QUANTUM, SCREEN_CENTRE
from lighting import phong_lighting, Sphere

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
pg.display.set_caption("Phong")


@jit(nopython=True)
def in_circle(r_x, r_y, r):
    return r_x ** 2 + r_y ** 2 <= r ** 2


if __name__ == "__main__":
    running = True
    spheres = [
        Sphere(
            "WOOD",
            SCREEN_CENTRE,
            100,
            Colour.OAK_BROWN.value,
            shininess_const=20,
            ambient_const=0.2,
            diffuse_const=0.45,
            specular_const=0.15
        ),
        Sphere(
            "METAL",
            SCREEN_CENTRE,
            100,
            Colour.METAL_GREY.value,
            shininess_const=200,
            ambient_const=0.2,
            diffuse_const=0.05,
            specular_const=1
        ),
        Sphere(
            "PLASTIC",
            SCREEN_CENTRE,
            100,
            Colour.CYAN.value,
            shininess_const=40,
            ambient_const=0.1,
            diffuse_const=0.55,
            specular_const=0.55
        ),
        Sphere(
            "CHALK",
            SCREEN_CENTRE,
            100,
            Colour.WHITE.value,
            shininess_const=5,
            diffuse_const=0.95,
            specular_const=0.001
        )
    ]
    light = np.array([800, -600, 800])
    view_dir = np.array([0, 0, 1])

    i = 0
    spheres_len = len(spheres)
    while running:
        screen.fill(Colour.GREY.value)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            running = False

        if keys[pg.K_SPACE]:
            i = (i + 1) % spheres_len

        if keys[pg.K_w]:
            light[2] += MOVEMENT_QUANTUM
        if keys[pg.K_s]:
            light[2] -= MOVEMENT_QUANTUM
        if keys[pg.K_a]:
            light[0] -= MOVEMENT_QUANTUM
        if keys[pg.K_d]:
            light[0] += MOVEMENT_QUANTUM
        if keys[pg.K_q]:
            light[1] -= MOVEMENT_QUANTUM
        if keys[pg.K_e]:
            light[1] += MOVEMENT_QUANTUM
        print(i, light)

        if 0 <= light[0] < SCREEN_WIDTH and 0 <= light[1] < SCREEN_HEIGHT:
            pg.draw.circle(screen, Colour.YELLOW.value, (int(light[0]), int(light[1])), 3)
        sphere = spheres[i]
        for x in range(sphere.position[0] - sphere.radius, sphere.position[0] + sphere.radius):
            for y in range(sphere.position[1] - sphere.radius, sphere.position[1] + sphere.radius):
                rel_x = x - sphere.position[0]
                rel_y = y - sphere.position[1]
                if in_circle(rel_x, rel_y, sphere.radius):
                    colour = phong_lighting(sphere, light, np.array([x, y, 0]), view_dir)
                    pg.draw.circle(screen, colour, (x, y), 1)
        pg.display.set_caption(f"Phong - {sphere.name}")
        pg.display.update()
    pg.quit()
