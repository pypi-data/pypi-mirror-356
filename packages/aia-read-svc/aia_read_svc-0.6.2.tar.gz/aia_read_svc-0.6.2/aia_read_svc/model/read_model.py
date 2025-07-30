from typing import List
from typing import Any
from dataclasses import dataclass
import json

@dataclass
class Speech:
    text: str
    language: str

    @staticmethod
    def from_dict(obj: Any) -> 'Speech':
        _text = str(obj.get("text"))
        _language = str(obj.get("language"))

        return Speech(_text, _language)