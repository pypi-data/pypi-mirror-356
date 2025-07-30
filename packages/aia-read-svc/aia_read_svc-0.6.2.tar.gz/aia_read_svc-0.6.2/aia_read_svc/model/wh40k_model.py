
from typing import List
from typing import Any
from dataclasses import dataclass
import json
from .read_model import Speech
import dataclasses

@dataclass
class WH40K_Abstract:
    
    def dict(self):
        return {k: v for k, v in dataclasses.asdict(self).items()}


@dataclass
class WH40K_Characteristic:
    name: str
    value: str

@dataclass
class WH40K_Unit_Images(WH40K_Abstract):
    image: bytes
    image_name: str
    unit_id: str

@dataclass
class WH40K_Unit(WH40K_Abstract):
    name: str
    code: str
    speech: Speech
    faction: str    
    edition: str
    characteristics: List[WH40K_Characteristic]

    def __init__(self, my_dict): 
        for key in my_dict: 
            setattr(self, key, my_dict[key]) 

@dataclass
class WH40K_Faction:
    name: str
    units: List[WH40K_Unit]


