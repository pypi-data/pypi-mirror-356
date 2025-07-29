import numpy as np
import sapien
from jaxtyping import Float
from ruckig import InputParameter, OutputParameter, Ruckig
from scipy.interpolate import interp1d
from scipy.spatial.transform import Rotation, Slerp


def ruckig_interpolation_pos(
    pos_array: Float[np.ndarray, "N D"],
    velocity_limit: float,
    acceleration_limit: float,
) -> Float[np.ndarray, "N D"]:
    """Performs smooth trajectory interpolation using Ruckig algorithm.

    Args:
        pos_array: Array of positions with shape (N, D) where N is the number of
            waypoints and D is the dimensionality of each position.
        velocity_limit: Maximum allowed velocity in each dimension.
        acceleration_limit: Maximum allowed acceleration in each dimension.

    Returns:
        An array of smoothed positions with the same shape as the input.
    """
    N, D = pos_array.shape
    otg = Ruckig(D, 1 / 60)
    inp = InputParameter(D)
    out = OutputParameter(D)

    inp.max_velocity = np.ones(D) * velocity_limit
    inp.max_acceleration = np.ones(D) * acceleration_limit
    inp.current_position = pos_array[0]

    pos_list = []
    for i in range(N - 1):
        inp.target_position = pos_array[i]
        inp.target_velocity = np.zeros(D)
        inp.target_acceleration = np.zeros(D)
        otg.update(inp, out)
        pos_list.append(out.new_position)
        out.pass_to_input(inp)
    pos_list.append(pos_array[-1])
    return np.array(pos_list)


def smooth_interpolation_pos(
    pos_array: Float[np.ndarray, "N D"],
    time_array: Float[np.ndarray, " N"],
    vel_limit: float = 1.5,
    acc_limit: float = 5,
) -> Float[np.ndarray, "M D"]:
    """Performs smooth position interpolation followed by Ruckig smoothing.

    Args:
        pos_array: Array of positions with shape (N, D) where N is the number of
            waypoints and D is the dimensionality of each position.
        time_array: Array of timestamps corresponding to each position, shape (N,).
        vel_limit: Maximum allowed velocity in each dimension.
        acc_limit: Maximum allowed acceleration in each dimension.

    Returns:
        Array of smoothed positions at integer timestamps, shape (M, D).
    """
    start_time = time_array[0]
    end_time = time_array[-1]
    all_times = np.arange(start_time, end_time + 1)
    interpolator = interp1d(
        time_array,
        pos_array,
        axis=0,
        kind="linear",
        bounds_error=False,
        fill_value=(pos_array[0], pos_array[-1]),
    )

    # Apply interpolation to all timestamps
    result = interpolator(all_times)
    result = ruckig_interpolation_pos(result, vel_limit, acc_limit)

    return result


def smooth_interpolation_rotation(
    quat_array: Float[np.ndarray, "N 4"],
    time_array: Float[np.ndarray, " N"],
    vel_limit: float = 1.5,
    acc_limit: float = 5,
) -> Float[np.ndarray, "M 4"]:
    """Interpolates quaternion rotations using Slerp followed by Ruckig smoothing.

    Args:
        quat_array: Array of quaternions with shape (N, 4) in wxyz format.
        time_array: Array of timestamps corresponding to each quaternion, shape (N,).
        vel_limit: Maximum allowed angular velocity in radians/second.
        acc_limit: Maximum allowed angular acceleration in radians/second².

    Returns:
        Array of smoothed quaternions at integer timestamps, shape (M, 4).
    """
    # Get time range and create integer timestamps
    start_time = time_array[0]
    end_time = time_array[-1]
    all_times = np.arange(start_time, end_time + 1)

    # Convert quaternions from wxyz to scipy's xyzw format
    scipy_quats = np.zeros_like(quat_array)
    scipy_quats[:, :3] = quat_array[:, 1:]  # xyz
    scipy_quats[:, 3] = quat_array[:, 0]  # w

    # Interpolate using Slerp
    rotations = Rotation.from_quat(scipy_quats)
    slerp = Slerp(time_array, rotations)
    interpolated_rotations = slerp(all_times)

    # Convert back to wxyz format
    interpolated_quats = np.zeros((len(all_times), 4))
    scipy_quats = interpolated_rotations.as_quat()
    interpolated_quats[:, 0] = scipy_quats[:, 3]  # w
    interpolated_quats[:, 1:] = scipy_quats[:, :3]  # xyz

    # Smooth and normalize
    smoothed_quats = ruckig_interpolation_pos(interpolated_quats, vel_limit, acc_limit)
    norms = np.linalg.norm(smoothed_quats, axis=1, keepdims=True)
    normalized_quats = smoothed_quats / norms

    return normalized_quats


def smooth_interpolate_pose(
    poses: list[sapien.Pose],
    time_arrays: list[int],
    trans_vel_limit: float = 5,
    trans_acc_limit: float = 30,
    rot_vel_limit: float = 6.28,
    rot_acc_limit: float = 30,
) -> list[sapien.Pose]:
    """Smoothly interpolates a sequence of poses.

    Args:
        poses: List of sapien.Pose objects to interpolate.
        time_arrays: List of timestamps corresponding to each pose.
        pos_vel_limit: Maximum allowed positional velocity.
        pos_acc_limit: Maximum allowed positional acceleration.
        rot_vel_limit: Maximum allowed rotational velocity in radians/second.
        rot_acc_limit: Maximum allowed rotational acceleration in radians/second².

    Returns:
        List of interpolated and smoothed sapien.Pose objectsm.
    """
    pos_array = np.array([p.p for p in poses])
    quat_array = np.array([p.q for p in poses])
    time_array = np.array(time_arrays)

    pos_array = smooth_interpolation_pos(
        pos_array, time_array, vel_limit=trans_vel_limit, acc_limit=trans_acc_limit
    )
    quat_array = smooth_interpolation_rotation(
        quat_array, time_array, vel_limit=rot_vel_limit, acc_limit=rot_acc_limit
    )

    return [sapien.Pose(pos_array[i], quat_array[i]) for i in range(len(pos_array))]
