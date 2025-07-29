import datetime
import pickle
from pathlib import Path

import sapien
from sapien import internal_renderer as R
from sapien.utils.viewer.plugin import Plugin

from dexmotion_viz.sapien_viz.struct.movie_state import (
    MovieState,
    ReplayState,
    WeldState,
    interpolate_movie_state,
)


class MovieWindow(Plugin):
    def __init__(
        self,
        data_path: Path,
        scene: sapien.Scene,
        joint_vel_limit: float = 1.5,
        joint_acc_limit: float = 5,
        trans_vel_limit: float = 5,
        trans_acc_limit: float = 30,
        rot_vel_limit: float = 6.28,
        rot_acc_limit: float = 30,
    ):
        super().__init__()
        self._interp_limits = {
            "joint_vel_limit": joint_vel_limit,
            "joint_acc_limit": joint_acc_limit,
            "trans_vel_limit": trans_vel_limit,
            "trans_acc_limit": trans_acc_limit,
            "rot_vel_limit": rot_vel_limit,
            "rot_acc_limit": rot_acc_limit,
        }
        self.ui_window = None
        self.data_path = data_path
        self.scene = scene
        self.physx: sapien.physx.PhysxCpuSystem = scene.get_physx_system()

        # Load data if exists
        self.selected_state_id = -1
        self._current_invisible_entities: set[sapien.Entity] = set()
        self._current_weld_states: set[WeldState] = set()
        self._selected_child_weld_entity: sapien.Entity | None = None
        self._selected_parent_weld_entity: sapien.Entity | None = None
        self._selected_weld_state: WeldState | None = None

        if not self.data_path.exists():
            print(f"File {self.data_path} does not exist, creating a new one.")
            self.data: list[MovieState] = []
            self.meta_data = {}
        else:
            try:
                self._load()
                if len(self.data) > 0:
                    self.selected_state_id = len(self.data) - 1
                    self.set_state(self.data[self.selected_state_id])
            except EOFError:
                print(f"Error loading {self.data_path}, creating a new one.")
                self.data: list[MovieState] = []
                self.meta_data = {}

        # Movie play states
        self._replay_states: list[ReplayState] = []
        self._replay_timestep = -1
        self._auto_loop = True
        self._loop_speed = 1

    def get_ui_windows(self):
        self.build()
        if self.ui_window:
            return [self.ui_window]
        return []

    def notify_selected_entity_change(self):
        for entity in self._current_invisible_entities:
            self.mark_entity_visibility(entity, False)

    def set_state(self, state: MovieState | ReplayState):
        for entity in self._current_invisible_entities.copy():
            self.mark_entity_visibility(entity, True)

        if isinstance(state, MovieState):
            self.scene.unpack_poses(state.scene)
            self.physx.unpack(state.physx)
            self._current_weld_states = state.weld_states.copy()
            state = state.to_replay_state()

        for entity, pose in state.actor.items():
            entity.set_pose(pose)

        for art, (pose, qpos) in state.articulation.items():
            art.set_pose(pose)
            art.set_qpos(qpos)

        for entity in state.invisible_entities:
            self.mark_entity_visibility(entity, False)

        for weld_state in state.weld_states:
            weld_state.child_entity.set_pose(
                weld_state.parent_entity.get_pose() * weld_state.pose
            )

    def get_state(self, timestep: int = 1) -> MovieState:
        actor_poses = {a: a.get_pose() for a in self.scene.get_all_actors()}
        articulation_poses = {
            a: (a.get_pose(), a.get_qpos()) for a in self.scene.get_all_articulations()
        }
        movie_state = MovieState(
            scene=self.scene.pack_poses(),
            physx=self.physx.pack(),
            actor=actor_poses,
            articulation=articulation_poses,
            timestep=timestep,
        )
        movie_state.invisible_entities = self._current_invisible_entities.copy()
        movie_state.weld_states = self._current_weld_states.copy()
        for weld_state in movie_state.weld_states:
            movie_state.actor[weld_state.child_entity] = (
                weld_state.parent_entity.get_pose() * weld_state.pose
            )

        return movie_state

    @property
    def num_states(self):
        return len(self.data)

    def build(self):
        if self.viewer.render_scene is None:
            self.ui_window = None
            return

        if self.ui_window is None:
            self.ui_window = (
                R.UIWindow().Pos(10, 10).Size(400, 400).Label("Movie Window")
            )
        else:
            self.ui_window.remove_children()

        num_states = self.num_states
        self.ui_window.append(R.UIDisplayText().Text(f"Num States: {num_states}"))

        selected_entity = self.viewer.selected_entity
        self.ui_window.append(
            R.UISameLine().append(
                R.UIButton()
                .Label("Play Movie")
                .Id("play_movie")
                .Callback(lambda p: self.play_movie()),
                R.UIButton()
                .Label("Stop Movie")
                .Id("clear")
                .Callback(lambda p: self.clear_movie()),
            ),
            R.UISameLine().append(
                R.UIButton().Label("Save").Id("save").Callback(lambda p: self.save()),
                R.UIButton()
                .Label("Add State")
                .Id("add")
                .Callback(lambda p: self.add_record()),
                R.UIButton()
                .Label("Remove State")
                .Id("remove")
                .Callback(lambda p: self.remove_record()),
            ),
        )

        # If movie is active, show the replay controls
        if len(self._replay_states) > 0:
            if self._auto_loop:
                increase = int(self._loop_speed)
            else:
                increase = 0

            self._replay_timestep = int(self._replay_timestep + increase) % len(
                self._replay_states
            )
            self.set_state(self._replay_states[self._replay_timestep])

            movie_section = R.UISection().Label("Movie")
            movie_section.append(
                R.UISameLine().append(
                    R.UISliderFloat()
                    .Min(0)
                    .Max(len(self._replay_states) - 1)
                    .Value(self._replay_timestep)
                    .Callback(
                        lambda slider: (
                            setattr(self, "_replay_timestep", slider.value),
                            setattr(self, "_auto_loop", False),
                        )
                    ),
                    R.UIDisplayText().Text(f"Step: {self._replay_timestep}"),
                ),
                R.UISameLine().append(
                    R.UISliderFloat()
                    .WidthRatio(0.5)
                    .Label("Loop speed")
                    .Min(1)
                    .Max(10)
                    .Value(self._loop_speed)
                    .Callback(lambda p: setattr(self, "_loop_speed", p.value)),
                    R.UICheckbox()
                    .Label("Auto Loop")
                    .Bind(self, "_auto_loop")
                    .Callback(lambda p: setattr(self, "_auto_loop", p.checked)),
                ),
            )
            self.ui_window.append(movie_section)
        else:
            if self.selected_state_id >= 0:
                current_state = self.data[self.selected_state_id]
                edit_section = R.UISection().Label("Edit")
                edit_section.append(
                    R.UISameLine().append(
                        R.UIInputInt()
                        .Value(current_state.timestep)
                        .Label("Timestep")
                        .Callback(
                            lambda p: setattr(current_state, "timestep", max(p.value, 1))
                        ),
                    ),
                    R.UISameLine().append(
                        R.UIButton()
                        .Label("Update")
                        .Id("update")
                        .Callback(lambda p: self.update_record()),
                        R.UIButton()
                        .Label("Move up")
                        .Id("move_up")
                        .Callback(lambda p: self.move_up(self.selected_state_id)),
                        R.UIButton()
                        .Label("Move down")
                        .Id("move_down")
                        .Callback(lambda p: self.move_down(self.selected_state_id)),
                    ),
                )

                # Show the tree of visible entities
                visible_entity_tree = R.UITreeNode().Label("Visible Entities")
                child = self._selected_child_weld_entity
                parent = self._selected_parent_weld_entity
                edit_section.append(
                    R.UIDummy().Height(10),
                    R.UISameLine().append(
                        R.UIButton()
                        .Label("Mark Invisible")
                        .Id("mark_invisible")
                        .Callback(
                            lambda p: self.mark_entity_visibility(
                                selected_entity, False
                            )
                        ),
                        R.UIButton()
                        .Label("Mark Visible")
                        .Id("mark_visible")
                        .Callback(
                            lambda p: self.mark_entity_visibility(selected_entity, True)
                        ),
                        R.UIDisplayText().Text(
                            f"Current timestep: {current_state.timestep}"
                        ),
                    ),
                    R.UIDummy().Height(10),
                    R.UISameLine().append(
                        R.UIButton()
                        .Label("Set Weld Child")
                        .Id("weld_child")
                        .Callback(
                            lambda p: setattr(
                                self, "_selected_child_weld_entity", selected_entity
                            )
                        ),
                        R.UIButton()
                        .Label("Set Weld Parent")
                        .Id("weld_parent")
                        .Callback(
                            lambda p: setattr(
                                self, "_selected_parent_weld_entity", selected_entity
                            )
                        ),
                        R.UIButton()
                        .Label("Weld")
                        .Id("weld")
                        .Callback(lambda p: self.weld_entity()),
                        R.UIButton()
                        .Label("Unweld")
                        .Id("unweld")
                        .Callback(lambda p: self.unweld_entity()),
                    ),
                    R.UISameLine().append(
                        R.UIDisplayText().Text(
                            f"Weld child: {child.name if child else 'None'}"
                        ),
                        R.UIDisplayText().Text(
                            f"Weld parent: {parent.name if parent else 'None'}"
                        ),
                    ),
                    R.UIDummy().Height(10),
                )
                for entity in current_state.invisible_entities:
                    if self.viewer.selected_entity == entity:
                        text = f"{entity.name} (selected)"
                    else:
                        text = f"{entity.name}"
                    visible_entity_tree.append(
                        R.UISelectable()
                        .Label(text)
                        .Id(f"{entity.name}_visible")
                        .Callback(
                            (lambda link: lambda _: self.viewer.select_entity(link))(
                                entity
                            )
                        )
                    )

                weld_state_tree = R.UITreeNode().Label("Weld States")
                for weld_state in current_state.weld_states:
                    if self._selected_weld_state == weld_state:
                        text = f"{weld_state.child_entity.name} -> {weld_state.parent_entity.name} (selected)"
                    else:
                        text = f"{weld_state.child_entity.name} -> {weld_state.parent_entity.name}"
                    weld_state_tree.append(
                        R.UISelectable()
                        .Label(text)
                        .Id(f"{weld_state.child_entity.name}_weld_state")
                        .Callback(
                            (
                                lambda weld_state: lambda _: setattr(
                                    self, "_selected_weld_state", weld_state
                                )
                            )(weld_state)
                        )
                    )

                # Show the tree of movie states
                state_tree = R.UITreeNode().Label("Movie States")
                edit_section.append(state_tree, weld_state_tree, visible_entity_tree)
                for i, state in enumerate(self.data):
                    if self.selected_state_id == i:
                        text = f"State {i} (selected)"
                    else:
                        text = f"State {i}"
                    state_tree.append(
                        R.UISelectable()
                        .Label(text)
                        .Id("state{}".format(i))
                        .Callback(
                            (
                                lambda state_id: lambda _: (
                                    setattr(self, "selected_state_id", state_id),
                                    self.set_state(self.data[state_id]),
                                )[0]
                            )(i)
                        )
                    )

                self.ui_window.append(edit_section)

    def before_render(self):
        for weld_state in self._current_weld_states:
            parent_pose = weld_state.parent_entity.get_pose()
            weld_state.child_entity.set_pose(parent_pose * weld_state.pose)

    def save(self):
        if len(self.data) < 2:
            print("Not enough states to save")
            return

        # Fill the meta data
        joint_info = {}
        for articulation in self.scene.get_all_articulations():
            joint_names = [j.name for j in articulation.get_active_joints()]
            joint_info[articulation.name] = joint_names
        self.meta_data["joint_info"] = joint_info

        data = [state.to_dict() for state in self.data]
        path = self.data_path
        # Remove existing timestamp if present
        stem = path.stem
        if len(stem.split("_")[-1]) == 11:
            stem = "_".join(stem.split("_")[:-1])
        timestamp = datetime.datetime.now().strftime("%m%d-%H%M%S")
        save_path = path.parent / f"{stem}_{timestamp}{path.suffix}"
        with save_path.open("wb") as f:
            replay = interpolate_movie_state(
                self.data,
                self._interp_limits["joint_vel_limit"],
                self._interp_limits["joint_acc_limit"],
                self._interp_limits["trans_vel_limit"],
                self._interp_limits["trans_acc_limit"],
                self._interp_limits["rot_vel_limit"],
                self._interp_limits["rot_acc_limit"],
            )
            replay = [state.to_dict() for state in replay]
            pickle.dump(
                {"data": data, "meta_data": self.meta_data, "replay": replay},
                f,
            )
        print(f"Save movie file {save_path}")

    def _load(self):
        with self.data_path.open("rb") as f:
            data = pickle.load(f)
            self.data = [
                MovieState.from_dict(state, self.scene) for state in data["data"]
            ]
            self.meta_data = data["meta_data"]

    def play_movie(self):
        if len(self.data) == 0:
            print("No movie data")
            return
        self._replay_states = interpolate_movie_state(
            self.data,
            self._interp_limits["joint_vel_limit"],
            self._interp_limits["joint_acc_limit"],
            self._interp_limits["trans_vel_limit"],
            self._interp_limits["trans_acc_limit"],
            self._interp_limits["rot_vel_limit"],
            self._interp_limits["rot_acc_limit"],
        )
        self._replay_timestep = self._replay_states[0].timestep

    def clear_movie(self):
        self._replay_states = []
        self._replay_timestep = -1

    def update_record(self):
        if self.selected_state_id >= 0:
            movie_state = self.get_state(
                timestep=self.data[self.selected_state_id].timestep
            )
            self.data[self.selected_state_id] = movie_state

    def add_record(self):
        movie_state = self.get_state()
        self.data.append(movie_state)
        self.selected_state_id = self.num_states - 1

    def remove_record(self):
        if self.selected_state_id >= 0:
            self.data.pop(self.selected_state_id)
            self.selected_state_id = max(self.selected_state_id - 1, 0)

    def move_up(self, current_state_id: int):
        if current_state_id > 0:
            self.data[current_state_id], self.data[current_state_id - 1] = (
                self.data[current_state_id - 1],
                self.data[current_state_id],
            )
            self.selected_state_id = current_state_id - 1
        else:
            print("Already at the first state")

    def move_down(self, current_state_id: int):
        if current_state_id < len(self.data) - 1:
            self.data[current_state_id], self.data[current_state_id + 1] = (
                self.data[current_state_id + 1],
                self.data[current_state_id],
            )
            self.selected_state_id = current_state_id + 1
        else:
            print("Already at the last state")

    def mark_entity_visibility(self, entity: sapien.Entity, visible: bool):
        if entity is None:
            return
        component: sapien.render.RenderBodyComponent = entity.find_component_by_type(
            sapien.render.RenderBodyComponent
        )
        if visible:
            component.visibility = 1.0
            if entity in self._current_invisible_entities:
                self._current_invisible_entities.remove(entity)
        else:
            component.visibility = 0.0
            self._current_invisible_entities.add(entity)

    def weld_entity(self):
        if (
            self._selected_child_weld_entity is None
            or self._selected_parent_weld_entity is None
        ):
            print("No child or parent weld entity selected")
            return

        for weld_state in self._current_weld_states:
            if weld_state.child_entity == self._selected_child_weld_entity:
                print("Already welded")
                return

        self._current_weld_states.add(
            WeldState(
                child_entity=self._selected_child_weld_entity,
                parent_entity=self._selected_parent_weld_entity,
                pose=self._selected_parent_weld_entity.pose.inv()
                * self._selected_child_weld_entity.pose,
            )
        )
        self._selected_child_weld_entity = None
        self._selected_parent_weld_entity = None

    def unweld_entity(self):
        if len(self._current_weld_states) == 0 or self._selected_weld_state is None:
            print("No weld states")
            return
        self._current_weld_states.remove(self._selected_weld_state)

    def close(self):
        self.save()
