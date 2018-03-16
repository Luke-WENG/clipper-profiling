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

## Docker Image Remove
sudo docker rm $(sudo docker ps -a -q)
sudo docker rmi $(sudo docker images -q)

## List Docker status
docker stats
docker stats --all --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
> https://docs.docker.com/engine/reference/commandline/stats/

## Limit Docker's Resources
docker run --it --cpu-rt-runtime=950000 \
                --ulimit rtprio=99 \
                --cap-add=sys_nice \
                debian:jessie
> https://docs.docker.com/config/containers/resource_constraints/

## Resize Docker's Resources on the fly
docker update -m 30m <CONTAINER_ID>
docker update --cpus 1.5 <CONTAINER_ID>
docker update --cpu-shares 1024 <CONTAINER_ID> # default: 1024

> https://docs.docker.com/engine/reference/commandline/update/

cd /sys/fs/cgroup/memory/docker/<target_docker_ID>/<cpu or memory>/docker/
> https://groups.google.com/forum/#!msg/docker-user/1CvdT-dcDkQ/Zkp5TAel0tYJ