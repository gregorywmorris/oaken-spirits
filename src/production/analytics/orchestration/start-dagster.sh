#!/bin/bash

# Check if Docker containers are running
if docker ps -f "name=oaken-mysql" --format '{{.Names}}' | grep -q "oaken-mysql"; then
    echo "Container 'oaken-mysql' is running."
else
    echo "Container 'oaken-mysql' is not running. Please start it first."
    exit 1
fi

if docker ps -f "name=airbyte-webapp" --format '{{.Names}}' | grep -q "airbyte-webapp"; then
    echo "Container 'airbyte-webapp' is running."
else
    echo "Container 'airbyte-webapp' is not running. Please start it first."
    exit 1
fi

# Start Dagster service

export DAGSTER_DBT_PARSE_PROJECT_ON_LOAD=1

cd dagster/

dagster dev