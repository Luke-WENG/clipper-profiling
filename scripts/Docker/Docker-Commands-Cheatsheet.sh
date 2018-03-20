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
docker update --memory 30m <CONTAINER_ID>
docker update --memory 30m --memory-swap 60m <CONTAINER_ID>
docker update --cpus 1.5 <CONTAINER_ID>
docker update --cpu-shares 1024 <CONTAINER_ID> # default: 1024

> https://docs.docker.com/engine/reference/commandline/update/
# Adjust memory and swap accounting
# When users run Docker, they may see these messages when working with an image:
#
# WARNING: Your kernel does not support cgroup swap limit. WARNING: Your
# kernel does not support swap limit capabilities. Limitation discarded.
# To prevent these messages, enable memory and swap accounting on your system. To enable these on system using GNU GRUB (GNU GRand Unified Bootloader), do the following.
#
# Log into Ubuntu as a user with sudo privileges.
#
# Edit the /etc/default/grub file.
#
# Set the GRUB_CMDLINE_LINUX value as follows:
#
# GRUB_CMDLINE_LINUX="cgroup_enable=memory swapaccount=1"
# Save and close the file.
#
# Update GRUB.
#
# $ sudo update-grub
# Reboot your system.

cd /sys/fs/cgroup/memory/docker/<target_docker_ID>/<cpu or memory>/docker/
> https://groups.google.com/forum/#!msg/docker-user/1CvdT-dcDkQ/Zkp5TAel0tYJ