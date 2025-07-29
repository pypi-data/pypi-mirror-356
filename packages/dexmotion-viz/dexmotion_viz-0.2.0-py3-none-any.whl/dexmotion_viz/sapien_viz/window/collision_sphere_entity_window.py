import time
from pathlib import Path

import numpy as np
import sapien
import yaml
from sapien import internal_renderer as R
from sapien.utils.viewer.plugin import Plugin
from sapien.utils.viewer.viewer import Viewer

from dexmotion_viz.sapien_viz.component.collision_sphere_component import (
    SphereGroupComponent,
)
from dexmotion_viz.sapien_viz.sapien_utils import find_all_components


class CollisionSphereEntityWindow(Plugin):
    def __init__(self):
        self.ui_window = None
        self.copied_sphere: SphereGroupComponent | None = None
        self.save_path = Path("./saved_collision_spheres.yml")

        self.selected_sphere: tuple[SphereGroupComponent | None, int] = (
            None,
            -1,
        )
        self.selected_articulation: sapien.physx.PhysxArticulation | None = None
        self.selected_sphere_node: R.Node | None = None
        self.gizmo: R.UIGizmo | None = None
        self._gizmo_pose = sapien.Pose()

        # Link rotation
        self._rotation_to_apply = np.zeros(3)
        self._translation_to_apply = np.zeros(3)

    def init(self, viewer: Viewer):
        self.viewer = viewer
        self.selected_sphere_mat = self.viewer.renderer_context.create_material(
            emission=[0, 0, 0, 1],
            base_color=[0.2, 0.6, 0.2, 0.7],
            specular=0.7,
            roughness=0.3,
            metallic=0.2,
        )

    def close(self):
        self.ui_window = None

    @property
    def selected_entity(self):
        return self.viewer.selected_entity

    def _handle_click(self):
        window = self.viewer.window
        if window.mouse_click(2):
            mx, my = window.mouse_position
            ww, wh = window.size
            if mx < 0 or my < 0 or mx >= ww or my >= wh:
                return
            tw, th = window.get_picture_size("Segmentation")
            mx = mx * tw / ww
            my = my * th / wh

            pixel = window.get_picture_pixel("Segmentation", int(mx), int(my))
            render_body_id = pixel[0]
            entity_id = pixel[1]
            entity = self.find_entity_by_id(entity_id)
            self.viewer.select_entity(entity)

            self.select_sphere_by_id(render_body_id)

    def find_entity_by_id(self, entity_id) -> sapien.Entity | None:
        scene = self.viewer.scene
        for entity in scene.entities:
            if entity.per_scene_id == entity_id:
                return entity

        return None

    def select_sphere_by_id(
        self, render_body_id
    ) -> tuple[int, SphereGroupComponent | None]:
        entity = self.selected_entity
        if entity is None:
            return

        # Each render body component has only one render shape
        components = find_all_components(entity, SphereGroupComponent)
        if len(components) == 1:
            collision_sphere = components[0]
        else:
            return

        print(render_body_id)
        for c in entity.components:
            if isinstance(c, sapien.render.RenderBodyComponent):
                if (
                    c.render_shapes[0].per_scene_id == render_body_id
                    and c in collision_sphere.sphere_visuals
                ):
                    index = collision_sphere.sphere_visuals.index(c)
                    self.select_sphere(collision_sphere, index)
                    break

    def select_sphere(self, collision_sphere: SphereGroupComponent, index: int):
        # If the selected sphere is the same as the current sphere, skip
        if (
            self.selected_sphere[0] == collision_sphere
            and self.selected_sphere[1] == index
        ):
            return

        # Otherwise, disable the visual of the previous selected sphere
        render_scene = self.viewer.render_scene
        context = self.viewer.renderer_context
        if self.selected_sphere[0] is not None:
            self.unselected_sphere_node()

        entity = collision_sphere.entity
        self.viewer.select_entity(entity)

        # Then create new visual for the selected sphere
        self.selected_sphere = (collision_sphere, index)
        collision_sphere.sphere_visuals[index].disable()
        link_node = render_scene.add_node()
        link_node.set_position(entity.pose.p)
        link_node.set_rotation(entity.pose.q)
        sphere_mesh = context.create_uvsphere_mesh(segments=32, half_rings=16)
        sphere_model = context.create_model(
            [sphere_mesh],
            [self.selected_sphere_mat],
        )
        sphere_node = render_scene.add_object(sphere_model, link_node)
        sphere_node.set_position(collision_sphere.sphere_pos[index])
        sphere_node.set_scale([collision_sphere.sphere_radius[index]] * 3)

        self.gizmo = R.UIGizmo().Bind(self, "gizmo_matrix")
        self.selected_sphere_node = link_node

    def after_render(self):
        self._handle_click()

    def unselected_sphere_node(self, update_sphere=True):
        if self.selected_sphere_node is not None:
            sphere_group, index = self.selected_sphere
            child_node = self.selected_sphere_node.children[0]
            self.viewer.render_scene.remove_node(self.selected_sphere_node)
            self.selected_sphere_node = None
            self.selected_sphere = (None, -1)

            # Save the modified sphere
            if update_sphere:
                sphere_group.sphere_pos[index] = child_node.position
                sphere_group.sphere_radius[index] = child_node.scale[0]
                sphere_group.update_sphere(
                    index, child_node.position, child_node.scale[0]
                )

            self.gizmo = None

    def notify_selected_entity_change(self):
        articulation = None
        if self.selected_entity:
            for c in self.selected_entity.components:
                if isinstance(c, sapien.physx.PhysxArticulationLinkComponent):
                    articulation = c.articulation
                    break

        self.selected_articulation = articulation
        self._rotation_to_apply = np.zeros(3)
        self._translation_to_apply = np.zeros(3)
        self.unselected_sphere_node()

    def switch_sphere(self, enable: bool):
        components = find_all_components(self.selected_entity, SphereGroupComponent)
        for c in components:
            c.enable() if enable else c.disable()
        self.viewer.notify_render_update()

    def switch_visual(self, enable: bool):
        components = find_all_components(
            self.selected_entity, sapien.render.RenderBodyComponent
        )
        for c in components:
            if c.name != "CollisionSphere":
                c.enable() if enable else c.disable()
        self.viewer.notify_render_update()

    def switch_robot_sphere(self, enable: bool):
        if self.selected_articulation is None:
            return

        for link in self.selected_articulation.links:
            components = find_all_components(link.entity, SphereGroupComponent)
            if len(components) == 1:
                components[0].enable() if enable else components[0].disable()
        self.viewer.notify_render_update()

    def switch_robot_visual(self, enable: bool):
        if self.selected_articulation is None:
            return

        for link in self.selected_articulation.links:
            components = find_all_components(
                link.entity, sapien.render.RenderBodyComponent
            )
            for c in components:
                if c.name != "CollisionSphere":
                    c.enable() if enable else c.disable()
        self.viewer.notify_render_update()

    def copy_spheres(self):
        components = find_all_components(self.selected_entity, SphereGroupComponent)
        if len(components) == 1:
            self.copied_sphere = components[0]
        elif len(components) > 1:
            raise ValueError("Only one collision sphere component is allowed.")

    def paste_spheres(self):
        if self.copied_sphere is None or self.selected_entity is None:
            return

        self.copied_sphere.paste_to(self.selected_entity)

    def clear_spheres(self):
        components = find_all_components(self.selected_entity, SphereGroupComponent)
        for c in components:
            c.clear()
        self.viewer.notify_render_update()

    def remove_sphere(self):
        if self.selected_sphere[0] is None:
            return

        self.selected_sphere[0].remove_sphere(self.selected_sphere[1])
        self.unselected_sphere_node(update_sphere=False)
        self.viewer.notify_render_update()

    def add_sphere(self, pos: list[float], radius: float):
        components = find_all_components(self.selected_entity, SphereGroupComponent)
        if len(components) == 0:
            sphere_group = SphereGroupComponent(self.selected_entity)
        else:
            sphere_group = components[0]
        sphere_group.add_sphere(pos, radius)
        self.select_sphere(sphere_group, len(sphere_group.sphere_visuals) - 1)
        self.viewer.notify_render_update()

    def apply_transform(self):
        if self.selected_entity is None:
            return
        components = find_all_components(self.selected_entity, SphereGroupComponent)
        if len(components) == 0:
            return

        sphere_group = components[0]
        pose = sapien.Pose(self._translation_to_apply)
        pose.set_rpy(np.deg2rad(self._rotation_to_apply))
        sphere_group.transform_all_spheres(pose)

    def build(self):
        if self.viewer.render_scene is None:
            self.ui_window = None
            return

        if self.ui_window is None:
            self.ui_window = (
                R.UIWindow().Pos(10, 10).Size(400, 400).Label("Collision Spheres")
            )
        else:
            self.ui_window.remove_children()

        if self.selected_entity is None:
            self.ui_window.append(R.UIDisplayText().Text("No entity selected."))
            return

        if self.selected_articulation is not None:
            self.ui_window.append(
                R.UIDisplayText().Text(f"Robot: {self.selected_articulation.name}")
            )
            self.ui_window.append(
                R.UISameLine().append(
                    R.UIButton()
                    .Label("Show Sphere")
                    .Id("show_robot_sphere")
                    .Callback(lambda p: self.switch_robot_sphere(True)),
                    R.UIButton()
                    .Label("Hide Sphere")
                    .Id("hide_robot_sphere")
                    .Callback(lambda p: self.switch_robot_sphere(False)),
                    R.UIButton()
                    .Label("Show Visual")
                    .Id("show_robot_visual")
                    .Callback(lambda p: self.switch_robot_visual(True)),
                    R.UIButton()
                    .Label("Hide Visual")
                    .Id("hide_robot_visual")
                    .Callback(lambda p: self.switch_robot_visual(False)),
                ),
                R.UISameLine().append(
                    R.UIButton()
                    .Label("Save")
                    .Callback(lambda p: self.save(self.selected_articulation)),
                ),
                R.UIDummy().Height(20),
            )

        components = find_all_components(self.selected_entity, SphereGroupComponent)
        p = self.selected_entity.pose.p
        q = self.selected_entity.pose.q
        self.ui_window.append(
            # Link info
            R.UIDisplayText().Text(f"Link: {self.selected_entity.name}"),
            R.UIInputFloat3().Value(p).ReadOnly(True).Label("position"),
            R.UIInputFloat4().Value(q).ReadOnly(True).Label("pose.q"),
            R.UISameLine().append(
                R.UIButton()
                .Label("Show Sphere")
                .Id("show_link_sphere")
                .Callback(lambda p: self.switch_sphere(True)),
                R.UIButton()
                .Label("Hide Sphere")
                .Id("hide_link_sphere")
                .Callback(lambda p: self.switch_sphere(False)),
                R.UIButton()
                .Label("Show Visual")
                .Id("show_link_visual")
                .Callback(lambda p: self.switch_visual(True)),
                R.UIButton()
                .Label("Hide Visual")
                .Id("hide_link_visual")
                .Callback(lambda p: self.switch_visual(False)),
            ),
            R.UIDummy().Height(20),
            # Link sphere transform
            R.UIDisplayText().Text("Link Sphere Transform"),
            R.UIInputFloat3()
            .Value(self._translation_to_apply)
            .Label("Translation")
            .Callback(lambda p: setattr(self, "_translation_to_apply", p.value))
            .Id("Translation"),
            R.UIInputFloat3()
            .Value(self._rotation_to_apply)
            .Label("Rotation")
            .Callback(lambda p: setattr(self, "_rotation_to_apply", p.value))
            .Id("Rotation Angle"),
            R.UIButton().Label("Apply").Callback(lambda p: self.apply_transform()),
            R.UIDummy().Height(20),
            # Sphere info
            R.UIDisplayText().Text(
                f"Number of Spheres: {0 if len(components) == 0 else len(components[0].sphere_visuals)}"
            ),
            R.UISameLine().append(
                R.UIButton()
                .Label("Clear All")
                .Callback(lambda p: self.clear_spheres()),
                R.UIButton().Label("Copy").Callback(lambda p: self.copy_spheres()),
                R.UIButton().Label("Paste").Callback(lambda p: self.paste_spheres()),
                R.UIButton().Label("Delete").Callback(lambda p: self.remove_sphere()),
                R.UIButton()
                .Label("Add")
                .Callback(lambda p: self.add_sphere([0, 0, 0], 0.05)),
            ),
        )

        if len(components) > 0:
            sphere_group = components[0]
            self.ui_window.append(R.UIDummy().Height(20))

            # Show the info of the selected sphere
            if self.selected_sphere[1] >= 0:
                self.ui_window.append(
                    R.UIDisplayText().Text(f"Sphere {self.selected_sphere[1]}"),
                    R.UIInputFloat3()
                    .Value(self.selected_sphere_node.children[0].position)
                    .Label("position")
                    .Callback(
                        lambda p: self.selected_sphere_node.children[0].set_position(
                            p.value
                        )
                    )
                    .Id("sphere_pos_{self.selected_sphere[1]}"),
                    R.UIInputFloat()
                    .Value(self.selected_sphere_node.children[0].scale[0])
                    .Label("radius")
                    .Callback(
                        lambda p: self.selected_sphere_node.children[0].set_scale(
                            [p.value] * 3
                        )
                    )
                    .Id("sphere_radius_{self.selected_sphere[1]}"),
                )

            if self.selected_sphere_node is not None:
                self.ui_window.append(self.gizmo)

                proj = self.viewer.window.get_camera_projection_matrix()
                view = (
                    (
                        self.viewer.window.get_camera_pose()
                        * sapien.Pose([0, 0, 0], [-0.5, -0.5, 0.5, 0.5])
                    )
                    .inv()
                    .to_transformation_matrix()
                )
                self.gizmo.CameraMatrices(view, proj)
                root_pose = sapien.Pose(
                    self.selected_sphere_node.position,
                    self.selected_sphere_node.rotation,
                )
                sphere_pose = root_pose * sapien.Pose(
                    self.selected_sphere_node.children[0].position
                )
                self.gizmo.Matrix(sphere_pose.to_transformation_matrix())
                self._gizmo_pose = sphere_pose
            else:
                if self.gizmo is not None:
                    self.gizmo.Matrix(np.eye(4))
                self._gizmo_pose = sapien.Pose()

            # Show the tree of spheres
            atree = R.UITreeNode().Label("Spheres")
            self.ui_window.append(atree)
            for i, sphere_visual in enumerate(sphere_group.sphere_visuals):
                if self.selected_sphere[1] == i:
                    text = f"Sphere {i} (selected)"
                else:
                    text = f"Sphere {i}"
                atree.append(
                    R.UISelectable()
                    .Label(text)
                    .Id("sphere{}".format(i))
                    .Callback(
                        (
                            lambda index: lambda _: self.select_sphere(
                                sphere_group, index
                            )
                        )(i)
                    )
                )

    @property
    def gizmo_matrix(self):
        return self._gizmo_pose.to_transformation_matrix()

    @gizmo_matrix.setter
    def gizmo_matrix(self, v):
        if self.selected_sphere_node is not None:
            child = self.selected_sphere_node.children[0]
            self._gizmo_pose = sapien.Pose(v)
            root_pose = sapien.Pose(
                self.selected_sphere_node.position, self.selected_sphere_node.rotation
            )
            relative_pose = root_pose.inv() * self._gizmo_pose
            child.set_position(relative_pose.p)
            child.set_rotation(relative_pose.q)

    def get_ui_windows(self):
        self.build()
        if self.ui_window:
            return [self.ui_window]
        return []

    def notify_scene_change(self):
        self.ui_window = None

    def set_save_path(self, path: Path):
        self.save_path = path

    def save(self, robot: sapien.physx.PhysxArticulation):
        if self.save_path is None:
            return

        self.unselected_sphere_node()
        collision_sphere_cfgs = {}
        for link in robot.links:
            components = find_all_components(link.entity, SphereGroupComponent)
            if len(components) == 1:
                collision_sphere_cfg = components[0].to_dict()
                collision_sphere_cfgs.update(collision_sphere_cfg)

        # Create a custom representer for lists to use flow style only for coordinate lists
        def list_representer(dumper, data):
            if len(data) > 0 and all(isinstance(x, (int, float)) for x in data):
                return dumper.represent_sequence(
                    "tag:yaml.org,2002:seq", data, flow_style=True
                )
            return dumper.represent_sequence(
                "tag:yaml.org,2002:seq", data, flow_style=False
            )

        yaml.add_representer(list, list_representer)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        save_path = (
            self.save_path.parent
            / f"{self.save_path.stem}_{timestamp}{self.save_path.suffix}"
        )
        with save_path.open("w") as f:
            yaml.dump(collision_sphere_cfgs, f, sort_keys=False)
            print(f"Saved collision spheres to {save_path}")

        return collision_sphere_cfgs
