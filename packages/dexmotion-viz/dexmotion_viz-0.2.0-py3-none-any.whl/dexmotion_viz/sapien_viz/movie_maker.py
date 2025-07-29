from pathlib import Path

import numpy as np
import sapien
from sapien.utils.viewer import Viewer
from sapien.utils.viewer.control_window import ControlWindow
from sapien.utils.viewer.entity_window import EntityWindow
from sapien.utils.viewer.render_window import RenderOptionsWindow
from sapien.utils.viewer.scene_window import SceneWindow
from sapien.utils.viewer.transform_window import TransformWindow

from dexmotion_viz.sapien_viz.window.articulation_window import ArticulationWindow
from dexmotion_viz.sapien_viz.window.movie_window import MovieWindow


class MovieMaker:
    def __init__(self, scene: sapien.Scene, offscreen: bool = False):
        self.offscreen = offscreen
        self.scene = scene

        self.viewer: Viewer | None = None
        self.movie_window: MovieWindow | None = None

    def setup_movie_viewer(
        self,
        file_path: Path,
        joint_vel_limit: float = 1.5,
        joint_acc_limit: float = 5,
        trans_vel_limit: float = 5,
        trans_acc_limit: float = 30,
        rot_vel_limit: float = 6.28,
        rot_acc_limit: float = 30,
    ) -> Viewer:
        movie_window = MovieWindow(
            file_path,
            self.scene,
            joint_vel_limit,
            joint_acc_limit,
            trans_vel_limit,
            trans_acc_limit,
            rot_vel_limit,
            rot_acc_limit,
        )
        viewer = Viewer(
            plugins=[
                TransformWindow(),
                RenderOptionsWindow(),
                movie_window,
                SceneWindow(),
                EntityWindow(),
                ArticulationWindow(),
                ControlWindow(),
            ]
        )
        viewer.set_scene(self.scene)
        self.viewer = viewer
        self.movie_window = movie_window
        return viewer

    def render(self, cams: list[sapien.render.RenderCameraComponent] | None = None):
        self.scene.update_render()
        data = {}
        if not self.offscreen:
            self.viewer.render()
        if cams is not None:
            for cam in cams:
                cam.take_picture()
                rgba = cam.get_picture("Color")
                if rgba.dtype == np.uint8:
                    data[cam.entity.name] = rgba[..., :3]
                else:
                    rgb_array = (rgba[..., :3] * 255).clip(0, 255).astype("uint8")
                    data[cam.entity.name] = rgb_array
        return data

    def run(self):
        while not self.viewer.closed:
            self.scene.update_render()
            self.viewer.render()
