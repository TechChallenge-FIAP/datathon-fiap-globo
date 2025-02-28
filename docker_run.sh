#!/bin/bash

echo "Construindo as imagens Docker..."
docker build -t imagem_preprocessamento -f Dockerfile.preprocess .
docker build -t imagem_treinamento -f Dockerfile.train .
docker build -t imagem_api -f Dockerfile.api .

echo "Executando o Pré-processamento..."
docker rm container_preprocessamento
docker run --rm --name container_preprocessamento -v "$(pwd):/app" imagem_preprocessamento

echo "Executando o Treinamento do Modelo..."
docker rm container_treinamento
docker run --rm --name container_treinamento -v "$(pwd):/app" imagem_treinamento

echo "Iniciando a API..."
docker rm container_api
docker run -d --name container_api -p 8000:8000 -v "$(pwd):/app" imagem_api
