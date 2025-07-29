import numpy as np
import sapien
from jaxtyping import Float
from sapien import Component
from sapien.render import RenderBodyComponent

from dexmotion_viz.sapien_viz.sapien_utils import find_all_components


class SphereGroupComponent(Component):
    def __init__(self, entity: sapien.Entity):
        super().__init__()
        entity.add_component(self)

        self.sphere_pos: list[Float[np.ndarray, "3"]] = []
        self.sphere_radius: list[float] = []
        self.sphere_visuals: list[RenderBodyComponent] = []
        self._sphere_enabled: bool = True

        self.red_mat = sapien.render.RenderMaterial(base_color=[1, 0.2, 0.2, 1])

    def add_sphere(self, pos: list[float], radius: float):
        self.sphere_pos.append(pos)
        self.sphere_radius.append(radius)
        self.sphere_visuals.append(self._create_sphere_visual(pos, radius))

    def remove_sphere(self, index: int):
        self.sphere_pos.pop(index)
        self.sphere_radius.pop(index)

        to_be_removed = self.sphere_visuals.pop(index)
        self.entity.remove_component(to_be_removed)

    def transform_all_spheres(self, pose: sapien.Pose):
        mat = pose.to_transformation_matrix()
        rot = mat[:3, :3]
        for i, (pos, radius) in enumerate(zip(self.sphere_pos, self.sphere_radius)):
            new_pos = rot @ pos + mat[:3, 3]
            self.update_sphere(i, new_pos, radius)

    def update_sphere(self, index, pos, radius):
        self.sphere_pos[index] = pos
        self.sphere_radius[index] = radius
        if index >= len(self.sphere_visuals):
            raise ValueError(
                f"Sphere index {index} is out of range {len(self.sphere_visuals)}"
            )

        old_sphere_visual = self.sphere_visuals[index]
        self.entity.remove_component(old_sphere_visual)
        new_sphere_visual = self._create_sphere_visual(pos, radius)
        self.sphere_visuals[index] = new_sphere_visual
        if not self.enabled:
            new_sphere_visual.disable()

    def _create_sphere_visual(self, pos: list[float], radius: float):
        sphere_visual = RenderBodyComponent()
        sphere_visual.set_name("CollisionSphere")
        new_render_shape = sapien.render.RenderShapeSphere(radius, self.red_mat)
        new_render_shape.set_local_pose(sapien.Pose(pos))
        sphere_visual.attach(new_render_shape)
        self.entity.add_component(sphere_visual)
        return sphere_visual

    @property
    def enabled(self):
        return self._sphere_enabled

    @enabled.setter
    def enabled(self, value: bool):
        if value:
            self.enable()
        else:
            self.disable()

    def enable(self):
        if not self._sphere_enabled:
            for sphere_visual in self.sphere_visuals:
                sphere_visual.enable()
            self._sphere_enabled = True

    def disable(self):
        if self._sphere_enabled:
            for sphere_visual in self.sphere_visuals:
                sphere_visual.disable()
            self._sphere_enabled = False

    def paste_to(self, entity: sapien.Entity):
        components = find_all_components(entity, SphereGroupComponent)
        if len(components) > 0:
            component = components[0]
        else:
            component = SphereGroupComponent(entity)

        for i in range(len(self.sphere_pos)):
            component.add_sphere(
                pos=self.sphere_pos[i],
                radius=self.sphere_radius[i],
            )
        return component

    def clear(self):
        for sphere_visual in self.sphere_visuals:
            self.entity.remove_component(sphere_visual)
        self.sphere_pos = []
        self.sphere_radius = []
        self.sphere_visuals = []

    def to_dict(self):
        collision_spheres = []
        for sphere_pos, sphere_radius in zip(self.sphere_pos, self.sphere_radius):
            # Convert numpy values to native Python types
            pos = [float(x) for x in sphere_pos]
            radius = float(sphere_radius)

            collision_spheres.append(
                {
                    "type": "sphere",
                    "origin": pos,
                    "radius": radius,
                }
            )
        link_name = self.entity.get_name()
        collision_sphere_cfg = {link_name: collision_spheres}
        return collision_sphere_cfg


def test():
    import time

    from sapien.utils.viewer.viewer import Viewer

    scene = sapien.Scene()
    viewer = Viewer()
    scene.set_ambient_light([0.5, 0.5, 0.5])

    builder = scene.create_actor_builder()
    builder.add_capsule_visual(
        radius=0.2,
        half_length=0.5,
        material=sapien.render.RenderMaterial(base_color=[0.2, 0.2, 0.6, 1]),
    )
    actor = builder.build("capsule")

    collision_sphere_component = SphereGroupComponent(actor)

    collision_sphere_component.add_sphere(pos=[0, 0, 0.5], radius=0.2)

    viewer.set_scene(scene)

    tic = time.perf_counter()
    while time.perf_counter() - tic < 3.0:
        viewer.render()

    collision_sphere_component.update_sphere(0, pos=[0, 0, 0.5], radius=0.5)

    while time.perf_counter() - tic < 6.0:
        viewer.render()

    collision_sphere_component.remove_sphere(0)

    while time.perf_counter() - tic < 9.0:
        viewer.render()

    collision_sphere_component.add_sphere(pos=[0, 0.5, 0.0], radius=0.2)

    while time.perf_counter() - tic < 12.0:
        viewer.render()


if __name__ == "__main__":
    test()
