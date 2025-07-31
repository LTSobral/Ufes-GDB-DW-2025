#!/bin/bash
CURRENT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source "$CURRENT_DIR/.env"
source "$COMPOSE_HOME/.env"

cd "$CURRENT_DIR/$COMPOSE_HOME"

docker-compose -f airflow-compose.yaml down --remove-orphans

docker-compose -f database-compose.yaml down --remove-orphans