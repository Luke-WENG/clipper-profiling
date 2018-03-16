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
cd /sys/fs/cgroup/memory/docker/<target_docker_ID>/<cpu or memory>/docker/
105488384 # 100.6015625 MB 31457280
> https://groups.google.com/forum/#!msg/docker-user/1CvdT-dcDkQ/Zkp5TAel0tYJ