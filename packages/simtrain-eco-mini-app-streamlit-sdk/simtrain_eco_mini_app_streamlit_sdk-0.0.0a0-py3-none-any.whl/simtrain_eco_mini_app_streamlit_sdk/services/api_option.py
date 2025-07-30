from dataclasses import dataclass, asdict
from typing import TypedDict, Optional, Dict, Any


class ApiOption(TypedDict, total=False):
    api_key: str = ""
