# API Differences Between Argilla v1 and v2

This document tracks the API differences between Argilla v1 and v2 that affect the CLI functionality.

## Authentication

### v1 Authentication
- Used a simple API key for authentication
- API key was passed in the `X-API-Key` header

### v2 Authentication
- Uses a more complex authentication system with JWT tokens
- API key is used to obtain a token, which is then used for subsequent requests
- Token is passed in the `Authorization` header with the `Bearer` prefix

## Workspaces

### v1 Workspaces
- Workspaces were simple containers for datasets
- Limited metadata and permissions

### v2 Workspaces
- Workspaces have more metadata and permissions
- Users can be assigned different roles within a workspace

## Datasets

### v1 Datasets
- Datasets were tied to a specific task type (text classification, token classification, etc.)
- Limited metadata

### v2 Datasets
- Datasets are more flexible and can be used for multiple task types
- More metadata and configuration options

## Schemas

### v1 Schemas
- No explicit schema management
- Schema was defined as part of the dataset creation

### v2 Schemas
- Explicit schema management with versioning
- Schemas can be shared across datasets

## Training

### v1 Training
- Training was tightly integrated with the dataset
- Limited configuration options

### v2 Training
- Training is more flexible and can be configured separately from the dataset
- More configuration options and frameworks supported

## Extraction

### v1 Extraction
- Limited extraction capabilities
- No explicit extraction pipeline

### v2 Extraction
- Enhanced extraction capabilities with a dedicated pipeline
- Support for more document types and extraction methods

## Issues and Workarounds

### Authentication Issues
- **Issue**: The v2 server requires a different authentication method
- **Workaround**: Implemented a flexible authentication system that tries different methods

### Schema Management Issues
- **Issue**: The v2 API for schema management is different from v1
- **Workaround**: Updated the schema management commands to use the v2 API

### Training Issues
- **Issue**: The v2 API for training is different from v1
- **Workaround**: Updated the training commands to use the v2 API

### Extraction Issues
- **Issue**: The v2 API for extraction is different from v1
- **Workaround**: Updated the extraction commands to use the v2 API
