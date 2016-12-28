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

If you want to be able to run docker as a regular user, add yourself to the docker group:

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

    # docker info | head

To set your own choice of storage driver, create a Drop-in snippet and use -s option to dockerd:

::

   /etc/systemd/system/docker.service.d/override.conf

   [Service]
   ExecStart=
   ExecStart=/usr/bin/dockerd -H fd:// -s overlay2

Recall that ExecStart= line is needed to drop inherited ExecStart.

