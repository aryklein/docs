Kubernetes cheet sheet
======================

Getting started with Google Cloud
---------------------------------

1) Download the the SDK app: ``google-cloud-sdk``

2) Initialize or reinitialize gcloud

::

    $ gcloud init

3) Configure the gcloud::

    $ # Set a default project
    $ gcloud config set project [PROJECT_ID]

    $ # gcloud config set compute/zone NAME
    $ gcloud config set compute/zone us-east1-b

    $ # gcloud config set compute/region NAME
    $ gcloud config set compute/region us-east1


Run ``gcloud help config`` to learn how to change individual settings.

This gcloud configuration is called [default]. You can create additional configurations if you work with multiple
accounts and/or projects.

Run ``gcloud topic configurations`` to learn more.

4) Create the Kubernetes cluster using Dashboard or gcloud

::

    $ gcloud container clusters create cluster-1 --zone us-east1-b --machine-type f1-micro --num-nodes 3 --enable-autoupgrade
    $ gcloud container clusters list

5) Get credentials for ``kubectl``:

``gcloud container clusters get-credentials`` updates a kubeconfig file with appropriate credentials and endpoint
information to point kubectl at a specific cluster in Google Kubernetes Engine. It takes a project and a zone as
parameters, passed through by set defaults or flags. By default, credentials are written to ``HOME/.kube/config``.
You can provide an alternate path by setting the KUBECONFIG environment variable. *This command enables switching to a
specific cluster, when working with multiple clusters. It can also be used to access a previously created cluster
from a new workstation.*

::

    $ gcloud container clusters get-credentials CLUSTER-NAME

6) Install kubectl binary on your system using gcloud

::

    $ gcloud components install kubectl


Working with Kubernetes
-----------------------

A list of useful commands

Checking Cluster Status
+++++++++++++++++++++++

Get a simple diagnostic for the cluster. This is a good way to verify that your cluster is generally healthy

::

    $ kubectl get componentstatuses

Listing Kubernetes Nodes
++++++++++++++++++++++++

Get a list of nodes

::
  
    $ kubectl get nodes

Get more information about a specific node

::
  
    $ kubectl describe node NODE-NAME

Namespaces
++++++++++

Kubernetes uses namespaces to organize objects in the cluster. You can think of each namespace as a folder
that holds a set of objects. By default, the ``kubectl command-line`` tool interacts with the default namespace.
If you want to use a different namespace, you can pass kubectl the ``--namespace`` flag.

Pod
+++

A Pod is a collection of containers and volumes running in the same execution environment. All containers in a Pod always run on the same machine.

Logs
++++

Getting a Pod logs:

::

    $ kubectl logs POD-NAME

If there are multiple containers in a pod, you can choose the container to view using the -c flag.

Execute a command in a container
++++++++++++++++++++++++++++++++

You can also use the exec command to execute a command in a running container

::

    $ kubectl exec -it POD-NAME -- sh

Creating a new Pod
++++++++++++++++++

The simplest way to create a Pod is via the imperative ``kubectl run`` command.

::

    $ kubectl run webserver --image=nginx

This manner of creating a Pod actually creates it via Deployment and ReplicaSet objects. The other way is using
a pod manifest

Create a Pod manifest using YAML or JSON, but YAML is generally preferred because it is slightly more human-editable
and has the ability to add comments.

Apply the manifest:

::

    $ kubectl apply -f pod-manifest.yaml

Listing and describing Pods
+++++++++++++++++++++++++++

::

    $ kubectl get pods
    $ kubectl describe pods POD-NAME

Deleting a Pod
++++++++++++++

::

    $ kubectl delete pods/kuard
    $ # OR
    $ kubectl delete -f pod-manifest.yaml
    
Access into a Pod
+++++++++++++++++

Without exposing the service to the world, you can reach the Pod using port-forward option

::

    $ kubectl port-forward POD-NAME 8080:8080

Using Volumes with Pods
+++++++++++++++++++++++

To understand volumes, please refer to the following link:

https://kubernetes.io/docs/concepts/storage/volumes/

Service Discovery
+++++++++++++++++

Use ``kubectl expose`` to create a service

::

    $ kubectl run webserver --image=nginx --replicas=3 --port=80 --labels="ver=1,app=webserver,env=prod"
    $ kubectl expose deployment webserver
    $ kubectl get service

This service is assigned a new type of virtual IP called a **cluster IP**. This is a special IP address the
system will load-balance across all of the pods that are identified by the selector.

Internal DNS
++++++++++++

When you spin up a pod, you Kubernetes will create a private DNS address that resolves with the cluster IP.
In this example it is: ``webserver.default.svc.cluster.local``

``webserver``: the name of the service.

``default``: the name of the namespace where the service is running.

``svc``: this is because it's a service.

``cluster.local``: the base domain name for the cluster.

NodePort
++++++++

The IPs for pods and the cluster IP are only reachable from within the cluster.
If you need to reach the Pod from outside, you can use the ``NodePort`` option. With this feature, if you can
reach any node in the cluster you can contact a service.

::

    $ kubectl expose deployment webserver --type=NodePort
    $ kubectl describe service webserver

Kubernetes will assign a random port to all nodes where the service is running

Load Balancer
+++++++++++++

If there is support from the cloud that you are running on, you can use the LoadBalancer type. This builds on
``NodePort`` by additionally configuring the cloud to create a new load balancer and direct it at nodes
in your cluster.

::

    $ kubectl expose deployment webserver --type=LoadBalancer
    $ # Or you can use 'edit' to change the type
    $ kubectl edit webserver

Endpoints
+++++++++

To get the IPs of the Pods you can use

::

    $ kubectl get endpoints
    $ kubectl get endpoints webserver

ReplicaSet
++++++++++

A ReplicaSet acts as a cluster-wide Pod manager, ensuring that the right types and number of Pods are running
at all times. 

ReplicaSets create and manage Pods but they do not own the Pods they create.

The ReplicaSet controller will create new Pods. The Pods are created using a Pod template that is contained in
the ReplicaSet specification. The Pods are created in exactly the same manner as when you created a Pod from a
YAML file. But instead of using a file, the Kubernetes ReplicaSet controller creates and submits a Pod manifest
based on the Pod template directly to the API server.

*Creating a ReplicaSet*:

.. code-block:: yaml

    apiVersion: extensions/v1beta1
    kind: ReplicaSet
    metadata:
        name: webserver
    spec:
        replicas: 3
        template:
             metadata:
                 labels:
                     app: webserver
                     version: "2"
             spec:
                 containers:
                     - name: webserver
                       image: "nginx"

::

    $ kubectl apply -f rs-test.yaml
    $ kubectl describe rs rs-test

**Delete a ReplicaSet:**

By default, this will delete the Pods that are managed by the ReplicaSet:

::

    $ kubectl delete rs webserver

Horizontal pod autoscaling (HPA)
++++++++++++++++++++++++++++++++

The following command scale automatically based on the CPU usage:

::

    $ kubectl autoscale rs webserver --min=2 --max=5 --cpu-percent=80

This command creates an autoscaler that scales between 2 and 5 replicas with a CPU threshold of 80%.

::

    $ kubectl get hpa
