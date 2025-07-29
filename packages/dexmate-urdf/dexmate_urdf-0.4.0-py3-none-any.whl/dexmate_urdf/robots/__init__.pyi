from pathlib import Path

class RobotType:
    def __init__(self, robot_type):
        pass

    def __getattr__(self, name) -> RobotModel:
        pass

    def __dir__(self) -> list[str]:
        pass

class RobotModel:
    def __init__(self, robot_type, robot_name):
        pass

    def __getattr__(self, name) -> RobotDir:
        pass

    def __dir__(self) -> list[str]:
        pass

class RobotDir:
    def __init__(self, robot_type, robot_name, version):
        pass

    @property
    def model_list(self) -> list[URDFModel]:
        pass

    @property
    def mesh_dir(self) -> Path:
        pass

    @property
    def path(self) -> Path:
        pass

    def __getattr__(self, name) -> URDFModel:
        pass

    def __dir__(self) -> list[str]:
        pass

class URDFModel:
    def __init__(self, robot_type, robot_name, version, urdf_name):
        pass

    @property
    def urdf(self) -> Path:
        pass

    @property
    def srdf(self) -> Path:
        pass

    @property
    def collision_spheres_urdf(self) -> Path:
        pass

class VegaModel(RobotModel):
    class VegaDir(RobotDir):
        pass
        vega_upper_body_no_effector = URDFModel
        vega_no_effector = URDFModel
        vega_upper_body = URDFModel
        vega_upper_body_fixed_head = URDFModel
        vega = URDFModel
        vega_tesollo_3f = URDFModel

    default = VegaDir

class OhandModel(RobotModel):
    class OhandDir(RobotDir):
        pass
        ohand_right = URDFModel
        ohand_left = URDFModel

    default = OhandDir

class HumanoidType(RobotType):
    vega = VegaModel

class HandsType(RobotType):
    ohand = OhandModel

humanoid = HumanoidType
hands = HandsType

def get_all_robot_dirs() -> list[RobotDir]:
    pass
