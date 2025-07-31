#!/bin/bash
CURRENT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source "$CURRENT_DIR/.env"
source "$COMPOSE_HOME/.env"

cd "$CURRENT_DIR/$COMPOSE_HOME"

docker-compose -f airflow-compose.yaml down --remove-orphans

docker-compose -f database-compose.yaml down --remove-orphans

docker volume ls | grep "$POSTGRES_VOLUME"

docker image rm airflow -f
docker image rm airflow/airflow-ufes -f
docker image rm airflow:$VERSION

docker build -t airflow:$VERSION -f "airflow-dockerfile" .
docker tag airflow:$VERSION airflow/airflow-ufes:$VERSION
docker tag airflow:$VERSION airflow/airflow-ufes:latest

docker network rm $NETWORK
docker network create $NETWORK

docker-compose -f airflow-compose.yaml up -d

docker-compose -f database-compose.yaml up -d

cd "$CURRENT_DIR"