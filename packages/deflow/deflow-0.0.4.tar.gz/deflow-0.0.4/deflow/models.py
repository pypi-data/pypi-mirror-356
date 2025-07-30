from typing import Literal, Union

from pydantic import BaseModel, Field

RunMode = Literal["N", "R", "F", "T"]


class Variable(BaseModel):
    stages: dict[str, dict[str, Union[str, int]]] = Field(default_factory=dict)
