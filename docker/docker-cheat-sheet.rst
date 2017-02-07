Docker cheat sheet
==================

This is not a HOWTO. It is only a cheat sheet to remind common procedures.
It only intends to be a personal help guide (for pesonal use). If you are going to
use it, please bear in mind, that I am not a Docker expert :)


Instalation
-----------

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


Configuration
-------------

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


Running a container
-------------------

`docker run` command will create a new container. 

::

    $ docker run [OPTIONS] IMAGE [COMMAND] [ARG...]


So for example:

::

    $ docker run -i -t ubuntu /bin/bash


**-i**: flag keeps STDIN open from the container, even if we're not attached to it.
This persistent standard input is one half of what we need for an interactive shell. 

**-t**: flag is the other half and tells Docker to assign a pseudo-tty to the container
we're about to create.

**ubuntu**: is the *image* to use to create a container. The ubuntu image is a stock image,
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
-------------------------

List running containers

::

    $ docker ps

Show all containers, both stopped and running:

::

   $ docker ps -a


Container naming
----------------

Docker will automatically generate a name at random for each container we create.
If we want to specify a particular container name in place of the automatically generated name,
we can do so using the `--name` flag:

::

    $ docker run --name foo_bar_container -i -t ubuntu /bin/bash


