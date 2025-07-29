"""Robot models module with dynamic imports for better code completion."""

from pathlib import Path
from .paths import get_mesh_dir, get_robot_dir, get_robot_path, get_urdf_paths


class URDFModel:
    """Represents a specific URDF model file within a robot directory."""

    def __init__(self, robot_type: str, robot_name: str, version: str, urdf_name: str):
        self._type = robot_type
        self._name = robot_name
        self._version = version
        self._urdf_name = urdf_name
        self._parent_dir = get_robot_path(robot_type, robot_name, version)

    @property
    def urdf(self) -> Path:
        """Get the path to this specific URDF file."""
        return self._parent_dir / self._urdf_name

    @property
    def srdf(self) -> Path:
        """Get the corresponding SRDF file path if it exists."""
        srdf_name = f"{self._urdf_name.rsplit('.', 1)[0]}_pin.srdf"
        path = self._parent_dir / srdf_name
        if path.exists():
            return path
        raise FileNotFoundError(f"SRDF file not found: {path}")

    @property
    def collision_spheres_urdf(self) -> Path:
        """Get the corresponding collision spheres URDF path if it exists."""
        collision_name = f"{self._urdf_name.rsplit('.', 1)[0]}_collision_spheres.collision.urdf"
        path = self._parent_dir / collision_name
        if path.exists():
            return path
        raise FileNotFoundError(f"Collision spheres URDF file not found: {path}")

    def __repr__(self) -> str:
        return str(self.urdf)


class RobotDir:
    """Represents a specific version of a robot."""

    def __init__(self, robot_type: str, robot_name: str, version: str):
        self._type = robot_type
        self._name = robot_name
        self._version = version
        self._urdf_models: dict[str, URDFModel] = {}

        # Initialize URDF models
        for urdf_path in get_urdf_paths(robot_type, robot_name, version):
            if urdf_path.suffix == ".urdf":
                model_name = urdf_path.stem
                self._urdf_models[model_name] = URDFModel(
                    robot_type, robot_name, version, urdf_path.name
                )

    @property
    def model_list(self) -> list[URDFModel]:
        """Get the list of URDF models in this robot directory."""
        return list(self._urdf_models.values())

    @property
    def mesh_dir(self) -> Path:
        """Get the mesh directory for this robot directory."""
        return get_mesh_dir(self._type, self._name, self._version)

    @property
    def path(self) -> Path:
        """Get the path to this robot directory."""
        return get_robot_path(self._type, self._name, self._version)

    def __repr__(self) -> str:
        return str(self.path)

    def __getattr__(self, name: str) -> URDFModel:
        """Allow accessing URDF models as attributes."""
        if name in self._urdf_models:
            return self._urdf_models[name]
        raise AttributeError(f"URDF model '{name}' not found in {self.path}")

    def __dir__(self) -> list[str]:
        return list(self._urdf_models.keys())


class RobotModel:
    """Represents a robot model with multiple versions."""

    def __init__(self, robot_type: str, robot_name: str):
        self._type = robot_type
        self._name = robot_name
        self._versions = {}

        # Dynamically load versions
        robot_dir = get_robot_dir() / robot_type / robot_name
        if robot_dir.exists():
            has_multiple_version = True
            # Check if there are any URDF files directly in the robot directory
            for file in robot_dir.iterdir():
                if file.suffix == ".urdf":
                    # Create a default version for models without explicit versions
                    self._versions["default"] = RobotDir(robot_type, robot_name, "")
                    has_multiple_version = False
                    break

            # Look for version subdirectories if no direct URDF files found
            if has_multiple_version:
                for version_dir in robot_dir.iterdir():
                    if version_dir.is_dir():
                        version_name = version_dir.name
                        self._versions[version_name] = RobotDir(
                            robot_type, robot_name, version_name
                        )

    def __getattr__(self, name: str) -> RobotDir:
        """Allow accessing versions as attributes."""
        if name in self._versions:
            return self._versions[name]
        raise AttributeError(f"Version '{name}' not found for robot {self._name}")

    def __dir__(self) -> list[str]:
        return list(self._versions.keys())

    def __repr__(self) -> str:
        return f"{self._type}/{self._name}"


class RobotType:
    """Represents a type of robot (e.g., humanoid, hand)."""

    def __init__(self, robot_type: str):
        self._type = robot_type
        self._models: dict[str, RobotModel] = {}

        # Dynamically load robot models
        type_dir = get_robot_dir() / robot_type
        if type_dir.exists():
            for robot_dir in type_dir.iterdir():
                if robot_dir.is_dir():
                    model_name = robot_dir.name
                    self._models[model_name] = RobotModel(robot_type, model_name)

    def __getattr__(self, name: str) -> RobotModel:
        if name in self._models:
            return self._models[name]
        raise AttributeError(f"Robot model '{name}' not found in {self._type}")

    def __dir__(self) -> list[str]:
        return list(self._models.keys())

    def __repr__(self) -> str:
        return self._type

# Create robot type modules dynamically
def _setup_robot_dir():
    robot_dir = get_robot_dir()
    if robot_dir.exists():
        for type_dir in robot_dir.iterdir():
            if type_dir.is_dir():
                type_name = type_dir.name
                globals()[type_name] = RobotType(type_name)


def get_all_robot_dirs() -> list[RobotDir]:
    """Gets all robot model directories.

    Returns:
        list[RobotDir]: A list containing RobotDir objects for all available robot models
            across all types and versions.
    """
    robot_dirs = []
    for robot_type in ["arms", "hands", "assembly", "humanoid"]:
        if robot_type in globals():
            robot_type_obj = globals()[robot_type]
            for model_name in dir(robot_type_obj):
                robot_model = getattr(robot_type_obj, model_name)
                for version in dir(robot_model):
                    robot_dirs.append(getattr(robot_model, version))
    return robot_dirs

_setup_robot_dir()
__all__ = ["humanoid", "hands", "arms", "assembly", "get_all_robot_dirs"]
