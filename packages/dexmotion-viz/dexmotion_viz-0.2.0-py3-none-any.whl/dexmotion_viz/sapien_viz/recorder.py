import numpy as np
import sapien
from sapien.utils.viewer import Viewer
from sapien.utils.viewer.entity_window import EntityWindow
from sapien.utils.viewer.render_window import RenderOptionsWindow
from sapien.utils.viewer.scene_window import SceneWindow
from sapien.utils.viewer.transform_window import TransformWindow

from dexmotion_viz.sapien_viz.window.articulation_window import ArticulationWindow
from dexmotion_viz.sapien_viz.window.record_window import RecordControlWindow


class Recorder:
    def __init__(self, scene: sapien.Scene, offscreen: bool = False):
        self.offscreen = offscreen
        self.scene = scene
        self.physx = scene.get_physx_system()

        self.viewer: Viewer | None = None
        self.recorder: RecordControlWindow | None = None

    def get_state(self):
        data = dict(scene=self.scene.pack_poses(), physx=self.physx.pack())
        data["actor"] = {}
        data["articulation"] = {}
        for entity in self.scene.get_all_actors():
            data["actor"][entity.name] = entity.get_pose()

        for articulation in self.scene.get_all_articulations():
            data["articulation"][articulation.name] = (
                articulation.get_pose(),
                articulation.get_qpos(),
            )

        return data

    def set_state(self, data: dict[str, bytes]):
        self.scene.unpack_poses(data["scene"])
        self.physx.unpack(data["physx"])

    def setup_recording_viewer(self, filename, joint_names: list[str]) -> Viewer:
        recorder = RecordControlWindow(filename, self, joint_names)
        viewer = Viewer(
            plugins=[
                TransformWindow(),
                RenderOptionsWindow(),
                recorder,
                SceneWindow(),
                EntityWindow(),
                ArticulationWindow(),
            ]
        )
        viewer.set_scene(self.scene)
        self.viewer = viewer
        self.recorder = recorder
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
