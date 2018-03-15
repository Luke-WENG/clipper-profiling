## List Docker CLI commands
docker
docker container --help

## List Docker Container Information (running, all, all show SIZE)
docker ps
docker ps -a
docker ps -a -s

## Display Docker version and info
docker --version
docker version
docker info

## Excecute Docker image
docker run hello-world

## List Docker images
docker image ls

## List Docker containers (running, all, all in quiet mode)
docker container ls
docker container ls --all
docker container ls -a -q