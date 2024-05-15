import numpy as np
from numba import jit

import config


class Sphere:
    def __init__(
            self,
            name,
            position,
            radius,
            colour,
            shininess_const=50,
            ambient_const=0.2,
            diffuse_const=0.5,
            specular_const=0.5
    ):
        self.name = name
        self.position = position
        self.radius = radius
        self.colour = np.array(colour)

        self.shininess = shininess_const
        self.ambient = ambient_const
        self.diffuse = diffuse_const
        self.specular = specular_const


@jit(nopython=True)
def z_of_sphere_point(sphere_centre, r, x, y):
    z_sqrt = r ** 2 - (x - sphere_centre[0]) ** 2 - (y - sphere_centre[1]) ** 2
    return np.sqrt(z_sqrt) + sphere_centre[2] if z_sqrt >= 0 else np.nan


@jit(nopython=True)
def normal_of(x, y, z):
    length = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    return np.array([x / length, y / length, z / length])


@jit(nopython=True)
def ambient_light(ambient):
    return ambient * config.I_a


def diffuse_light(diffuse, normal, light_dir):
    return diffuse * config.I_d * max(np.dot(normal, light_dir), 0)


def specular_light(specular, normal, light_dir, view_dir, shininess):
    reflection = 2 * max(np.dot(light_dir, normal), 0) * normal - light_dir
    cos_angle = np.dot(view_dir, reflection) / (np.linalg.norm(view_dir) * np.linalg.norm(reflection))
    return specular * config.I_s * np.power(cos_angle, shininess)


def phong_lighting(sphere, light, point, view_dir):
    point[2] = z_of_sphere_point(sphere.position, sphere.radius, point[0], point[1])
    normal = normal_of(point[0] - sphere.position[0], point[1] - sphere.position[1], point[2] - sphere.position[2])

    # light dir and light colour
    light_dir = light - point
    light_dir = light_dir / np.linalg.norm(light_dir)
    light = np.array([255, 255, 255])
    light_x_colour = (light * sphere.colour) / np.linalg.norm(light)

    ambient = sphere.colour * ambient_light(sphere.ambient)
    diffuse = light_x_colour * diffuse_light(sphere.diffuse, normal, light_dir)
    specular = light * specular_light(sphere.specular, normal, light_dir, view_dir, sphere.shininess)
    illumination = ambient + diffuse + specular

    illumination_list = [int(min(255, max(0, x))) for x in illumination]
    return tuple(illumination_list)
