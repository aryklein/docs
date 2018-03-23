Kubernetes cheet sheet
======================

Getting started with Google Cloud
---------------------------------

1) Download the the SDK app: ``google-cloud-sdk``

2) Initialize or reinitialize gcloud::

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

4) Create the Kubernetes cluster using Dashboard or gcloud::

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

6) Install kubectl binary on your system using gcloud::

    $ gcloud components install kubectl

Working with Kubernetes (kubectl command)
-----------------------------------------

A list of useful commands

Checking Cluster Status
+++++++++++++++++++++++

Get a simple diagnostic for the cluster. This is a good way to verify that your cluster is generally healthy::

    $ kubectl get componentstatuses

Listing Kubernetes Worker nodes
+++++++++++++++++++++++++++++++

::
  
    $ kubectl get nodes
