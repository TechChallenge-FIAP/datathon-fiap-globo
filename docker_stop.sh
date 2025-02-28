#!/bin/bash
echo "Parando a API..."
docker stop container_api
docker rm container_api

echo "Processo concluído."
