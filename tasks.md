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

#### Basic Commands ✅
- [x] `info_app`: Server information commands
- [x] `login_app`: Authentication commands
- [x] `logout_app`: Logout functionality
- [x] `whoami_app`: User identification

#### User Management ✅
- [x] `users_app`: User management commands
  - [x] Create user
  - [x] List users
  - [x] Delete user

#### Workspace Management ✅
- [x] `workspaces_app`: Workspace management
  - [x] Create workspace
  - [x] List workspaces
  - [x] Add user to workspace
  - [x] Remove user from workspace

#### Dataset Management ✅
- [x] `datasets_app`: Dataset operations
  - [x] Create dataset
  - [x] List datasets
  - [x] Delete dataset
  - [x] Push to HuggingFace Hub

#### Advanced Functionality
- [ ] `training_app`: Model training commands 🔄
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
- [x] Phase 3: Command Migration - User Management ✅
- [x] Phase 3: Command Migration - Workspace Management ✅
- [x] Phase 3: Command Migration - Dataset Management ✅
- [ ] Phase 3: Command Migration - Advanced Functionality 🔄
- [ ] Phase 4: Integration and Testing
- [ ] Phase 5: Documentation and Finalization

## Implementation Plan for Next Steps

### Phase 3: Command Migration - Next Steps
1. ✅ Basic Commands
   - ✅ `info_app`: Server information commands
   - ✅ `login_app`: Authentication commands
   - ✅ `logout_app`: Logout functionality
   - ✅ `whoami_app`: User identification

2. ✅ User Management Commands (`users_app`)
   - [x] Implement user creation
   - [x] Implement user listing
   - [x] Implement user deletion
   - [x] Write tests for user management commands

3. ✅ Workspace Management Commands (`workspaces_app`)
   - [x] Implement workspace creation
   - [x] Implement workspace listing
   - [x] Implement adding users to workspaces
   - [x] Implement removing users from workspaces

4. ✅ Dataset Management Commands (`datasets_app`)
   - [x] Implement dataset creation
   - [x] Implement dataset listing
   - [x] Implement dataset deletion
   - [x] Implement push to HuggingFace Hub

5. 🔄 Advanced Functionality
   - [ ] Examine v1 implementation in `argilla-v1/src/argilla_v1/cli/training`
   - [ ] Implement training commands
   - [ ] Examine v1 implementation in `argilla-v1/src/argilla_v1/cli/extraction`
   - [ ] Implement extraction commands
   - [ ] Examine v1 implementation in `argilla-v1/src/argilla_v1/cli/schemas`
   - [ ] Implement schema management commands