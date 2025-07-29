from typing import cast

import numpy as np
import sapien
from sapien import internal_renderer as R


class VisualRobot:
    def __init__(self, robot: sapien.physx.PhysxArticulation, render_scene: R.Scene):
        self.robot = robot
        self.pinocchio_model = robot.create_pinocchio_model()
        self.render_scene = render_scene
        self._qpos = self.robot.get_qpos()
        self._joint_names = [j.name for j in self.robot.get_active_joints()]

        self._visual_links = self._clone_from_robot()

    def set_qpos(self, qpos: np.ndarray):
        self.pinocchio_model.compute_forward_kinematics(qpos)
        self._qpos = qpos
        for idx, obj in self._visual_links.items():
            pose = self.robot.pose * self.pinocchio_model.get_link_pose(idx)
            obj.set_position(pose.p)
            obj.set_rotation(pose.q)

    def set_joint_positions(self, joint_name_to_value_dict: dict[str, float]):
        for joint_name, value in joint_name_to_value_dict.items():
            idx = self._joint_names.index(joint_name)
            self._qpos[idx] = value
        self.set_qpos(self._qpos)

    def _clone_from_robot(self) -> dict[int, R.Node]:
        robot_visuals = {}
        for link_index, link in enumerate(self.robot.get_links()):
            visual = link.entity.find_component_by_type(
                sapien.render.RenderBodyComponent
            )
            if visual is not None:
                link_node = self.render_scene.add_node()
                render_node = visual._internal_node
                for obj in render_node.children:
                    obj = cast(R.Object, obj)
                    new_obj = self.render_scene.add_object(obj.model, link_node)
                    new_obj.set_position(obj.position)
                    new_obj.set_rotation(obj.rotation)
                    new_obj.set_scale(obj.scale)
                    new_obj.transparency = 1

                link_node.set_position(link.entity_pose.p)
                link_node.set_rotation(link.entity_pose.q)
                robot_visuals[link_index] = link_node

        return robot_visuals

    def set_transparency(self, transparency: float):
        for obj in self._visual_links.values():
            for child in obj.children:
                child = cast(R.Object, child)
                child.transparency = transparency

    def clear(self):
        for obj in self._visual_links.values():
            self.render_scene.remove_node(obj)

        self._visual_links.clear()
        self.pinocchio_model = None
        self.robot = None

    def __del__(self):
        self.clear()
