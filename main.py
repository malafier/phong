import numpy as np
import pygame as pg

from config import SCREEN_WIDTH, SCREEN_HEIGHT, Colour
from lighting import phong_lighting, Sphere, Light

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
pg.display.set_caption("Phong Lighting")

MOVEMENT_QUANTUM = 200

if __name__ == "__main__":
    running = True
    spheres = [
        Sphere(
            np.array([SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 0]),
            100,
            Colour.BROWN.value,
            50,
            diffuse_const=0.5,
            specular_const=0.5
        ),
        Sphere(
            np.array([SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 0]),
            100,
            Colour.METAL_GREY.value,
            500,
            diffuse_const=1,
            specular_const=0.01
        ),
        Sphere(
            np.array([SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 0]),
            100,
            Colour.WHITE.value,
            2,
            diffuse_const=0.01,
            specular_const=1
        )
    ]
    light = Light(np.array([800, -600, 800]),)
    camera = np.array([0, 0, -1000])

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
            light.position[2] += MOVEMENT_QUANTUM
        if keys[pg.K_s]:
            light.position[2] -= MOVEMENT_QUANTUM
        if keys[pg.K_a]:
            light.position[0] -= MOVEMENT_QUANTUM
        if keys[pg.K_d]:
            light.position[0] += MOVEMENT_QUANTUM
        if keys[pg.K_q]:
            light.position[1] -= MOVEMENT_QUANTUM
        if keys[pg.K_e]:
            light.position[1] += MOVEMENT_QUANTUM
        print(i, light.position)

        sphere = spheres[i]
        for x in range(sphere.position[0] - sphere.radius, sphere.position[0] + sphere.radius):
            for y in range(sphere.position[1] - sphere.radius, sphere.position[1] + sphere.radius):
                rel_x = x - sphere.position[0]
                rel_y = y - sphere.position[1]
                if rel_x ** 2 + rel_y ** 2 <= sphere.radius ** 2:
                    point = np.array([x, y, 0])
                    colour = phong_lighting(sphere, light, point, camera)
                    pg.draw.circle(screen, colour, (x, y), 1)
        pg.display.update()
    pg.quit()
