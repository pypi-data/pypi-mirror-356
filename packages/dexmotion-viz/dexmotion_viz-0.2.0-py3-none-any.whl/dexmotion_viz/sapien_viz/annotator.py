from pathlib import Path

import numpy as np
import sapien
from sapien.utils import Viewer
from sapien.utils.viewer.viewer import (
    ArticulationWindow,
    ControlWindow,
    RenderOptionsWindow,
    SceneWindow,
    TransformWindow,
)

from dexmotion_viz.sapien_viz.component.collision_sphere_component import (
    SphereGroupComponent,
)
from dexmotion_viz.sapien_viz.window.collision_sphere_entity_window import (
    CollisionSphereEntityWindow,
)

DEFAULT_HEIGHT = 10


class SphereAnnotator:
    def __init__(
        self,
        urdf_path: Path | str,
    ):
        self.urdf_path = Path(urdf_path)
        self._initialize_scene()

    def _initialize_scene(self):
        """Initialize the SAPIEN scene with viewing setup."""
        self.scene = sapien.Scene()

        # Setup light
        self.scene.set_ambient_light(np.array([0.6, 0.6, 0.6]))
        self.scene.add_directional_light(np.array([1, 1, -1]), np.array([1, 1, 1]))
        self.scene.add_point_light(
            np.array([2, 2, 2]), np.array([1, 1, 1]), shadow=False
        )
        self.scene.add_point_light(
            np.array([2, -2, 2]), np.array([1, 1, 1]), shadow=False
        )

        # Setup ground
        render_mat = sapien.render.RenderMaterial()
        render_mat.base_color = [0.06, 0.08, 0.12, 1]
        render_mat.metallic = 0.0
        render_mat.roughness = 0.9
        render_mat.specular = 0.8
        self.scene.add_ground(DEFAULT_HEIGHT, render_material=render_mat)

        # Setup viewer
        plugins = [
            TransformWindow(),
            RenderOptionsWindow(),
            ControlWindow(),
            SceneWindow(),
            ArticulationWindow(),
        ]
        self.collision_sphere_window = CollisionSphereEntityWindow()
        plugins.append(self.collision_sphere_window)
        self.viewer = Viewer(plugins=plugins)
        self.viewer.set_scene(self.scene)
        self.viewer.set_camera_pose(
            sapien.Pose(
                [1.43346, 0.0135722, 0.772064 + DEFAULT_HEIGHT],
                [0.00547725, 0.297903, 0.00167024, -0.954579],
            )
        )
        self.viewer.control_window.move_speed = 0.01

    def load_robot(
        self,
        srdf_path: Path | None = None,
        collision_spheres_cfg: list[dict[str, float, str, list[float]]] = [],
    ) -> sapien.physx.PhysxArticulation:
        loader = self.scene.create_urdf_loader()
        robot = loader.load(str(self.urdf_path), srdf_path)
        config_path = self.urdf_path.parent / "configs"
        config_path.mkdir(exist_ok=True)
        self.collision_sphere_window.set_save_path(
            config_path / f"{self.urdf_path.stem}_collision_spheres.yml"
        )

        robot.set_name(self.urdf_path.stem)
        link_name_to_link = {link.name: link for link in robot.links}
        robot.set_qpos(np.zeros(robot.dof))
        robot.set_pose(sapien.Pose(p=[0, 0, DEFAULT_HEIGHT]))

        for link_name, collision_spheres in collision_spheres_cfg.items():
            if link_name == "source_urdf":
                continue
            link = link_name_to_link[link_name].entity
            sphere_component = SphereGroupComponent(link)
            for sphere in collision_spheres:
                assert sphere["type"] in ["sphere"]
                sphere_component.add_sphere(sphere["origin"], sphere["radius"])

        return robot

    def run(self):
        while not self.viewer.closed:
            self.viewer.render()
