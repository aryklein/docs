Personal Docker Swarm notes
===========================

Docker Swarm provides native clustering functionality for Docker containers, which turns a group of Docker
engines into a single, virtual Docker engine.

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
