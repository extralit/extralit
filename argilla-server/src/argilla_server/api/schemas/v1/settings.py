# Copyright 2024-present, Extralit Labs, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Optional

from pydantic import BaseModel, ConfigDict


class HuggingfaceSettings(BaseModel):
    space_id: Optional[str]
    space_title: Optional[str]
    space_subdomain: Optional[str]
    space_host: Optional[str]
    space_repo_name: Optional[str]
    space_author_name: Optional[str]
    space_persistent_storage_enabled: bool

    model_config = ConfigDict(from_attributes=True)


class ArgillaSettings(BaseModel):
    show_huggingface_space_persistent_storage_warning: Optional[bool] = None
    share_your_progress_enabled: bool = False


class Settings(BaseModel):
    argilla: ArgillaSettings
    huggingface: Optional[HuggingfaceSettings] = None
