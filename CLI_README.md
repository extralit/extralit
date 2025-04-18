# Extralit CLI

The Extralit CLI provides a command-line interface for interacting with the Extralit platform. It allows you to manage workspaces, datasets, schemas, and more.

## Installation

The Extralit CLI is included with the Extralit Python package. You can install it using pip:

```bash
pip install extralit
```

## Authentication

Before using the CLI, you need to authenticate with the Extralit server:

```bash
extralit login --api-url http://your-extralit-server --api-key your-api-key
```

You can check your authentication status with:

```bash
extralit whoami
```

And log out with:

```bash
extralit logout
```

## Commands

### Info

Get information about the Extralit server:

```bash
extralit info
```

### Workspaces

List workspaces:

```bash
extralit workspaces list
```

Create a new workspace:

```bash
extralit workspaces create --name my-workspace --description "My workspace description"
```

Add a user to a workspace:

```bash
extralit workspaces --name my-workspace add-user --username user1 --role admin
```

Remove a user from a workspace:

```bash
extralit workspaces --name my-workspace delete-user --username user1
```

### Datasets

List datasets:

```bash
extralit datasets --workspace my-workspace list
```

Create a new dataset:

```bash
extralit datasets --workspace my-workspace create --name my-dataset --description "My dataset description"
```

Delete a dataset:

```bash
extralit datasets --workspace my-workspace delete --name my-dataset
```

Push a dataset to HuggingFace Hub:

```bash
extralit datasets --workspace my-workspace push-to-hub --name my-dataset --repo-id username/repo-name
```

### Schemas

List schemas:

```bash
extralit schemas --workspace my-workspace list
```

Upload schemas:

```bash
extralit schemas --workspace my-workspace upload path/to/schemas --overwrite
```

Delete a schema:

```bash
extralit schemas --workspace my-workspace delete schema-id
```

### Training

Train a model:

```bash
extralit training --name my-dataset --framework spacy --model en_core_web_sm
```

With additional options:

```bash
extralit training --name my-dataset --framework transformers --model bert-base-uncased --workspace my-workspace --train-size 0.8 --seed 42 --device 0 --output-dir models/my-model
```

### Extraction

Export extraction data:

```bash
extralit extraction --workspace my-workspace --env-file .env export --output exports
```

With type filter:

```bash
extralit extraction --workspace my-workspace --env-file .env export --type text_classification --output exports
```

### Users

List users:

```bash
extralit users list
```

Create a new user:

```bash
extralit users create --username user1 --password password123 --full-name "User One" --email user1@example.com
```

Delete a user:

```bash
extralit users delete --username user1
```

## Environment Variables

The Extralit CLI respects the following environment variables:

- `EXTRALIT_API_URL`: The URL of the Extralit server
- `EXTRALIT_API_KEY`: Your API key for authentication

## Configuration

The CLI stores configuration in `~/.extralit/config.json`. You can edit this file directly if needed.

## Troubleshooting

### Authentication Issues

If you're having trouble authenticating, try:

1. Checking that your API key is correct
2. Ensuring the server URL is correct and accessible
3. Logging out and logging in again

### Command Failures

If a command fails, check:

1. That you're authenticated
2. That you have the necessary permissions
3. That the resources you're trying to access exist

For more detailed error information, you can add the `--debug` flag to any command.

## API Differences Between v1 and v2

For information about API differences between Argilla v1 and v2 that affect the CLI, see [API_DIFFERENCES.md](API_DIFFERENCES.md).

## Contributing

For information about contributing to the Extralit CLI, see [CONTRIBUTING.md](CONTRIBUTING.md).
