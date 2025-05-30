#  Copyright 2021-present, the Recognai S.L. team.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from typing import Any, Literal, Optional
from uuid import UUID

from argilla_v1.pydantic_v1 import BaseModel


class SuggestionModel(BaseModel):
    id: UUID
    question_id: UUID
    value: Any
    type: Optional[Literal["model", "human", "selection"]] = None
    score: Optional[float] = None
    agent: Optional[str] = None
