#!/bin/bash
CURRENT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source "$CURRENT_DIR/.env"
source "$COMPOSE_HOME/.env"

# Validate required environment variables
required_vars=("COMPOSE_HOME" "POSTGRES_VOLUME" "VERSION" "NETWORK")
for var in "${required_vars[@]}"; do
    if [[ -z "${!var}" ]]; then
        echo "Error: Required environment variable $var is not set"
        exit 1
    fi
done

cd "$CURRENT_DIR/$COMPOSE_HOME" || { echo "Failed to change to compose directory"; exit 1; }

docker-compose -f airflow-compose.yaml down --remove-orphans

docker-compose -f database-compose.yaml down --remove-orphans

docker volume ls | grep "$POSTGRES_VOLUME"

docker image rm airflow -f
docker image rm airflow/airflow-ufes -f
docker image rm airflow:$VERSION

docker build -t airflow:$VERSION -f "airflow-dockerfile" .
docker tag airflow:$VERSION airflow/airflow-ufes:$VERSION
docker tag airflow:$VERSION airflow/airflow-ufes:latest

# Remove network if it exists
docker network rm "$NETWORK" 2>/dev/null || true

# Create network
if ! docker network create "$NETWORK"; then
    echo "Failed to create Docker network: $NETWORK"
    exit 1
fi

docker-compose -f airflow-compose.yaml up -d

docker-compose -f database-compose.yaml up -d

cd "$CURRENT_DIR" || { echo "Failed to return to original directory"; exit 1; }
