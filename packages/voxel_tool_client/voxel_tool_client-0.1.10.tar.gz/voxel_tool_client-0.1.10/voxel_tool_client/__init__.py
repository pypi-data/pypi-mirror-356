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
class PathFindingParams:
    level_name: Optional[str] = None
    start: Optional[Vector3] = None
    end: Optional[Vector3] = None

@dataclasses.dataclass()
class PathFindingResult:
    path: Optional[List[Vector3]] = None
    error: Optional[str] = None

@dataclasses.dataclass()
class FindNPCPositionParams:
    npc_id: int
    world_id: int

@dataclasses.dataclass()
class FindNPCPositionResult:
    position: Optional[Vector3] = None
    error: Optional[str] = None

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
        return data_version

    def find_path(self, params: PathFindingParams) -> PathFindingResult:
        sub_url = "/path_finding/"
        result = self._do_request(sub_url, dataclasses.asdict(params))
        if result.error is not None:
            return PathFindingResult(
                path=None,
                error=result.error
            )

        path = None
        data_path = result.data.get("path")
        data_error = result.data.get("error")
        if data_path is not None:
            path = []
            for data_position in data_path:
                path_position = Vector3(x=data_position["x"], y=data_position["y"], z=data_position["z"])
                path.append(path_position)
        
        return PathFindingResult(
            path=path,
            error=data_error,
        )
    
    def find_npc_position(self, params: FindNPCPositionParams) -> FindNPCPositionResult:
        sub_url = "/find_npc_position/"
        result = self._do_request(sub_url, dataclasses.asdict(params))
        if result.error is not None:
            return FindNPCPositionResult(
                position=None,
                error=result.error
            )
        data_position = result.data.get("position")
        data_error = result.data.get("error")
        if data_position is not None:
            position = Vector3(x=data_position["x"], y=data_position["y"], z=data_position["z"])
        return FindNPCPositionResult(
            position=position,
            error=data_error,
        )
