from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Dict, Optional

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json
@dataclass
class PropertyDefinition:
    name: str
    kind: str
    category: str
    password: bool
    value: Any

    def property_value(self):
        if self.kind == 'CI':
            ci = CiDefinition.from_dict(self.value)
            return {p.name: p.property_value() for p in ci.properties}
        else:
            return self.value

    def secret_value(self):
        if self.kind == 'CI':
            ci = CiDefinition.from_dict(self.value)
            return [p.value for p in ci.properties if p.password and p.value]
        else:
            return [self.value] if self.password and self.value else []


@dataclass_json
@dataclass
class CiDefinition:
    id: str
    type: str
    properties: List[PropertyDefinition]


@dataclass_json
@dataclass
class TaskContext(CiDefinition):
    def output_properties(self) -> list[str]:
        return [p.name for p in self.properties if p.category == 'output']

    def secrets(self) -> list[str]:
        secret_list = []
        for p in self.properties:
            secret_list.extend(p.secret_value())
        return secret_list

    def build_locals(self) -> Dict[str, Any]:
        return {p.name: p.property_value() for p in self.properties}

    def scriptLocation(self) -> str:
        return next(p.value for p in self.properties if p.name == 'scriptLocation')


@dataclass_json
@dataclass
class AutomatedTaskAsUserContext:
    username: Optional[str]
    password: Optional[str]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ReleaseContext:
    id: str
    automated_task_as_user: AutomatedTaskAsUserContext


@dataclass_json()
@dataclass
class InputContext:
    release: ReleaseContext
    task: TaskContext
