# Argilla v2 Test Server

This directory contains the configuration for running a local Argilla v2 server for testing the Extralit CLI.

## Starting the Server

To start the server, run the following command from this directory:

```bash
docker compose up -d
```

This will start the Argilla server and all required services (PostgreSQL, Elasticsearch, and Redis) in the background.

## Accessing the Server

Once the server is running, you can access it at:

- **URL**: http://localhost:6900
- **Username**: argilla
- **Password**: argilla12345678
- **API Key**: argilla.apikey
- **Workspace**: default

## Stopping the Server

To stop the server, run:

```bash
docker compose down
```

To stop the server and remove all data (volumes), run:

```bash
docker compose down -v
```

## Checking Server Status

To check the status of the server, run:

```bash
docker compose ps
```

To view the logs, run:

```bash
docker compose logs -f
```

## Using with Extralit CLI

To use this server with the Extralit CLI, you can log in with:

```bash
extralit login --api-url http://localhost:6900 --api-key argilla.apikey
```
