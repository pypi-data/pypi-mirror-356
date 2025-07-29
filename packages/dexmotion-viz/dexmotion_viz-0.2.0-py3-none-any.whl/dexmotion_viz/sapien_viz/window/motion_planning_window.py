import numpy as np
import sapien
from loguru import logger
from sapien import internal_renderer as R
from sapien.utils.viewer.plugin import Plugin

from dexmotion_viz.sapien_viz.entity.visual_robot import VisualRobot
from dexmotion_viz.sapien_viz.sapien_utils import (
    get_articulation_joint_indices,
)

DEFAULT_MONITOR_REFRESH_RATE = 60


class MotionPlanningWindow(Plugin):
    ui_window: R.UIWindow

    # Ghost objects
    # visual_hands: dict[str, R.Node | None] = dict(left=None, right=None)
    # ee2hand = dict(left=sapien.Pose(), right=sapien.Pose())

    def __init__(self):
        self.robot: sapien.Articulation = None

        # UI state
        self._visual_transparency = 0.7
        self._is_visual_hidden = True
        self._auto_loop = True
        self._loop_speed = 1
        self._show_target_robot = True

        # Motion planning state
        self._mp_planning_robot: VisualRobot | None = None
        self._mp_target_robot: VisualRobot | None = None
        self._mp_trajectory: tuple[list[str], np.ndarray] = ([], np.array([]))
        self._mp_compute_time: float = 0.0
        self._mp_duration: float = 0
        self._mp_percentage: float = 0

    # -------------------------------------------------------------------------- #
    # API functions
    # -------------------------------------------------------------------------- #


    def set_robot(self, robot: sapien.physx.PhysxArticulation):
        self.robot = robot
        self._mp_target_robot = VisualRobot(self.robot, self.viewer.render_scene)
        self._mp_planning_robot = VisualRobot(self.robot, self.viewer.render_scene)

    def update_motion_plan(
        self,
        trajectory: np.ndarray,
        joint_names: list[str],
        duration: float,
        compute_time: float = 0.0,
    ):
        if self.robot is None:
            logger.error("No robot is set, please call set_robot first.")
            return

        self._mp_trajectory = (joint_names, trajectory)
        self._mp_duration = duration
        self._mp_compute_time = compute_time

        mp_qpos = self._mp_trajectory[1][-1]
        qpos = self.robot.get_qpos()
        joint_indices = get_articulation_joint_indices(
            self.robot, self._mp_trajectory[0]
        )
        qpos[joint_indices] = mp_qpos
        self._mp_target_robot.set_qpos(qpos)
        self.show_visual_robots(["arm"])

    def clear_motion_plan(self):
        self._mp_duration = 0
        self._mp_trajectory = ([], np.array([]))
        self._mp_compute_time = 0
        self._mp_percentage = 0
        self.hide_visual_robots(["arm"])

    # -------------------------------------------------------------------------- #
    # Core render functions
    # -------------------------------------------------------------------------- #
    def _build_motion_planning_ui(self):
        mp_activated = len(self._mp_trajectory[0]) > 0
        if not mp_activated:
            self.ui_window.append(
                R.UIDisplayText().Text("No active motion plan monitored.")
            )
            self.hide_visual_robots(entity_types=["arm"])
            return
        else:
            self.show_visual_robots(entity_types=["arm"])

        self._update_planning_visual()

        if mp_activated:
            motion_section = (
                R.UISection()
                .Label("Motion Planning")
                .Id("Motion Section")
                .Expanded(True)
            )
            length = self._mp_trajectory[1].shape[0]
            index = np.clip(int(self._mp_percentage * length), 0, length - 1)
            motion_section.append(
                R.UIDisplayText().Text(
                    f"Trajectory length: {length}, duration: {self._mp_duration:.2f}s,"
                    f"compute time: {self._mp_compute_time:.2f}s"
                ),
                R.UISameLine().append(
                    R.UISliderFloat()
                    .WidthRatio(0.5)
                    .Min(0)
                    .Max(1)
                    .Value(self._mp_percentage)
                    .Callback(
                        lambda slider: (
                            setattr(self, "_mp_percentage", slider.value),
                            setattr(self, "_auto_loop", False),
                        )
                    ),
                    R.UIDisplayText().Text(f"Step: {index}"),
                ),
                R.UISliderFloat()
                .WidthRatio(0.5)
                .Label(" Loop speed")
                .Min(0.1)
                .Max(10)
                .Value(self._loop_speed)
                .Callback(lambda p: setattr(self, "_loop_speed", p.value)),
                R.UISliderFloat()
                .WidthRatio(0.5)
                .Label(" Transparency")
                .Min(0)
                .Max(1)
                .Value(self._visual_transparency)
                .Bind(self, "visual_transparency"),
                R.UISameLine().append(
                    R.UICheckbox().Label("Auto Loop").Bind(self, "_auto_loop"),
                    R.UICheckbox()
                    .Label("Show Target")
                    .Bind(self, "_show_target_robot")
                    .Callback(
                        lambda p: self._mp_target_robot.set_transparency(
                            self.visual_transparency if p.checked else 1
                        )
                    ),
                ),
            )
            self.ui_window.append(motion_section)

    def build(self):
        if self.scene is None:
            self.ui_window = None
            return

        # Build window
        if not hasattr(self, "ui_window") or self.ui_window is None:
            self.ui_window = (
                R.UIWindow().Pos(10, 10).Size(400, 400).Label("Motion Planning")
            )
        else:
            self.ui_window.remove_children()

        self._build_motion_planning_ui()

    @property
    def visual_transparency(self):
        return self._visual_transparency

    @visual_transparency.setter
    def visual_transparency(self, v):
        self.viewer.notify_render_update()
        self._visual_transparency = v

        if self._mp_planning_robot is not None:
            self._mp_planning_robot.set_transparency(v)
        if self._mp_target_robot is not None and self._show_target_robot:
            self._mp_target_robot.set_transparency(v)

    def _update_planning_visual(self):
        # Update the motion planning percentage
        if self._auto_loop:
            length = self._mp_trajectory[1].shape[0]
            percentage_per_refresh = (
                1 / self._mp_duration / DEFAULT_MONITOR_REFRESH_RATE * self._loop_speed
            )
            self._mp_percentage += percentage_per_refresh
            self._mp_percentage = self._mp_percentage % 1

        # Unhide the motion planning visual
        if self._is_visual_hidden:
            self._is_visual_hidden = False
            self._mp_planning_robot.set_transparency(self._visual_transparency)

        trajectory = self._mp_trajectory[1]
        length = trajectory.shape[0]
        mp_qpos = trajectory[np.clip(int(self._mp_percentage * length), 0, length - 1)]
        qpos = self.robot.get_qpos()
        joint_indices = get_articulation_joint_indices(
            self.robot, self._mp_trajectory[0]
        )
        qpos[joint_indices] = mp_qpos
        self._mp_planning_robot.set_qpos(qpos)
        self.viewer.notify_render_update()

    # -------------------------------------------------------------------------- #
    # Convenient functions
    # -------------------------------------------------------------------------- #
    def get_ui_windows(self):
        self.build()
        if self.ui_window:
            return [self.ui_window]
        return []

    def hide_visual_robots(self, entity_types: list[str] = ["hand", "arm"]):
        if "hand" in entity_types:
            raise NotImplementedError("Hand is not supported yet.")

        if self._is_visual_hidden:
            return
        self._is_visual_hidden = True
        if self._mp_planning_robot is not None:
            self._mp_planning_robot.set_transparency(1)
            self._mp_target_robot.set_transparency(1)

    def show_visual_robots(self, entity_types: list[str] = ["hand", "arm"]):
        if "hand" in entity_types:
            raise NotImplementedError("Hand is not supported yet.")

        if not self._is_visual_hidden:
            return
        self._is_visual_hidden = False
        if self._mp_planning_robot is not None:
            self._mp_planning_robot.set_transparency(self._visual_transparency)
            if self._show_target_robot:
                self._mp_target_robot.set_transparency(self._visual_transparency)

    @property
    def scene(self) -> sapien.Scene:
        return self.viewer.scene

    @property
    def renderer_context(self):
        return self.viewer.renderer_context

    @property
    def selected_entity(self) -> sapien.Entity:
        return self.viewer.selected_entity

    # -------------------------------------------------------------------------- #
    # Task stage functions
    # -------------------------------------------------------------------------- #
    # def execute_motion_plan(self):
    #     if not hasattr(self, "_mp_activated_sides") or not self._mp_activated_sides:
    #         logger.warning("No motion plan is activated.")
    #         return

    #     trajectories = {}
    #     for side in self.controlled_sides:
    #         if side not in self.mp_trajectory:
    #             logger.warning(f"Side {side} is not in the motion plan.")
    #             continue
    #         trajectories[side] = self.mp_trajectory[side]

    #     if len(trajectories) > 0:
    #         self.robot_wrapper.follow_arm_hand_trajectory(trajectories)
    #     self.clear_motion_plan()
