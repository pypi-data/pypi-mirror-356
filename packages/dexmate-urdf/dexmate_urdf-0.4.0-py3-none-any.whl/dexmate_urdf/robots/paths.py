import importlib.resources
from pathlib import Path
from typing import Literal

ROBOT_TYPES = Literal["hands", "humanoid", "arms", "assembly"]


def get_robot_dir() -> Path:
    """Get the root directory containing all robot models."""
    with importlib.resources.files("dexmate_urdf") as f:
        return (f / "robots").resolve()


def get_robot_names(
    robot_type: ROBOT_TYPES,
) -> list[str]:
    """Get all available robots for a given type.

    Args:
        robot_type: Type of robot (hand, humanoid, arm, assembly)

    Returns:
        List of robot names available for the given type
    """
    robot_dir = get_robot_dir() / robot_type
    if not robot_dir.exists():
        raise ValueError(f"Robot type {robot_type} not found")
    return [p.name for p in robot_dir.iterdir() if p.is_dir()]


def get_robot_path(
    robot_type: ROBOT_TYPES,
    robot_name: str,
    version: str = "default",
) -> Path:
    """Get the path to a specific robot's directory.

    Args:
        robot_type: Type of robot (hand, humanoid, arm, assembly)
        robot_name: Name of the robot
        version: Version of the robot

    Returns:
        Path to the robot's directory
    """
    robot_dir = get_robot_dir() / robot_type / robot_name
    if version != "default":
        robot_dir = robot_dir / version
    if not robot_dir.exists():
        raise ValueError(f"Robot {robot_name} of type {robot_type} not found")
    return robot_dir


def get_urdf_paths(
    robot_type: ROBOT_TYPES, robot_name: str, version: str = "default"
) -> list[Path]:
    """Get the path to a robot's URDF file.

    Args:
        robot_type: Type of robot (hand, humanoid, arm, assembly)
        robot_name: Name of the robot
        version: Version of the robot

    Returns:
        Path to the robot's URDF file
    """
    robot_dir = get_robot_path(robot_type, robot_name, version)
    urdf_files = list(robot_dir.glob("*.urdf"))
    if not urdf_files:
        raise FileNotFoundError(f"No URDF file found for {robot_name} in {robot_type}")
    return urdf_files


def get_mesh_dir(
    robot_type: ROBOT_TYPES, robot_name: str, version: str = "default"
) -> Path:
    """Get the path to a robot's mesh directory.

    Args:
        robot_type: Type of robot (hand, humanoid, arm, assembly)
        robot_name: Name of the robot

    Returns:
        Path to the robot's mesh directory
    """
    robot_dir = get_robot_path(robot_type, robot_name, version)
    mesh_dir = robot_dir / "meshes"
    if not mesh_dir.exists():
        raise FileNotFoundError(
            f"No meshes directory found for {robot_name} in {robot_type}"
        )
    return mesh_dir
