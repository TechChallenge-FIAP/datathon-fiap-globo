#!/bin/bash
unzip datathon_zip/challenge-webmedia-e-globo-2023.zip -d datathon_zip

mkdir -p data/paginas
mkdir -p data/users

mv datathon_zip/itens/itens/* data/paginas/
mv datathon_zip/files/treino/* data/users/

chmod +x docker_stop.sh

bash -c "sudo docker compose build"
bash -c "sudo docker compose up -d"
