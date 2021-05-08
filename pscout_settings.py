from dataclasses import dataclass
from dataclasses_serialization.json import JSONSerializer
import json

NO_CAMERA = 0
IDS_USB2 = 1

@dataclass
class MaxResultCount:
    with_image: int
    without_image: int


@dataclass
class Connection:
    ip: str
    port: int
    use_ssl: bool
    certificate: str
    key: str


@dataclass
class Settings:
    max_result_count: MaxResultCount
    default_disabled_categroies: list
    connection: Connection
    camera_type: int


def load_json_file(fn: str) -> Settings:
    with open(fn, "rt") as f:
        myjson = json.loads(f.read())
    settings = JSONSerializer.deserialize(Settings, myjson)
    return settings


def save_json_file(fn: str, settings: Settings) -> None:
    myjson = JSONSerializer.serialize(settings)
    with open(fn, "wt") as f:
        f.write(json.dumps(myjson, indent=4))
