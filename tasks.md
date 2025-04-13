# CLI Migration Plan: Argilla v1 to v2

## Overview
This document outlines the plan to migrate the CLI functionality from Argilla v1 to Argilla v2. The CLI was removed in v2, but many researchers prefer using it over the Python SDK. This migration will restore CLI functionality in v2.

## Project Structure Analysis

### Phase 1: Analysis and Setup (Days 1-2) ✅
- [x] Analyze v1 CLI structure in `argilla-v1/src/argilla_v1/cli/`
- [x] Analyze v2 codebase structure in `argilla/src/argilla/`
- [x] Identify dependencies and imports that need updating
- [x] Create initial directory structure in `argilla/src/argilla/cli/`
- [x] Set up testing environment for CLI commands

### Phase 2: Core CLI Framework Migration (Days 3-4) ✅
- [x] Migrate base CLI framework:
  - [x] Port `ArgillaTyper` class and extensions
  - [x] Create main `app.py` entry point
  - [x] Set up command registration structure
  - [x] Update package imports to v2 structure
  - [x] Ensure CLI can be invoked properly (Tests passing)

### Phase 3: Command Migration (Days 5-12) 🔄
Migrate each command module individually, in order of dependency:

#### Basic Commands
- [x] `info_app`: Server information commands
- [x] `login_app`: Authentication commands
- [x] `logout_app`: Logout functionality
- [x] `whoami_app`: User identification

#### User Management
- [ ] `users_app`: User management commands
  - [ ] Create user
  - [ ] List users
  - [ ] Update user
  - [ ] Delete user

#### Workspace Management
- [ ] `workspaces_app`: Workspace management
  - [ ] Create workspace
  - [ ] List workspaces
  - [ ] Update workspace
  - [ ] Delete workspace

#### Dataset Management
- [ ] `datasets_app`: Dataset operations
  - [ ] Create dataset
  - [ ] List datasets
  - [ ] Update dataset
  - [ ] Delete dataset
  - [ ] Import/export functionality

#### Advanced Functionality
- [ ] `training_app`: Model training commands
- [ ] `extraction_app`: Extraction pipeline commands
- [ ] `schemas_app`: Schema management

### Phase 4: Integration and Testing (Days 13-15)
- [ ] Integrate all command modules with main CLI app
- [ ] Write comprehensive tests for each command
- [ ] Test with actual Argilla v2 server
- [ ] Fix any compatibility issues
- [ ] Document any API differences between v1 and v2

### Phase 5: Documentation and Finalization (Days 16-18)
- [ ] Update CLI documentation
- [ ] Create migration guide for users coming from v1
- [ ] Add examples for common CLI usage patterns
- [ ] Final testing and bug fixes
- [ ] Prepare pull request

## Implementation Notes

### Key Challenges
1. **API Differences**: The v2 API may differ from v1, requiring command adaptation
2. **Import Structure**: All imports need to be updated from `argilla_v1` to `argilla`
3. **Dependencies**: Some v1 CLI features might depend on v1-specific functionality
4. **Testing**: Ensuring commands work correctly with the v2 backend

### Implementation Strategy
- Port one module at a time, starting with simpler commands
- Test each module thoroughly before moving to the next
- Keep the same command structure where possible for backward compatibility
- Document any necessary changes to command syntax or behavior

### Required Changes in `pyproject.toml`
- Add CLI entry point in `argilla/pyproject.toml`:
```toml
[project.scripts]
argilla = "argilla.cli.app:app"
```

## Progress Tracking
- [x] Phase 1: Analysis and Setup ✅
- [x] Phase 2: Core CLI Framework Migration ✅
- [x] Phase 3: Command Migration - Basic Commands ✅
  - [x] info_app
  - [x] login_app
  - [x] logout_app
  - [x] whoami_app
- [ ] Phase 3: Command Migration - User Management 🔄
- [ ] Phase 3: Command Migration - Workspace Management
- [ ] Phase 3: Command Migration - Dataset Management
- [ ] Phase 3: Command Migration - Advanced Functionality
- [ ] Phase 4: Integration and Testing
- [ ] Phase 5: Documentation and Finalization

## Implementation Plan for Next Steps

### Phase 3: Command Migration - Next Steps
1. ✅ Basic Commands
   - ✅ `info_app`: Server information commands
   - ✅ `login_app`: Authentication commands
   - ✅ `logout_app`: Logout functionality
   - ✅ `whoami_app`: User identification

2. 🔄 User Management Commands (`users_app`)
   - [ ] Examine v1 implementation in `argilla-v1/src/argilla_v1/cli/users`
   - [ ] Implement user creation
   - [ ] Implement user listing
   - [ ] Implement user update
   - [ ] Implement user deletion
   - [ ] Write tests for user management commands