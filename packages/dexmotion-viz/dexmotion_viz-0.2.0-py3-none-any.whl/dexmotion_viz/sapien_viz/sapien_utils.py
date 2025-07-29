from typing import TypeVar

import numpy as np
import sapien

TypeComponent = TypeVar("TypeComponent", bound=sapien.Component)


def fetch_subtree_links(robot: sapien.physx.PhysxArticulation, root_link_name: str):
    all_joints = robot.get_joints()
    root_link = robot.find_link_by_name(root_link_name)
    subtree_links = [root_link]

    for joint in all_joints:
        if joint.parent_link == root_link:
            subtree_links.extend(fetch_subtree_links(robot, joint.child_link.name))

    return subtree_links


def get_articulation_link_indices(
    robot: sapien.physx.PhysxArticulation, link_names: list[str]
) -> np.ndarray:
    all_link_names = [link.name for link in robot.get_links()]
    return np.array([all_link_names.index(name) for name in link_names])


def get_articulation_joint_indices(
    robot: sapien.physx.PhysxArticulation, joint_names: list[str]
) -> np.ndarray:
    all_joint_names = [joint.name for joint in robot.get_active_joints()]
    return np.array([all_joint_names.index(name) for name in joint_names])


def generate_box_lines():
    corners = (
        np.array(
            [
                [-1, -1, -1],
                [1, -1, -1],
                [1, 1, -1],
                [-1, 1, -1],
                [-1, -1, 1],
                [1, -1, 1],
                [1, 1, 1],
                [-1, 1, 1],
            ]
        )
        * 0.5
    )

    # fmt: off
    lines = np.array([
        0, 1, 1, 2, 2, 3, 3, 0,  # Bottom face
        4, 5, 5, 6, 6, 7, 7, 4,  # Top face
        0, 4, 1, 5, 2, 6, 3, 7   # Connecting lines
    ])
    # fmt: on

    return corners[lines].reshape(-1)


def find_all_components(
    entity: sapien.Entity | None, component_type: type[TypeComponent]
) -> list[TypeComponent]:
    if entity is None:
        return []

    components = []
    for c in entity.components:
        if isinstance(c, component_type):
            components.append(c)
    return components
