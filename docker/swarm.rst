Personal Docker Swarm notes
===========================

These notes were taken from the official Docker site. It's almost a copy-paste of the most important commands.
If you look for a better reference, please visit the `Docker site <https://docs.docker.com/engine/swarm/>`_.

Docker Swarm provides native clustering functionality for Docker containers, which turns a group of Docker
engines into a single, virtual Docker engine.

.. contents::

Concepts
--------

A *node* is a Docker engine participating in the Swarm cluster. A *manager node* is a node that dispatches
units of work called *tasks* to *worker nodes*. Worker nodes receive and execute tasks dispatched from
manager nodes. By default manager nodes also run services as worker nodes.

A service is the definition of the tasks to execute on the Docker nodes. When you create a service, you
specify which container image to use and which commands to execute inside running containers.

In the replicated services model, the swarm manager distributes a specific number of replica
tasks among the nodes based upon the scale you set in the desired state.

Create a swarm
--------------

I will use 3 Docker engines: ``manager1`` as a manager node, ``Worker1`` and ``Worker2`` as a workers nodes.

Run the following command in ``manager1`` to create a new Swarm:

.. code-block:: bash

    $ docker swarm init --advertise-addr <MANAGER-IP>

This command will output a token. Then to add a *worker node* to this swarm, run the following command
on all workers nodes (in this case ``Worker1`` and ``Worker2``):

.. code-block:: bash

    $ docker swarm join --token <MANAGER-TOKEN> <MANAGER-IP>:2377
    
 If you don’t have the token, you can run the following command on a manager node to retrieve the
 join command for a worker:

.. code-block:: bash

    $ docker swarm join-token worker

You can run ``docker node ls`` command in a manager node to view information about all nodes:

.. code-block:: bash

    ary@manager1:~$ docker node ls
    ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS
    xvlcp35ga9xq9rxage1c0727i *   manager1            Ready               Active              Leader
    htu6nmeeni94ixpxjr6mxmev2     worker1             Ready               Active
    k4rstpdvkeukqzy4svywkvxgj     worker2             Ready               Active


The ``*`` next to the node ID indicates that you’re currently connected on this node.
Docker Engine swarm mode automatically names the node for the machine host name.

Deploy a service
----------------

Run the following command on a manager node:

.. code-block:: bash

     $ docker service create --replicas 2 --name helloworld alpine ping docker.com
     
- The ``docker service create`` command creates a new service.
- The ``--name`` flag names the service ``helloworld``.
- The ``--replicas`` flag specifies the desired state of 2 running instance.
- The arguments ``alpine ping docker.com`` define the service as an Alpine Linux container
that executes the command ping docker.com.

You can run ``docker service ls`` to see the list of running services:

.. code-block:: bash

    ary@manager1:~$ docker service ls
    ID                  NAME                MODE                REPLICAS            IMAGE               PORTS
    7qki5ynei1tc        helloworld          replicated          2/2                 alpine:latest       

You can run ``docker service ps <SERVICE-ID>`` to see which nodes are running the service:

.. code-block:: bash

    ary@manager1:~$ docker service ps helloworld 
    ID                  NAME                IMAGE               NODE                DESIRED STATE       CURRENT STATE                ERROR               PORTS
    rmmzwx8e9gxk        helloworld.1        alpine:latest       worker1             Running             Running about a minute ago                       
    wxu7a15pl912        helloworld.2        alpine:latest       worker2             Running             Running about a minute ago


Also, you can run ``docker ps`` on the node where the task is running to see details about the container
for the task.

Scale a running service
-----------------------

In a manager node run the following command to change the desired state of the service running in the swarm:

``$ docker service scale <SERVICE-ID>=<NUMBER-OF-TASKS>``

.. code-block:: bash

    ary@manager1:~$ docker service ps helloworld
    ID                  NAME                IMAGE               NODE                DESIRED STATE       CURRENT STATE            ERROR               PORTS
    rmmzwx8e9gxk        helloworld.1        alpine:latest       worker1             Running             Running 11 minutes ago                       
    wxu7a15pl912        helloworld.2        alpine:latest       worker2             Running             Running 11 minutes ago                       
    
    ary@manager1:~$ docker service scale helloworld=5
    helloworld scaled to 5
    
    ary@manager1:~$ docker service ps helloworld
    ID                  NAME                IMAGE               NODE                DESIRED STATE       CURRENT STATE            ERROR               PORTS
    rmmzwx8e9gxk        helloworld.1        alpine:latest       worker1             Running             Running 11 minutes ago                       
    wxu7a15pl912        helloworld.2        alpine:latest       worker2             Running             Running 11 minutes ago                       
    76fz3aa57yzj        helloworld.3        alpine:latest       manager1            Running             Running 3 seconds ago                        
    stixo2wmxxws        helloworld.4        alpine:latest       manager1            Running             Running 3 seconds ago                        
    wfzjzx1vthud        helloworld.5        alpine:latest       worker2             Running             Running 3 seconds ago 


Delete the service running on the swarm
---------------------------------------

.. code-block:: bash

    $ docker service rm <SERVICE-ID>

Even though the service no longer exists, the task containers take a few seconds to clean up.
You can use docker ps on the nodes to verify when the tasks have been removed.


Publish ports
-------------

When you create a swarm service, you can publish that service's ports to hosts outside the swarm in two ways:

1) You can rely on the routing mesh. When you publish a service port, the swarm makes the service accessible at
the target port on every node, regardless of whether there is a task for the service running on that node or
not. This is less complex and is the right choice for many types of services.

2) You can publish a service task's port directly on the swarm node where that service is running.
This feature is available in Docker 1.13 and higher. This bypasses the routing mesh and provides the maximum
flexibility, including the ability for you to develop your own routing framework. However, you are responsible
for keeping track of where each task is running and routing requests to the tasks, and load-balancing across
the nodes.

1- Publish a service port using the routing mesh
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To publish a service’s ports externally to the swarm, use the ``--publish <PUBLISHED-PORT>:<SERVICE-PORT>`` flag.
The swarm makes the service accessible at the published port on every swarm node.

.. code-block:: bash

    $ docker service create --name my_web --replicas 3 --publish published=8080,target=80 nginx

Three tasks will run on up to three nodes. You don’t need to know which nodes are running the tasks; connecting
to port 8080 on any of the 10 nodes will connect you to one of the three nginx tasks

2- Publish a service port directly on the swarm node
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To publish a service's port directly on the node where it is running, use the ``mode=host`` option to the
``--publish`` flag.

.. code-block:: bash

    $ docker service create --mode global --publish mode=host,target=80,published=8080 --name=nginx nginx:latest

In addition, if you use ``mode=host`` and you do not use the ``--mode=global`` flag on docker service create,
it will be difficult to know which nodes are running the service in order to route work to them.


Connect the service to an overlay network
-----------------------------------------

You can use overlay networks to connect one or more services within the swarm.
First, create overlay network on a manager node using the ``docker network create`` command with
the ``--driver overlay`` flag.

.. code-block:: bash

    $ docker network create --driver overlay my-network

After you create an overlay network in swarm mode, all manager nodes have access to the network.
You can create a new service and pass the ``--network flag`` to attach the service to the overlay network:

.. code-block:: bash

    $ docker service create --replicas 3 --network my-network --name my-web nginx

The swarm extends ``my-network`` to each node running the service.
You can also connect an existing service to an overlay network using the ``--network-add`` flag.

.. code-block:: bash

    $ docker service update --network-add my-network my-web
    
To disconnect a running service from a network, use the --network-rm flag.

.. code-block:: bash

    $ docker service update --network-rm my-network my-web
 

Replicated or Global Services
-----------------------------

Swarm mode has two types of services: **replicated** and **global**. For **replicated** services,
you specify the number of replica tasks for the swarm manager to schedule onto available nodes.
For **global** services, the scheduler places *one task* on each available node that meets the
service’s placement constraints and resource requirements.

You control the type of service using the ``--mode`` flag. If you don’t specify a mode, the service
defaults to replicated. For **replicated** services, you specify the number of replica tasks you want
to start using the ``--replicas`` flag. For example, to start a replicated nginx service with 3 replica tasks:

.. code-block:: bash

    $ docker service create --name my_web --replicas 3 nginx

To start a global service on each available node, pass ``--mode global`` to ``docker service create``.
Every time a new node becomes available, the scheduler places a task for the global service on the new node.
For example to start a service that runs alpine on every node in the swarm:

.. code-block:: bash

    $ docker service create --name myservice --mode global alpine sh
