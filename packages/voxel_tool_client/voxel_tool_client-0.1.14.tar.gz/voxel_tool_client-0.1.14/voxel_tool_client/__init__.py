import requests
import dataclasses
from typing import *

@dataclasses.dataclass()
class ClientConfig:
    base_url: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None

@dataclasses.dataclass()
class Vector3:
    x: float
    y: float
    z: float

@dataclasses.dataclass()
class ResultData:
    data: Optional[Any] = None
    error: Optional[str] = None

@dataclasses.dataclass()
class NpcFindingRequest():
    npc_id: int
    world_id: int

@dataclasses.dataclass()
class NpcFindingResult():
    success: bool = False
    message: Optional[str] = None
    error: Optional[str] = None

    position: Optional[Vector3] = None

@dataclasses.dataclass()
class PathFindingRequest():
    world_id: int
    start: Vector3
    end: Vector3

@dataclasses.dataclass()
class PathFindingResult():
    success: bool = False
    message: Optional[str] = None
    error: Optional[str] = None

    path: Optional[List[Vector3]] = None
    collision: Optional[List[Vector3]] = None

class VoxelClient:
    def __init__(self, config: ClientConfig):
        self.config = config

    def _get_default_config(self)-> Dict[str, Any]:
        return {
            "username": self.config.username,
            "password": self.config.password,
        }

    def _do_request(self, sub_url: str, params: Dict[str, Any]) -> ResultData:
        try:
            data = {
                "config": self._get_default_config(),
                "data": params
            }
            url = f"{self.config.base_url}{sub_url}"
            response = requests.post(url, json=data)
            response.raise_for_status()
            return ResultData(
                data=response.json(),
                error=None
            )
        except requests.exceptions.RequestException as e:
            return ResultData(
                data=None,
                error=f"请求失败: {str(e)}"
            )
        
    def get_voxel_version(self) -> Optional[str]:
        sub_url = "/get_voxel_version/"
        result = self._do_request(sub_url, {})
        if result.error is not None:
            return None
        data_version = result.data.get("version")
        if data_version is None:
            return None
        return data_version

    def find_path(self, params: PathFindingRequest) -> PathFindingResult:
        sub_url = "/path_finding/"
        result = self._do_request(sub_url, dataclasses.asdict(params))
        if result.error is not None:
            return PathFindingResult(   
                success=False,
                message=None,
                path=None,
                collision=None,
                error=result.error
            )

        path = None
        data_path = result.data.get("path")
        data_message = result.data.get("message")
        if data_path is not None:
            path = []
            for data_position in data_path:
                path_position = Vector3(x=data_position["x"], y=data_position["y"], z=data_position["z"])
                path.append(path_position)
        
        return PathFindingResult(
            success=True,
            message=data_message,
            path=path,
            collision=None,
            error=None,
        )
    
    def get_npc_id_by_world_id(self, world_id: int) -> List[int]:
        sub_url = "/get_npc_id_by_world_id/"
        result = self._do_request(sub_url, {"world_id": world_id})
        if result.error is not None:
            return []
        return result.data

    def find_npc_position(self, params: NpcFindingRequest) -> NpcFindingResult:
        sub_url = "/find_npc_position/"
        result = self._do_request(sub_url, dataclasses.asdict(params))
        if result.error is not None:
            return NpcFindingResult(
                success=False,
                message=None,
                position=None,
                error=result.error,
            )
        data_position = result.data.get("position")
        data_message = result.data.get("message")
        position = None
        if data_position is not None:
            position = Vector3(x=data_position["x"], y=data_position["y"], z=data_position["z"])
        return NpcFindingResult(
            success=True,
            message=data_message,
            position=position,
            error=None,
        )
