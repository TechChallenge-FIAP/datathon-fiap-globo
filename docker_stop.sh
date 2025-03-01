#!/bin/bash
echo "Parando a API..."
sudo docker stop container_api
sudo docker rm container_api

echo "Processo concluído."
