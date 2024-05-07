import numpy as np
from numba import jit


class Sphere:
    def __init__(self, position, radius, colour, shininess_const):
        self.position = position
        self.radius = radius
        self.colour = np.array(colour)
        self.shininess = shininess_const


class Light:
    def __init__(self, position, ambient_const, diffuse_const, specular_const):
        self.position = position
        self.ambient = ambient_const
        self.diffuse = diffuse_const
        self.specular = specular_const


@jit(nopython=True)
def z_of_sphere_point(sphere_centre, r, x, y):
    z = np.sqrt(r ** 2 - (x - sphere_centre[0]) ** 2 - (y - sphere_centre[1]) ** 2) + sphere_centre[2]
    return z if z >= 0 else -z


def get_z(sphere, point):
    return z_of_sphere_point(sphere.position, sphere.radius, point[0], point[1])


@jit(nopython=True)
def ambient_light(ambient, colour):
    return ambient * colour


def diffuse_light(diffuse, normal, light_dir, colour):
    return diffuse * np.dot(normal, light_dir) * colour


def specular_light(specular, normal, light_dir, view_dir, colour, shininess):
    reflected_vec = light_dir - 2 * np.dot(light_dir, normal) * normal
    cos_angle = np.dot(view_dir, reflected_vec) / (np.linalg.norm(view_dir) * np.linalg.norm(reflected_vec))
    return specular * colour * np.power(cos_angle, shininess)


def phong_lighting(sphere, light, point, camera):
    vec_to_viewer = (camera - point) / np.linalg.norm(camera - point)
    point[2] = get_z(sphere, point)

    normal = (point - sphere.position) / np.linalg.norm(point - sphere.position)
    vec_to_light = (light.position - point) / np.linalg.norm(light.position - point)

    ambient = ambient_light(light.ambient, sphere.colour)
    diffuse = diffuse_light(light.diffuse, normal, vec_to_light, sphere.colour)
    specular = specular_light(light.specular, normal, vec_to_light, vec_to_viewer, sphere.colour, sphere.shininess)
    illumination = ambient + diffuse + specular

    illumination_list = [int(min(255, max(0, i))) for i in illumination]
    return tuple(illumination_list)
