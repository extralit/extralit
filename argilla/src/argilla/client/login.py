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
Temporary login module for CLI testing.
This will be replaced in Phase 3 of the CLI migration.
"""

class ArgillaCredentials:
    """Placeholder for ArgillaCredentials class."""
    
    def __init__(self, api_url=None, api_key=None):
        self.api_url = api_url
        self.api_key = api_key
    
    @classmethod
    def exists(cls):
        """Check if credentials exist."""
        # Placeholder implementation for testing
        return True