from dataclasses import dataclass, field

import numpy as np
import sapien

from dexmotion_viz.utils.motion_utils import (
    smooth_interpolate_pose,
    smooth_interpolation_pos,
)


@dataclass
class WeldState:
    child_entity: sapien.Entity
    parent_entity: sapien.Entity
    pose: sapien.Pose

    def __hash__(self) -> int:
        return hash(
            (
                self.child_entity.name,
                self.parent_entity.name,
                tuple(self.pose.p),
                tuple(self.pose.q),
            )
        )

    def to_dict(self) -> dict:
        return {
            "child_entity": self.child_entity.name,
            "parent_entity": self.parent_entity.name,
            "pose": (self.pose.p, self.pose.q),
        }

    @classmethod
    def from_dict(cls, data: dict, scene: sapien.Scene) -> "WeldState":
        entities = scene.get_entities()
        articulation_entities = [
            l.entity for a in scene.get_all_articulations() for l in a.get_links()
        ]
        entities.extend(articulation_entities)
        for entity in entities:
            if entity.name == data["child_entity"]:
                child_entity = entity
            if entity.name == data["parent_entity"]:
                parent_entity = entity
        pose = sapien.Pose(data["pose"][0], data["pose"][1])
        return cls(child_entity, parent_entity, pose)


@dataclass
class ReplayState:
    actor: dict[sapien.Entity, sapien.Pose]
    articulation: dict[sapien.physx.PhysxArticulation, tuple[sapien.Pose, np.ndarray]]
    invisible_entities: set[sapien.Entity] = field(default_factory=set)
    weld_states: set[WeldState] = field(default_factory=set)
    timestep: int = 0

    def to_dict(self) -> dict:
        return {
            "actor": {k.name: (v.p, v.q) for k, v in self.actor.items()},
            "articulation": {
                k.name: ((v[0].p, v[0].q), v[1]) for k, v in self.articulation.items()
            },
            "invisible_entities": [e.name for e in self.invisible_entities],
            "weld_states": [w.to_dict() for w in self.weld_states],
            "timestep": self.timestep,
        }

    @classmethod
    def from_dict(cls, data: dict, scene: sapien.Scene) -> "ReplayState":
        all_actors = {a.name: a for a in scene.get_all_actors()}
        all_articulations = {a.name: a for a in scene.get_all_articulations()}
        state = cls(
            actor={
                all_actors[k]: sapien.Pose(data["actor"][k][0], data["actor"][k][1])
                for k in data["actor"]
            },
            articulation={
                all_articulations[k]: (
                    sapien.Pose(
                        data["articulation"][k][0][0], data["articulation"][k][0][1]
                    ),
                    data["articulation"][k][1],
                )
                for k in data["articulation"]
            },
            invisible_entities=set(all_actors[k] for k in data["invisible_entities"]),
            weld_states={WeldState.from_dict(w, scene) for w in data["weld_states"]},
            timestep=data["timestep"],
        )
        return state

    def unpack(self):
        for actor in self.actor:
            actor.set_pose(self.actor[actor])
        for art in self.articulation:
            art.set_pose(self.articulation[art][0])
            art.set_qpos(self.articulation[art][1])

        # TODO: set visible for True
        for entity in self.invisible_entities:
            entity.set_visible(False)

        for weld in self.weld_states:
            weld.child_entity.set_pose(weld.parent_entity.get_pose() * weld.pose)


@dataclass
class MovieState:
    scene: bytes
    physx: bytes
    actor: dict[sapien.Entity, sapien.Pose]
    articulation: dict[sapien.physx.PhysxArticulation, tuple[sapien.Pose, np.ndarray]]
    timestep: int = 1
    invisible_entities: set[sapien.Entity] = field(default_factory=set)
    weld_states: set[WeldState] = field(default_factory=set)

    def to_dict(self) -> dict:
        data = self.to_replay_state().to_dict()
        data["scene"] = self.scene
        data["physx"] = self.physx
        return data

    def to_replay_state(self) -> ReplayState:
        return ReplayState(
            actor=self.actor,
            articulation=self.articulation,
            invisible_entities=self.invisible_entities,
            weld_states=self.weld_states,
            timestep=self.timestep,
        )

    @classmethod
    def from_dict(cls, data: dict, scene: sapien.Scene) -> "MovieState":
        replay_state = ReplayState.from_dict(data, scene)
        state = cls(
            scene=data["scene"],
            physx=data["physx"],
            **replay_state.__dict__,
        )

        return state


def interpolate_movie_state(
    movie_states: list[MovieState],
    joint_vel_limit: float,
    joint_acc_limit: float,
    trans_vel_limit: float,
    trans_acc_limit: float,
    rot_vel_limit: float,
    rot_acc_limit: float,
) -> list[ReplayState]:
    first_state = movie_states[0]
    time_steps = []
    actor_pose = {a: [] for a in first_state.actor}
    art_pose = {a: [] for a in first_state.articulation}
    art_qpos = {a: [] for a in first_state.articulation}
    last_time_step = 0
    invisible_entities = []
    weld_states = []

    for state in movie_states:
        last_time_step += state.timestep
        time_steps.append(last_time_step)
        invisible_entities.append(state.invisible_entities)
        weld_states.append(state.weld_states)
        for actor, _ in first_state.actor.items():
            if actor not in state.actor:
                raise ValueError(f"Actor {actor} not found in state {state}")
            actor_pose[actor].append(state.actor[actor])
        for art, (pose, qpos) in first_state.articulation.items():
            if art not in state.articulation:
                raise ValueError(f"Articulation {art} not found in state {state}")
            art_pose[art].append(state.articulation[art][0])
            art_qpos[art].append(state.articulation[art][1])

    final_actor_pose = {}
    final_art_pose = {}
    final_art_qpos = {}
    for actor, poses in actor_pose.items():
        final_actor_pose[actor] = smooth_interpolate_pose(
            poses,
            time_steps,
            trans_vel_limit,
            trans_acc_limit,
            rot_vel_limit,
            rot_acc_limit,
        )
    for art, poses in art_pose.items():
        final_art_pose[art] = smooth_interpolate_pose(poses, time_steps)
    for art, qposes in art_qpos.items():
        final_art_qpos[art] = smooth_interpolation_pos(
            qposes, time_steps, vel_limit=joint_vel_limit, acc_limit=joint_acc_limit
        )

    replay_states = []
    for i in range(time_steps[-1] - time_steps[0] + 1):
        corresponding_index = (
            np.searchsorted(np.array(time_steps) + time_steps[0], i, side="right") - 1
        )

        current_actors = {}
        current_articulations = {}

        for actor in actor_pose:
            current_actors[actor] = final_actor_pose[actor][i]

        for art in art_pose:
            current_articulations[art] = (
                final_art_pose[art][i],
                final_art_qpos[art][i],
            )

        replay_state = ReplayState(
            actor=current_actors,
            articulation=current_articulations,
            invisible_entities=invisible_entities[corresponding_index],
            weld_states=weld_states[corresponding_index],
            timestep=i + time_steps[0],
        )

        replay_states.append(replay_state)

    return replay_states
