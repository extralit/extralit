# Extralit Repository Overview

## Repository Structure

The Extralit repository contains several components:

- `argilla-server`: The backend server component
- `argilla-frontend`: The frontend web application
- `argilla`: The Python client library
- `argilla-v1`: The new version of the Python client library

## Issue #70 Fix

This PR addresses the failing unit tests in the `argilla-server` component. There were two main issues:

1. Schema changes in text fields and text questions settings:
   - A new property `use_table` was added with a default value of `False`
   - The test expectations needed to be updated to include this property

2. Workspace-related endpoints returning 500 errors:
   - The error handling in the `delete_workspace` endpoint needed to be improved
   - Added proper error handling for unexpected exceptions

### Changes Made

1. Updated test parametrization in `test_create_dataset_field.py` to include the `use_table` property in the expected settings
2. Added a new test case for when `use_table` is explicitly set to `True`
3. Improved error handling in the `delete_workspace` endpoint to properly handle unexpected exceptions

These changes should fix the 21 failing tests in the CI pipeline.