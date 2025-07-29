import pickle
import time
from pathlib import Path

import numpy as np
from sapien.utils.viewer.control_window import ControlWindow


class RecordControlWindow(ControlWindow):
    def __init__(self, data_path: Path, env, joint_names: list[str]):
        super().__init__()
        self.env = env
        self.joint_names = joint_names

        data_path.parent.mkdir(exist_ok=True, parents=True)
        if data_path.exists():
            data = np.load(str(data_path), allow_pickle=True)
            if isinstance(data, dict) and data.get("recorded_states") is not None:
                self.record_states = data["recorded_states"]
                self.joint_names = data["joint_names"]
            else:
                raise ValueError(f"Invalid data format: {type(data)}")
            self.env.set_state(self.record_states[-1])
            print(
                f"Load existing recording with {len(self.record_states)} saved states."
            )
        else:
            self.record_states = []
            print("Start recording from scratch...")
        self.data_path = data_path
        self.current_index = len(self.record_states) - 1
        self.copied_data = None

        instructions = """
        Press i to save the current state.
        Press g to duplicate the current state and append to the end.
        Press p to pop out the current state.
        Press k to set to the next state.
        Press j to set to the previous state.
        """
        print(instructions)

    def _handle_input_ipjk(self):
        if self.window.key_down("i"):
            data = self.env.get_state()
            self.record_states.insert(self.current_index + 1, data)
            self.current_index += 1
            print(
                f"Save {self.current_index}-th state."
                f"Now there are {len(self.record_states)} states in total."
            )
            time.sleep(0.2)
        if self.window.key_down("c"):
            data = self.record_states[self.current_index]
            self.copied_data = data.copy()
            print(f"Copied {self.current_index}-th state.")
            time.sleep(0.2)
        if self.window.key_down("v"):
            if self.copied_data is None:
                print("No data is  copied, so pasting is not feasible")
            self.record_states.insert(self.current_index + 1, self.copied_data)
            self.current_index += 1
            self.copied_data = None
            print(
                f"Pasted copied data to {self.current_index}-th state."
                f"Now there are {len(self.record_states)} states in total."
            )
            time.sleep(0.2)
        if self.window.key_down("g"):
            data = self.env.get_state()
            duplicate_index = self.current_index
            self.record_states.append(data)
            self.current_index = len(self.record_states) - 1
            print(
                f"Duplicating {duplicate_index}-th state and appending to the end. "
                f"Now there are {len(self.record_states)} states in total."
            )
            time.sleep(0.2)
        if self.window.key_down("p"):
            self.record_states.pop(self.current_index)
            self.current_index = max(self.current_index - 1, 0)
            data = self.record_states[self.current_index]
            self.env.set_state(data)
            print(
                f"Pop out the {self.current_index}-th state,"
                f"now set to the new {self.current_index}-th state"
            )
            time.sleep(0.2)
        if self.window.key_down("k"):
            self.current_index += 1
            self.current_index = min(self.current_index, len(self.record_states) - 1)
            data = self.record_states[self.current_index]
            self.env.set_state(data)
            print(f"Set to state index {self.current_index}")
            time.sleep(0.2)
        if self.window.key_down("j"):
            self.current_index -= 1
            self.current_index = max(self.current_index, 0)
            data = self.record_states[self.current_index]
            self.env.set_state(data)
            print(f"Set to state index {self.current_index}")
            time.sleep(0.2)

    def after_render(self):
        if self._single_step and self.viewer.paused:
            self.viewer.paused = False
        elif self._single_step and not self.viewer.paused:
            self._single_step = False
            self.viewer.paused = True

        self._sync_fps_camera_controller()

        self._handle_focused_entity()

        self._handle_click()

        self._handle_input_wasd()
        self._handle_input_mouse()
        self._handle_input_f()
        self._handle_input_esc()
        self._handle_input_ipjk()

        if self.show_camera_linesets:
            self._update_camera_linesets()

        if self.show_joint_axes:
            self._update_joint_axes()
        if self.show_origin_frame:
            self._update_coordinate_axes()

    def close(self):
        super().close()
        with self.data_path.open("wb") as f:
            pickle.dump(
                {
                    "recorded_states": self.record_states,
                    "joint_names": self.joint_names,
                },
                f,
            )
            print(f"Save recoding file {self.data_path}")
