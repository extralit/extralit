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

### Phase 3: Command Migration (Days 5-12) ✅
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

#### Advanced Functionality ✅
- [x] `training_app`: Model training commands
- [x] `extraction_app`: Extraction pipeline commands
- [x] `schemas_app`: Schema management

### Phase 4: Integration and Testing (Days 13-15) 🔄
- [x] Integrate all command modules with main CLI app
- [x] Write comprehensive tests for each command
  - [x] Test core app functionality and registration
  - [x] Test workspace management commands ✅ (Fixed on April 14, 2025)
  - [x] Test dataset management commands
  - [x] Test user management commands ✅ (Added on April 15, 2025)
  - [x] Test schema management commands ✅ (Fixed on April 15, 2025)
  - [x] Test training and extraction commands ✅ (Fixed on April 15, 2025)
- [ ] Test with actual Argilla v2 server
- [ ] Fix any compatibility issues
- [ ] Document any API differences between v1 and v2
- [ ] Implement comprehensive error handling and logging
  - [ ] Create consistent error handling patterns across all commands
  - [ ] Add detailed logging for debugging purposes
  - [ ] Implement user-friendly error messages
- [ ] Add shell completion support for commands
  - [ ] Implement completion for command names
  - [ ] Implement completion for command options
  - [ ] Test completion in different shell environments
- [ ] Implement command aliases for backward compatibility
  - [ ] Map v1 command names to v2 command names
  - [ ] Ensure parameter compatibility between versions
- [ ] Add versioning strategy for CLI commands
  - [ ] Implement version command to show CLI version
  - [ ] Add deprecation warnings for commands that will change in future

### Phase 5: Documentation and Finalization (Days 16-18)
- [ ] Update CLI documentation
  - [ ] Update main README with CLI installation and usage
  - [ ] Update command-specific documentation
- [ ] Create migration guide for users coming from v1
  - [ ] Document command mapping between v1 and v2
  - [ ] Highlight breaking changes and new features
- [ ] Add examples for common CLI usage patterns
  - [ ] Create example scripts for common workflows
  - [ ] Add examples to documentation
- [ ] Final testing and bug fixes
  - [ ] Perform end-to-end testing of all commands
  - [ ] Fix any remaining issues
- [ ] Prepare pull request
  - [ ] Create comprehensive PR description
  - [ ] Address reviewer feedback
- [ ] Add detailed help text for all commands
- [ ] Create command reference documentation
- [ ] Document error handling and logging
- [ ] Document shell completion setup
- [ ] Document command aliases and versioning

## Implementation Notes

### Key Challenges
1. **API Differences**: The v2 API may differ from v1, requiring command adaptation
2. **Import Structure**: All imports need to be updated from `argilla_v1` to `argilla`
3. **Dependencies**: Some v1 CLI features might depend on v1-specific functionality
4. **Testing**: Ensuring commands work correctly with the v2 backend
5. **Error Handling**: Implementing comprehensive error handling and logging
6. **Backward Compatibility**: Maintaining compatibility with v1 commands through aliases
7. **Documentation**: Creating clear and comprehensive documentation for users
8. **API Compatibility Layer**: Creating a layer to handle differences between v1 and v2 APIs
9. **Configuration Management**: Handling configuration files and environment variables
10. **Performance**: Ensuring CLI commands perform well with large datasets

### Implementation Strategy
- Port one module at a time, starting with simpler commands
- Test each module thoroughly before moving to the next
- Keep the same command structure where possible for backward compatibility
- Document any necessary changes to command syntax or behavior
- Replace all mock implementations with real API calls
- Ensure proper error handling for all API interactions

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
- [x] Phase 3: Command Migration - Advanced Functionality ✅
- [x] Phase 4: Integration and Testing - Main app integration ✅
- [x] Phase 4: Integration and Testing - Initial command testing ✅
- [x] Phase 4: Integration and Testing - Complete test coverage ✅
- [ ] Phase 4: Integration and Testing - Live server testing 🔄
- [ ] Phase 5: Documentation and Finalization

## Next Steps

### API Integration (Priority 1)
1. Create API compatibility layer:
   - [x] Implement proper `ArgillaCredentials` class
   - [x] Complete the `init_callback()` function in callback.py
   - [x] Create basic API client for CLI commands
   - [x] Implement authentication and token handling

2. Replace mock implementations with real API calls:
   - [x] Update login and logout commands to use real implementation
   - [x] Update info command to use client implementation
   - [x] Update whoami command to use client implementation
   - [x] Update datasets module to use real API calls
   - [ ] Update users module to use real API calls
   - [ ] Update workspaces module to use real API calls
   - [ ] Update extraction module to use real API calls
   - [ ] Update schemas module to use real API calls
   - [ ] Update training module to use real API calls

### Live Server Testing (Priority 2)
1. Set up testing environment:
   - [ ] Set up a local Argilla v2 server for testing
   - [ ] Configure test data and users

2. Test all command modules:
   - [ ] Test all commands against the live server
   - [ ] Document any API compatibility issues
   - [ ] Fix any issues found during testing

3. Error Handling and Logging:
   - [ ] Implement consistent error handling across all commands
   - [ ] Add proper logging for debugging purposes
   - [ ] Create user-friendly error messages

4. Command Completion and Aliases:
   - [ ] Implement shell completion for commands and options
   - [ ] Add command aliases for backward compatibility
   - [ ] Test completion in different environments

### Documentation
1. Update CLI documentation:
   - [ ] Create comprehensive command reference
   - [ ] Document new features and improvements
   - [ ] Update installation instructions
   - [ ] Add troubleshooting section

2. Create migration guide:
   - [ ] Document differences between v1 and v2 CLI
   - [ ] Provide examples for common use cases
   - [ ] Create upgrade path instructions
   - [ ] Document command mapping between versions

## Recent Progress

### April 15, 2025
- Added comprehensive test files for remaining CLI commands:
  - Created `test_users.py` with tests for user management commands
  - Created `test_schemas.py` with tests for schema management commands
  - Created `test_training.py` with tests for training commands
  - Created `test_extraction.py` with tests for extraction commands
- Fixed mocking issues in tests by updating patch statements to use correct import paths
- Fixed assertion issues in user management tests
- Fixed schema management command tests by updating command structure and mocking
- Fixed training command tests by updating assertions
- Fixed extraction command tests by updating command structure and assertions
- All CLI command tests are now passing successfully
- Updated tasks.md to reflect progress

### April 14, 2025
- Fixed issues with workspace commands tests:
  - Updated `test_workspaces_add_user_command_help` and `test_workspaces_delete_user_command_help` tests to include the required `--name` parameter before the command name
  - Fixed the mock data in `test_workspaces_list` to use proper datetime objects instead of strings
  - Updated the mocking approach in `test_workspaces_create`, `test_workspaces_add_user`, and `test_workspaces_delete_user` to correctly test the command functionality
- All workspace management command tests are now passing successfully