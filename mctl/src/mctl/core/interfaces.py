from dataclasses import dataclass
from typing import List

@dataclass()
class InitialiserResponse:
    base_path: str
    dirs: List[str]
    config_path: str


@dataclass()
class ServerInfoResponse:
    name: str
    path: str
    type: str
    version: str
    memory: str
    jar: str
    java: str
