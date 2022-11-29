from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from dataclasses_json import dataclass_json, LetterCase, config
from marshmallow import fields


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TaskReportingRecord:
    target_id: str
    server_url: str
    server_user: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class BuildRecord(TaskReportingRecord):
    project: str
    build: str
    outcome: str
    start_date: datetime = field(metadata=config(encoder=datetime.isoformat, decoder=datetime.fromisoformat, mm_field=fields.DateTime(format='iso')))
    end_date: datetime = field(metadata=config(encoder=datetime.isoformat, decoder=datetime.fromisoformat, mm_field=fields.DateTime(format='iso')))
    duration: str
    build_url: str = field(metadata=config(field_name="build_url"))
    type: str = "udm.BuildRecord"
    id: str = ""
