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
