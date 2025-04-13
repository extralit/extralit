# Copyright 2024-present, Argilla, Inc.
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

"""
Argilla client stub for CLI testing.
This is a temporary implementation that will be replaced in Phase 3 of the CLI migration.
"""

class Argilla:
    """
    Stub Argilla client class for CLI testing.
    This is a placeholder implementation that will be replaced in Phase 3.
    """
    
    def __init__(self, api_url=None, api_key=None):
        self.api_url = api_url
        self.api_key = api_key
    
    @classmethod
    def from_credentials(cls, api_url=None, api_key=None):
        """Create client from credentials."""
        return cls(api_url, api_key)