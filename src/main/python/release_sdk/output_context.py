from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, List

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class OutputContext:
    exit_code: int
    output_properties: Dict[str, Any]
    reporting_records: List[Dict[str, Any]]
