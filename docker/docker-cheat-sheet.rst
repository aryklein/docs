Docker cheat sheet
==================

.. contents::

This is not a HOWTO. It is only a cheat sheet to remind common procedures.
It only intends to be a personal help guide (for pesonal use). If you are going to
use it, please keep in mind, that I am not a Docker expert :)


Installation and configuration
-----------------------------

Archlinux:
~~~~~~~~~~

.. code-block:: bash

    $ sudo pacman -S docker

Start and Enable the service

.. code-block:: bash

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

.. code-block:: bash

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

.. code-block:: bash

    $ docker info | head

To set your own choice of storage driver, create a Drop-in snippet and use -s option to dockerd:

.. code-block:: bash

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

.. code-block:: bash

    $ docker run [OPTIONS] IMAGE [COMMAND] [ARG...]

So for example:

.. code-block:: bash

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

.. code-block:: bash

   $ docker images
   $ docker image ls

Docker uses this image to create a new container inside a filesystem. The container has a network
with an IP address, and a bridge interface to talk to the local host.


**/bin/bash**: is command to run in our new container, in this case launching a Bash shell with
the /bin/bash command.


Listing Docker containers
~~~~~~~~~~~~~~~~~~~~~~~~~

List running containers

.. code-block:: bash

    $ docker ps

Show all containers, both stopped and running:

.. code-block:: bash

   $ docker ps -a


Container naming
~~~~~~~~~~~~~~~~

Docker will automatically generate a name at random for each container we create.
If we want to specify a particular container name in place of the automatically generated name,
we can do so using the `--name` flag:

.. code-block:: bash

    $ docker run --name foo_bar_container -i -t ubuntu /bin/bash


Starting, stopping and deleting containers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To start a stopped container:

.. code-block:: bash

   $ docker start CONTAINER ...

Stop one or more running containers:

.. code-block:: bash

   $ docker stop CONTAINER ...


Attaching to a running containe:   

.. code-block:: bash

    $ docker attach CONTAINER

You can detach from a container and leave it running using the **CTRL-p CTRL-q** key sequence.


Deleting a container:

.. code-block:: bash

    $ docker rm CONTAINER


Daemonized containers
~~~~~~~~~~~~~~~~~~~~~

Daemonized containers don't have an interactive session. And are ideal for running
applications and services.

.. code-block:: bash

    $ docker run --name daemon_container -d ubuntu /bin/sh -c "while true; do echo hello world; sleep 1; done"


Container logging
~~~~~~~~~~~~~~~~~

To see the output of a container, you can run:

.. code-block:: bash

    $ docker logs [CONTAINER]


To see the output added in real-time, use `-f`

.. code-block:: bash

   $ docker logs -f [CONTAINER]


Journald logging driver
~~~~~~~~~~~~~~~~~~~~~~~

The journald logging driver sends container logs to the systemd journal. Log entries can be retrieved
using the journalctl command, through use of the journal API, or using the docker logs command.

Configure the default logging driver by passing the --log-driver option to the Docker daemon:

.. code-block:: bash

    $ dockerd --log-driver=journald

or edit the `/etc/systemd/system/docker.service.d/override.conf` like this:

.. code-block:: bash

   [Service]
   ExecStart=
   ExecStart=/usr/bin/dockerd -H fd:// -s overlay2 --log-driver=journald



To configure the logging driver for a specific container, use the `--log-driver` flag on the docker run command.

.. code-block:: bash

   $ docker run --log-driver=journald ...
   $ sudo journalctl -u docker CONTAINER_NAME=container_name


Inspecting processes inside a container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see processes running inside the container:

.. code-block:: bash

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

.. code-block:: bash

    $ docker run --restart=always ...

    
It will try to restart the container no matter what exit code is returned. Alternatively, we can
specify a value of `on-failure` which restarts the container if it exits with a non-zero exit code:

.. code-block:: bash

    $ docker run --restart=on-failure:5 ...


It will restart a maximum of 5 times if a non-zero exit code is received.


Docker images
-------------

Docker images are made as a series of read-only layers. When a container starts, Docker takes the
read-only image and adds a read-write layer on top. If the running container modifies an existing file,
the file is copied out of the underlying read-only layer and into the top-most read-write layer where the
changes are applied. The version in the read-write layer hides the underlying file, but does not destroy it.
It still exists in the underlying layer. When a Docker container is deleted, relaunching the image will start
a fresh container without any of the changes made in the previously running container. Those changes are lost. 
Docker calls this combination of read-only layers with a read-write layer on top a Union File System.

Taken from `here <http://container-solutions.com/understanding-volumes-docker/>`_


Images live inside repositories, and repositories live on registries. The default registry is the public registry
managed by Docker, Inc., Docker Hub.

Each repository can contain multiple images (e.g., the ubuntu repository contains
images for Ubuntu 12.04, 12.10, 13.04, 13.10, 14.04, 16.04)

Pulling images
~~~~~~~~~~~~~~

`docker pull` command pulls down the image from the ubuntu repository to the local host

.. code-block:: bash

    $ docker pull ubuntu:16.04
    $ docker pull ubuntu:latest


Listing images
~~~~~~~~~~~~~~

List images available in the Docker host:

.. code-block:: bash

    $ docker images
    $ docker image ls


Searching for images
~~~~~~~~~~~~~~~~~~~~
To search all of the publicly available images on Docker Hub, run:

.. code-block:: bash

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


Dockerfile Languague
~~~~~~~~~~~~~~~~~~~~

- FROM: specifies the base image
- RUN: By default, it executes a command inside a shell using the command wrapper `/bin/sh -c`
- EXPOSE: tells Docker that the application in this container will use this specific port on the container.

(I need to add more info here)


Volumes
-------

Volumes are directories or files that are outside of the default Union File System and
exist as normal directories and files on the host filesystem.

Creating volumes
~~~~~~~~~~~~~~~~

**Creating a volume at the run time with `-v` flag:**

.. code-block::

    $ docker run -it --name CONTAINER_NAME -h CONTAINER_HOSTNAME -v /data ubuntu:latest /bin/bash
    root@CONTAINER_HOSTNAME:/# ls /data
    root@CONTAINER_HOSTNAME:/#

It will creates a docker volume and a `/data` directory inside the container and this directory will live
outside the Union File System and directly accessible on the host. Any files that the image held inside the
`/data`  directory will be copied into the volume.

The same effect can be achieved using the VOLUME statement in a Dockerfile:

.. code-block::

   FROM ubuntu:latest
   VOLUME /data


We can know where the volume is on the host by using the `docker inspect` command on the host

.. code-block:: bash

    $ docker inspect -f "{{json .Mounts}}" CONTAINER_NAME


**Creating a volume using the `docker volume create` command:**

.. code-block:: bash

   $ docker volume create --name vol-test
   $ docker volume ls
   $ docker run -it --name CONTAINER_NAME -h CONTAINER_HOSTNAME -v VOL_NAME:/data ubuntu:latest /bin/bash


**Mounting a specific directory from the host using the `-v` flag:**

.. code-block:: bash

   $ docker run -v /home/user/data:/data -it -h test-container ubuntu:latest /bin/bash


It will mount the `/home/user/data` host directory into the container `/data` directory. It could be useful to share
files between the container and the host

In order to preserve portability, the host directory for a volume cannot be specified in a Dockerfile because
the host directory may not be available on all systems.


Listing volumes in the host
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   $ docker volume ls


Sharing data between containers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The argument `--volumes-from` in the docker run command, is used to give volume access to another container

.. code-block:: bash

    $ docker run -it -h NEWCONTAINER --volumes-from CONTAINER_NAME IMAGE PROC
    $ docker run -it -h test-container2 --volumes-from test-container1 ubuntu /bin/bash


If you want to mount the volume in a different directory inside the container, you should specify with `-v` flag
the volume_name and the mount point into the container.

.. code-block:: bash

    $ docker run -it -h NEWCONTAINER -v VOL_ID:/data2 ubuntu /bin/bash
    
 
User-defined networks
---------------------

It is recommended to use user-defined bridge networks to control which containers can communicate with each other, and also to enable automatic DNS resolution of container names to IP addresses (in favor of the deprecated option ``--link``)

The easiest user-defined network to create is a bridge network. This network is similar to the historical,
default `docker0` network.
 
.. code-block:: bash
 
    $ docker network create --subnet=172.18.0.0/24 --gateway=172.18.0.1 --driver=bridge my_network
    $ docker network inspect my_network
    
Then you can launch a container in this network, with a fixed-ip using:

.. code-block:: bash

    $ docker run --network my_network --ip 172.18.0.2 ...
