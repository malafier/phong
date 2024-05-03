import numpy as np
from numba import njit


class Sphere:
    def __init__(self, position, radius, colour, shininess_const):
        self.position = position
        self.radius = radius
        self.colour = np.array(colour)
        self.shininess = shininess_const

    def normal(self, point):
        return (point - self.position) / self.radius

    def view_dir(self, point):
        return (self.position - point) / np.linalg.norm(self.position - point)


class Light:
    def __init__(self, position, ambient_const, diffuse_const, specular_const):
        self.position = position
        self.ambient = ambient_const
        self.diffuse = diffuse_const
        self.specular = specular_const

    def light_dir(self, point):
        return (self.position - point) / np.linalg.norm(self.position - point)


@njit(fastmath=True)
def ambient_light(ambient, colour):
    return ambient * colour


def diffuse_light(diffuse, normal, light_dir, colour):
    return diffuse * np.dot(normal, light_dir) * colour


def specular_light(specular, normal, light_dir, view_dir, colour, shininess):
    reflect_dir = 2 * np.dot(normal, light_dir) * normal - light_dir
    specular_factor = pow(np.dot(view_dir, reflect_dir), shininess)
    return specular * specular_factor * colour


def phong_lighting(sphere, light, point, camera):
    normal = sphere.normal(point)
    light_dir = light.light_dir(point)
    view_dir = (camera - point) / np.linalg.norm(camera - point)

    ambient = ambient_light(light.ambient, sphere.colour)
    diffuse = diffuse_light(light.diffuse, normal, light_dir, sphere.colour)
    specular = specular_light(light.specular, normal, light_dir, view_dir, sphere.colour, sphere.shininess)
    illumination = ambient + diffuse + specular
    return tuple(int(min(255, max(0, i))) for i in illumination)
