"""Visualization module for rendering robots using SAPIEN.

This module provides visualization capabilities for rendering and interacting with robot models
in a 3D environment using the SAPIEN physics engine. It handles scene setup, robot loading,
camera controls, and real-time visualization updates.
"""

import threading
import time
from pathlib import Path

import numpy as np
import sapien
from loguru import logger
from sapien.utils import Viewer
from sapien.utils.viewer.viewer import (
    ArticulationWindow,
    ControlWindow,
    EntityWindow,
    RenderOptionsWindow,
    SceneWindow,
    TransformWindow,
)

from dexmotion_viz.sapien_viz.entity.visual_robot import VisualRobot
from dexmotion_viz.sapien_viz.window.motion_planning_window import (
    MotionPlanningWindow,
)
# pylint: disable=no-member


class RobotVisualizer:
    """A class for visualizing robots using the SAPIEN physics engine.

    This class provides functionality to visualize and interact with
    robot models in a 3D environment using SAPIEN. It handles scene setup,
    robot loading, and visualization updates.

    Args:
        urdf_path (Path | str): Path to the URDF file describing the robot model.
    """

    def __init__(
        self,
        urdf_path: Path | str,
        enable_motion_plan: bool = False,
    ):
        self.urdf_path = urdf_path
        self.scene = None
        self.viewer = None
        self.enable_motion_plan = enable_motion_plan
        self._initialize_scene()

        self._physical_robot = self._add_physical_robot()
        if self.enable_motion_plan:
            self.motion_planning_window.set_robot(self._physical_robot)

        self._render_thread = None
        self._render_lock = threading.Lock()
        self._running = False

    def _add_physical_robot(
        self, color: np.ndarray | None = None
    ) -> sapien.physx.PhysxArticulation:
        """Add a new robot to the scene.

        Args:
            name (str): Unique identifier for the robot
            color (np.ndarray | None): RGBA color array for the robot.
                                     If None, uses original materials.
        """
        if self.scene is None:
            raise RuntimeError("Scene must be initialized before adding robots")

        loader = self.scene.create_urdf_loader()
        loader.fix_root_link = True
        loader.load_multiple_collisions_from_file = True

        robot = loader.load(str(self.urdf_path))

        if color is not None:
            for link in robot.get_links():
                for visual in link.entity.find_component_by_type(
                    sapien.render.RenderBodyComponent
                ).render_shapes:
                    mat = visual.material
                    mat.set_base_color(color)

        # Set robot initial pose
        robot.set_pose(sapien.Pose([0.0, 0.0, 0.0], [1.0, 0.0, 0.0, 0.0]))

        # Setup joint properties
        for joint in robot.get_active_joints():
            joint.set_drive_properties(10000, 500)

        return robot

    def _initialize_scene(self):
        """Initialize the SAPIEN scene with viewing setup."""
        self.scene = sapien.Scene()

        # Setup light
        self.scene.set_ambient_light(np.array([0.2, 0.2, 0.2]))
        self.scene.add_directional_light(
            np.array([1, 1, -1]), np.array([2, 2, 2]), shadow=False
        )
        # self.scene.add_point_light(
            # np.array([2, 2, 2]), np.array([1, 1, 1]), shadow=False
        # )
        # self.scene.add_point_light(
            # np.array([2, -2, 2]), np.array([1, 1, 1]), shadow=False
        # )

        # Setup ground
        render_mat = sapien.render.RenderMaterial()
        render_mat.base_color = [0.06, 0.08, 0.12, 1]
        render_mat.metallic = 0.0
        render_mat.roughness = 0.9
        render_mat.specular = 0.8
        self.scene.add_ground(-1.5, render_material=render_mat)

        # Setup viewer
        plugins = [
            TransformWindow(),
            RenderOptionsWindow(),
            ControlWindow(),
            SceneWindow(),
            EntityWindow(),
            ArticulationWindow(),
        ]
        if self.enable_motion_plan:
            self.motion_planning_window = MotionPlanningWindow()
            plugins.append(self.motion_planning_window)
        self.viewer = Viewer(plugins=plugins)
        self.viewer.set_scene(self.scene)
        self.viewer.set_camera_pose(
            sapien.Pose(
                [1.43346, 0.0135722, 0.772064],
                [0.00547725, 0.297903, 0.00167024, -0.954579],
            )
        )

        self.scene.set_environment_map(
            sapien.asset.create_dome_envmap(
                sky_color=[0.6, 0.6, 0.7],
                ground_color=[0.0, 0.0, 0.0],
                blend=0.0,
            )
        )

        logger.info("Sapien scene initialized successfully")

    def set_qpos(self, qpos: np.ndarray):
        """Update robot joint positions.

        Args:
            qpos (np.ndarray): Array of joint positions corresponding
                to the robot's degrees of freedom
            robot_name (str): Name of the robot to update
        """
        self._physical_robot.set_qpos(qpos)

    def set_joint_positions(self, joint_name_to_value_dict: dict[str, float]):
        """Set robot joint positions using a dictionary of joint names and values.

        Args:
            joint_name_to_value_dict (dict[str, float]): Dictionary mapping joint names
                to their desired positions
            robot_name (str): Name of the robot to update
        """
        sapien_qpos = np.zeros(int(self._physical_robot.dof))
        for i, active_joint in enumerate(self._physical_robot.get_active_joints()):
            joint_name = active_joint.get_name()
            if joint_name in joint_name_to_value_dict:
                sapien_qpos[i] = joint_name_to_value_dict[joint_name]
            else:
                logger.warning(
                    f"Joint {joint_name} not found in the Sapien robot model. Skipping..."
                )
        self.set_qpos(sapien_qpos)

    def render_loop(self):
        """Run the rendering loop."""
        while self._running and not self.viewer.closed:
            with self._render_lock:
                self.viewer.render()
            time.sleep(1 / 60)

    def start_rendering(self):
        """Start the rendering loop in a separate thread.

        Creates and starts a daemon thread that runs the render loop.
        """
        self._running = True
        self._render_thread = threading.Thread(target=self.render_loop, daemon=True)
        self._render_thread.start()
        logger.info("Sapien rendering loop started successfully")

    def stop_rendering(self):
        """Stop the rendering loop.

        Stops the rendering thread and waits for it to complete.
        """
        self._running = False
        if hasattr(self, "render_thread"):
            self._render_thread.join()

    def __del__(self):
        """Cleanup when the visualizer is destroyed.

        Ensures the rendering thread is properly stopped before object deletion.
        """
        self.stop_rendering()

    def update_motion_plan(
        self,
        motion_plan: np.ndarray,
        joint_names: list[str],
        duration: float,
        compute_time: float = 0.0,
    ):
        """Update the motion plan for the robot.

        Args:
            motion_plan (np.ndarray): The motion plan to update.
            joint_names (list[str]): The joint names to update.
            duration (float): The duration of the motion plan.
            compute_time (float): The compute time of the motion plan.
        """
        self.motion_planning_window.update_motion_plan(
            motion_plan, joint_names, duration, compute_time
        )

    def clear_motion_plan(self):
        self.motion_planning_window.clear_motion_plan()

    def create_visual_robot(self) -> VisualRobot:
        robot = VisualRobot(self._physical_robot, self.viewer.render_scene)
        robot.set_transparency(0.8)
        return robot
