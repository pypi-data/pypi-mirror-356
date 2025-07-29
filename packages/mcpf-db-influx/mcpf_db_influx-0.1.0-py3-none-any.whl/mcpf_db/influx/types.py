import inspect
from dataclasses import dataclass
from typing import Any


@dataclass
class InfluxConfig:
    """
    Configuration for InfluxDB connection.
    """

    url: str | None = None
    token: str | None = None
    org: str | None = None
    bucket: str | None = None

    @classmethod
    def from_dict(cls, dict: dict[str, Any]) -> "InfluxConfig":
        """Use this constructor to create an InfluxConfig object from
        a dictionary whose surplus keys are ignored instead of raising TypeError."""
        return cls(**{k: v for k, v in dict.items() if k in inspect.signature(cls).parameters})
