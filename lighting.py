import numpy as np
from numba import jit
import config


class Sphere:
    def __init__(self, position, radius, colour, shininess_const=50, ambient=0.2, diffuse_const=0.5, specular_const=0.5):
        self.position = position
        self.radius = radius
        self.colour = np.array(colour)
        self.shininess = shininess_const
        self.ambient = ambient
        self.diffuse = diffuse_const
        self.specular = specular_const


class Light:
    def __init__(self, position):
        self.position = position
        self.ambient = 0.2
        self.light_colour = np.array([255, 255, 255])


@jit(nopython=True)
def z_of_sphere_point(sphere_centre, r, x, y):
    z = np.sqrt(r ** 2 - (x - sphere_centre[0]) ** 2 - (y - sphere_centre[1]) ** 2) + sphere_centre[2]
    return z if z >= 0 else -z


def get_z(sphere, point):
    return z_of_sphere_point(sphere.position, sphere.radius, point[0], point[1])


@jit(nopython=True)
def ambient_light():
    return config.AMBIENT_INTENSITY


def diffuse_light(normal, light_dir):
    return np.dot(normal, light_dir) * config.DIFFUSE_INTENSITY


def specular_light(normal, light_dir, view_dir, shininess):
    reflected_vec = light_dir - 2 * np.dot(light_dir, normal) * normal
    cos_angle = np.dot(view_dir, reflected_vec) / (np.linalg.norm(view_dir) * np.linalg.norm(reflected_vec))
    return np.power(cos_angle, shininess) * config.SPECULAR_INTENSITY


def phong_lighting(sphere, light, point, camera):
    vec_to_viewer = (camera - point) / np.linalg.norm(camera - point)
    point[2] = get_z(sphere, point)

    normal = (point - sphere.position) / np.linalg.norm(point - sphere.position)
    vec_to_light = (light.position - point) / np.linalg.norm(light.position - point)
    # light_x_colour = sphere.colour + light.light_colour
    # for i in range(len(light_x_colour)):
    #     if light_x_colour[i] > 255:
    #         light_x_colour[i] = 255

    ambient = sphere.ambient * ambient_light()
    diffuse = sphere.diffuse * diffuse_light(normal, vec_to_light)
    specular = sphere.specular * specular_light(normal, vec_to_light, vec_to_viewer, sphere.shininess)
    illumination = ambient + diffuse + specular
    # print(sphere.colour, illumination)

    illumination_list = [int(min(255, max(0, x * illumination))) for x in sphere.colour]
    return tuple(illumination_list)
