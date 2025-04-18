# CLI Commands Documentation

This document describes the CLI commands available in Argilla V2.

## File Operations

### List Files

List files in a workspace.

```bash
argilla files list --workspace <workspace_name> [--path <path>] [--recursive/--no-recursive] [--include-version/--no-include-version]
```

Options:
- `--workspace`, `-w`: Workspace name (required)
- `--path`, `-p`: Path prefix to filter files (default: "")
- `--recursive/--no-recursive`: List files recursively (default: recursive)
- `--include-version/--no-include-version`: Include version information (default: include)

Example:
```bash
argilla files list --workspace my-workspace --path documents/
```

### Upload File

Upload a file to a workspace.

```bash
argilla files upload <file_path> --workspace <workspace_name> [--remote-path <remote_path>] [--overwrite]
```

Arguments:
- `file_path`: Path to the file to upload (required)

Options:
- `--workspace`, `-w`: Workspace name (required)
- `--remote-path`, `-r`: Remote path to store the file (default: same as local filename)
- `--overwrite`, `-o`: Overwrite existing file (default: False)

Example:
```bash
argilla files upload data.csv --workspace my-workspace --remote-path data/data.csv
```

### Download File

Download a file from a workspace.

```bash
argilla files download <remote_path> --workspace <workspace_name> [--output <output_path>] [--version-id <version_id>] [--overwrite]
```

Arguments:
- `remote_path`: Remote path of the file to download (required)

Options:
- `--workspace`, `-w`: Workspace name (required)
- `--output`, `-o`: Local path to save the file (default: same as remote filename)
- `--version-id`, `-v`: Version ID of the file to download
- `--overwrite`: Overwrite existing file (default: False)

Example:
```bash
argilla files download data/data.csv --workspace my-workspace --output ./downloaded_data.csv
```

### Delete File

Delete a file from a workspace.

```bash
argilla files delete <remote_path> --workspace <workspace_name> [--version-id <version_id>] [--force]
```

Arguments:
- `remote_path`: Remote path of the file to delete (required)

Options:
- `--workspace`, `-w`: Workspace name (required)
- `--version-id`, `-v`: Version ID of the file to delete
- `--force`, `-f`: Force deletion without confirmation (default: False)

Example:
```bash
argilla files delete data/data.csv --workspace my-workspace --force
```

## Document Operations

### List Documents

List documents in a workspace.

```bash
argilla documents list --workspace <workspace_name>
```

Options:
- `--workspace`, `-w`: Workspace name (required)

Example:
```bash
argilla documents list --workspace my-workspace
```

### Add Document

Add a document to a workspace.

```bash
argilla documents add --workspace <workspace_name> [--file <file_path>] [--url <url>] [--pmid <pmid>] [--doi <doi>]
```

Options:
- `--workspace`, `-w`: Workspace name (required)
- `--file`, `-f`: Path to the document file
- `--url`, `-u`: URL of the document
- `--pmid`, `-p`: PubMed ID of the document
- `--doi`, `-d`: DOI of the document

Note: At least one of `--file`, `--url`, `--pmid`, or `--doi` must be provided.

Example:
```bash
argilla documents add --workspace my-workspace --url https://example.com/document.pdf
```

### Delete Document

Delete a document from a workspace.

```bash
argilla documents delete <document_id> --workspace <workspace_name> [--force]
```

Arguments:
- `document_id`: ID of the document to delete (required)

Options:
- `--workspace`, `-w`: Workspace name (required)
- `--force`, `-f`: Force deletion without confirmation (default: False)

Example:
```bash
argilla documents delete 123e4567-e89b-12d3-a456-426614174000 --workspace my-workspace --force
```

Note: Document deletion is not yet implemented in the API.

## Schema Operations

### List Schemas

List schemas in a workspace.

```bash
argilla schemas list --workspace <workspace_name>
```

Options:
- `--workspace`, `-w`: Workspace name (required)

Example:
```bash
argilla schemas list --workspace my-workspace
```

### Upload Schemas

Upload schemas to a workspace.

```bash
argilla schemas upload <directory> --workspace <workspace_name> [--overwrite] [--exclude <schema_name>...]
```

Arguments:
- `directory`: Directory containing schema files (required)

Options:
- `--workspace`, `-w`: Workspace name (required)
- `--overwrite`, `-o`: Overwrite existing schemas (default: False)
- `--exclude`, `-e`: List of schema names to exclude from upload

Example:
```bash
argilla schemas upload ./schemas --workspace my-workspace --overwrite
```

### Download Schemas

Download schemas from a workspace.

```bash
argilla schemas download <directory> --workspace <workspace_name> [--name <name>] [--exclude <schema_name>...] [--overwrite]
```

Arguments:
- `directory`: Directory to save the downloaded schemas (required)

Options:
- `--workspace`, `-w`: Workspace name (required)
- `--name`, `-n`: Filter schemas by name
- `--exclude`, `-e`: List of schema names to exclude from download
- `--overwrite`, `-o`: Overwrite existing schema files (default: False)

Example:
```bash
argilla schemas download ./downloaded_schemas --workspace my-workspace
```

## Shell Completion

Argilla CLI supports shell completion for Bash, Zsh, and Fish shells.

### Bash

Add the following to your `~/.bashrc` file:

```bash
eval "$(argilla --completion bash)"
```

### Zsh

Add the following to your `~/.zshrc` file:

```bash
eval "$(argilla --completion zsh)"
```

### Fish

Add the following to your `~/.config/fish/config.fish` file:

```fish
argilla --completion fish | source
```

## Command Aliases

Argilla CLI supports command aliases for frequently used commands.

### Creating an Alias

You can create an alias by adding it to your shell configuration file:

```bash
# Bash/Zsh
alias arl="argilla"
alias arlf="argilla files"
alias arld="argilla documents"
alias arls="argilla schemas"

# Fish
alias arl "argilla"
alias arlf "argilla files"
alias arld "argilla documents"
alias arls "argilla schemas"
```

## Versioning

Argilla CLI follows semantic versioning. You can check the version with:

```bash
argilla --version
```
