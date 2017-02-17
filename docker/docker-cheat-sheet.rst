Docker cheat sheet
==================

This is not a HOWTO. It is only a cheat sheet to remind common procedures.
It only intends to be a personal help guide (for pesonal use). If you are going to
use it, please bear in mind, that I am not a Docker expert :)


Instalation and configuration
-----------------------------

Archlinux:
~~~~~~~~~~

::

    $ sudo pacman -S docker

Start and Enable the service

::

    $ sudo systemctl start docker.service
    $ sudo systemctl enable docker.service
    $ sudo docker info


The Docker daemon
~~~~~~~~~~~~~~~~~

By default, the daemon listens on a Unix socket at `/var/run/docker.sock` for incoming Docker
requests. If a group named docker exists on our system, Docker will apply ownership of the socket
to that group. Hence, any user that belongs to the docker group can run Docker without needing
to use the sudo command. So if you want to be able to run docker as a regular user,
add yourself to the docker group:

::

    $ sudo gpasswd -a user docker
    $ sudo newgrp docker


Storage driver
~~~~~~~~~~~~~~

Storage driver, a.k.a. graph driver has huge impact on performance. Its job is to store layers
of container images efficiently, that is when several images share a layer, only one layer uses
disk space. The default, most compatible option, `devicemapper` offers suboptimal performance,
which is outright terrible on rotating disks. Additionally, `devicemappper` is not recommended
in production. As Arch linux ships new kernels, there's no point using the compatibility option.
A good, modern choice is `overlay2`. To see current storage driver, run:

::

    $ docker info | head

To set your own choice of storage driver, create a Drop-in snippet and use -s option to dockerd:

::

   /etc/systemd/system/docker.service.d/override.conf

   [Service]
   ExecStart=
   ExecStart=/usr/bin/dockerd -H fd:// -s overlay2

Recall that `ExecStart=` line is needed to drop inherited ExecStart.


Working with containers
-----------------------

Running a container
~~~~~~~~~~~~~~~~~~~

`docker run` command will create a new container. 

::

    $ docker run [OPTIONS] IMAGE [COMMAND] [ARG...]

So for example:

::

    $ docker run -i -t ubuntu /bin/bash

* **-i**: flag keeps STDIN open from the container, even if we're not attached to it.
This persistent standard input is one half of what we need for an interactive shell. 

* **-t**: flag is the other half and tells Docker to assign a pseudo-tty to the container
we're about to create.

* **ubuntu**: is the *image* to use to create a container. The ubuntu image is a stock image,
also known as a "base" image, provided by Docker, Inc., on the Docker Hub registry. You can use
base images like the ubuntu base image (and the similar fedora , debian , centos , etc., images)
as the basis for building your own images on the operating system of your choice.


If Docker can't find the image on your local Docker host, it will
reach out to the Docker Hub registry run by Docker, Inc., and look for it there.
Once Docker find the image, it'll download the image and store it on the local host.

You can list all local store image with:

::

   $ docker image

Docker uses this image to create a new container inside a filesystem. The container has a network
with an IP address, and a bridge interface to talk to the local host.


**/bin/bash**: is command to run in our new container, in this case launching a Bash shell with
the /bin/bash command.


Listing Docker containers
~~~~~~~~~~~~~~~~~~~~~~~~~

List running containers

::

    $ docker ps

Show all containers, both stopped and running:

::

   $ docker ps -a


Container naming
~~~~~~~~~~~~~~~~

Docker will automatically generate a name at random for each container we create.
If we want to specify a particular container name in place of the automatically generated name,
we can do so using the `--name` flag:

::

    $ docker run --name foo_bar_container -i -t ubuntu /bin/bash


Starting, stopping and deleting containers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To start a stopped container:

::

   $ docker start CONTAINER ...

Stop one or more running containers:

::

   $ docker stop CONTAINER ...


Attaching to a running containe:   

::

    $ docker attach CONTAINER


Deleting a container:

::

    $ docker rm CONTAINER


Daemonized containers
~~~~~~~~~~~~~~~~~~~~~

Daemonized containers don't have an interactive session. And are ideal for running
applications and services.

::

    $ docker run --name daemon_container -d ubuntu /bin/sh -c "while true; do echo hello world; sleep 1; done"


Container logging
~~~~~~~~~~~~~~~~~

To see the output of a container, you can run:

::

    $ docker logs [CONTAINER]


To see the output added in real-time, use `-f`

::

   $ docker logs -f [CONTAINER]


Journald logging driver
~~~~~~~~~~~~~~~~~~~~~~~

The journald logging driver sends container logs to the systemd journal. Log entries can be retrieved
using the journalctl command, through use of the journal API, or using the docker logs command.

Configure the default logging driver by passing the --log-driver option to the Docker daemon:

::

    $ dockerd --log-driver=journald

or edit the `/etc/systemd/system/docker.service.d/override.conf` like this:

::

   [Service]
   ExecStart=
   ExecStart=/usr/bin/dockerd -H fd:// -s overlay2 --log-driver=journald



To configure the logging driver for a specific container, use the `--log-driver` flag on the docker run command.

::

   $ docker run --log-driver=journald ...
   $ sudo journalctl -u docker CONTAINER_NAME=container_name


Inspecting processes inside a container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see processes running inside the container:

::

   $ docker top CONTAINER

   $ docker stats
   $ docker stats CONTAINER


Automatic container restarts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to configure Docker to restart automatically a container if it fails
You have to run the container with the `--restart` flag.

The `--restart` flag checks for the container exit code and makes a decision whether
or not to restart it. The default behavior is to not restart containers at all.

So for example:

::

    $ docker run --restart=always ...

    
It will try to restart the container no matter what exit code is returned. Alternatively, we can
specify a value of `on-failure` which restarts the container if it exits with a non-zero exit code:

::

    $ docker run --restart=on-failure:5 ...


It will restart a maximum of 5 times if a non-zero exit code is received.


Docker images
-------------

Images live inside repositories, and repositories live on registries. The default registry is the public registry
managed by Docker, Inc., Docker Hub.

Each repository can contain multiple images (e.g., the ubuntu repository contains
images for Ubuntu 12.04, 12.10, 13.04, 13.10, 14.04, 16.04)

Pulling images
~~~~~~~~~~~~~~

`docker pull` command pulls down the image from the ubuntu repository to the local host

::

    $ docker pull ubuntu:16.04
    $ docker pull ubuntu:latest


Listing images
~~~~~~~~~~~~~~

List images available in the Docker host:

::

    $ docker images


Searching for images
~~~~~~~~~~~~~~~~~~~~
To search all of the publicly available images on Docker Hub, run:

::

    $ docker search httpd


Building images
~~~~~~~~~~~~~~~

There are two ways to create personal images in Docker:

- using docker commit
- using docker build with a Dockerfile

It's not recommended to use the docker commit approach. Instead, it's recommend to
build images using a definition file called Dockerfile and then `docker build` command.
The Dockerfile uses a basic DSL (Domain Specific Language) with instructions for building Docker images.
Once we have a Dockerfile we then use the `docker build` command to build a new image from
the instructions in the Dockerfile.


