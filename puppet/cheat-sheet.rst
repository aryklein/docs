Puppet cheat sheet
==================

.. contents::

This is not a HOWTO. It is only a cheat sheet to remember common procedures.
It only intends to be a personal help guide (for pesonal use). If you are going to
use it, please take in mind that I am not a Puppet expert. Each item of this cheat
sheet was tested on Ubuntu 16.04.

Working with certs
------------------

Listing certificates
````````````````````

On puppet master List certificate requests:

.. code-block:: bash

   # puppet cert list

List all signed certificates and unsigned certificate requests. Signed certificates
are also listed, prefixed by '+', and revoked or invalid certificates are prefixed by '-' 
(the verification outcome is printed in parenthesis). If '--human-readable' or '-H' is specified,
certificates are formatted in a way to improve human scan-ability. If '--machine-readable' or '-m'
s specified, output is formatted concisely for consumption by a script.

.. code-block:: bash

    # puppet cert list --all


Regenerating a Puppet agent certificate
```````````````````````````````````````

You may encounter a situation in which you need to regenerate a certificate for a Puppet agent node.
The following steps explain how to regenerate a certificate for a Puppet agent node using PE’s
built-in certificate authority (CA).

**Unless otherwise indicated, the following steps should be performed on your agent nodes**

1. **On the Puppet master**, clear the cert for the agent node. Run puppet cert clean <CERTNAME>.
2. Stop the Puppet agent, MCollective, and pxp-agent services

.. code-block:: bash

       # puppet resource service puppet ensure=stopped
       # puppet resource service mcollective ensure=stopped
       # puppet resource service pxp-agent ensure=stopped

3. Delete the agent's SSL directory. On \*nix nodes, run:

.. code-block:: bash

       # rm -rf /etc/puppetlabs/puppet/ssl
       # find /etc/puppetlabs/puppet/ssl -name <fqdn>.pem -delete

4. Remove the agent's cached catalog. On \*nix nodes,run:
   
.. code-block:: bash

       # rm -f /opt/puppetlabs/puppet/cache/client_data/catalog/<CERTNAME>.json.

5. Re-start the Puppet agent and MCollective services.
   
.. code-block:: bash

       # puppet resource service puppet ensure=running
       # puppet resource service mcollective ensure=running

After the Puppet agent starts, it will automatically generate keys and request
a new certificate from the CA Puppet master.

6. **On the Puppet master** sign each agent node’s certificate request.

.. code-block:: bash

       # puppet cert list
       # puppet cert sign <NAME>

7. Test the Puppet agent:

.. code-block:: bash

       # puppet agent --test


Remove certificate request on Puppet Master
```````````````````````````````````````````
.. code-block:: bash

      # puppet ca destroy <NAME>


Resource Types
--------------

Puppet code is composed primarily of resource declarations. A resource describes
something about the state of the system, such as a certain user or file should exist,
or a package should be installed.

Resource types are single units of configuration composed by:
- A type (package, service, file, user, mount, exec ...)
- A title (how is called and referred)
- Zero or more arguments

.. code-block:: ruby

    resource_type { 'title':
      attribute  => value,
      other_attribute => value,
    }


Example of a resource is:

.. code-block:: ruby

    file { 'motd':
      path    => '/etc/motd',
      content => 'Tomorrow is another day',
    }

    user { 'mitchell':
      ensure     => present,
      uid        => '1000',
      gid        => '1000',
      shell      => '/bin/bash',
      home       => '/home/mitchell'
    }

    
For the full list of available resource types try:

::

    # puppet resource --types
    # puppet describe --list
    # puppet describe file


**Example:** Installation of OpenSSH package

.. code-block:: ruby

   package { 'openssh':
     ensure => present,
   }

Creation of ``/etc/motd`` file:

.. code-block:: ruby

    file { 'motd':
      path => '/etc/motd',
    }

Start of *httpd* service:

.. code-block:: ruby

    service { 'httpd':
      ensure => running,
      enable => true,
    }


Resource Abstraction Layer
--------------------------
The RAL stands for the Resource Abstraction Layer, and it refers to the components of Puppet that
interact with the system. The RAL provides an abstract concept of something you can manage, and it
defines concrete ways of managing things. The Puppet RAL is what allows you to write a manifest that
works on several different platforms without having to remember if you should invoke ``apt-get install```
or ``yum install``.

Resources are abstracted from the underlying OS

Use ``puppet resource`` to interrogate the RAL:

.. code-block:: bash

    # puppet resource user
    # puppet resource user root
    # puppet resource service
    # puppet resource service ssh

Or to directly modify resources:

.. code-block:: bash

    # puppet resource service ssh ensure=running enable=true
    # systemctl is-enable ssh
    # puppet resource service ssh ensure=running enable=false
    # puppet resource service ssh
    # systemctl is-enable ssh



Manifests
---------

Puppet programs are called manifests. Manifests are composed of puppet code and their filenames
use the .pp extension. The default main manifest in Puppet installed via apt-get is
``/etc/puppetlabs/code/environments/production/manifests/site.pp``


Environments
------------
Environments are isolated groups of Puppet agent nodes. A Puppet master server can serve each environment
with completely different main manifests and modulepaths. This frees you to use different versions of the
same modules for different populations of nodes, which is useful for testing changes to your Puppet code 
before implementing them on production machines. (You could also do this by running a separate Puppet master
for testing, but using environments is often easier.)

Structure of an environment
```````````````````````````
An environment is just a directory (in Puppet master) that follows a few conventions:

- The directory name is the environment name.
- It must be located on the Puppet master server in one of the ``environmentpath`` directories, usually ``$codedir/environments``
- It should contain a ``modules`` directory. If present, it will become part of the environment’s default modulepath.
- It should contain a ``manifests`` directory, which will be the environment’s default main manifest.
- It may contain an ``environment.conf`` file, which can locally override several settings, including ``modulepath`` and ``manifest``.

An example for creating a ``testing`` enviroment is:

.. code-block:: bash

    # cp -r /etc/puppetlabs/code/environments/production /etc/puppetlabs/code/environments/testing


**Assigning environments via the agent's config file**:

In ``puppet.conf`` on each agent node, you can set the environment setting in either the agent or main config section.
When that node requests a catalog from the Puppet master, it will request that environment

::

    [main]
    certname = agent01.example.com
    server = puppet
    environment = testing
    runinterval = 1h

Node definition
---------------

A node definition or node statement is a block of Puppet code that will only be included in matching nodes’ catalogs.
This feature allows you to assign specific configurations to specific nodes.

Node definitions should go in the main manifest. The main manifest can be a single file, or a directory containing
many files.

.. code-block:: ruby

    # <ENVIRONMENTS DIRECTORY>/<ENVIRONMENT>/manifests/site.pp
    node 'www1.example.com' {
      include common
      include apache
      include squid
    }
    node 'db1.example.com' {
      include common
      include mysql
    }


In the example above, only ``www1.example.com`` would receive the apache and squid classes, and only ``db1.example.com``
would receive the mysql class.

Node definitions look like class definitions. The general form of a node definition is:

- The node keyword
- The name(s) of the node(s), separated by commas (with an optional final trailing comma)
- An opening curly brace
- Any mixture of class declarations, variables, resource declarations, collectors, conditional statements,
  chaining relationships, and functions
- A closing curly brace

The name **default** (without quotes) is a special value for node names. If no node statement matching a given node can be found, the default node will be used.


Classes - Definition
--------------------

Classes are containers of different resources. They are code blocks that can
be called in a code elsewhere.

This is a class declaration:

.. code-block:: ruby

    class example_class {
        ...
        code
        ...
    }


Modules Structure
-----------------

This is an example of a Puppet module directory structure:

- *files*
- *manifests*: it must exists. It is the place for Puppet module code
- *templates*
- *tests*: used for testing in the local machine before appling in puppet agent nodes


**Example of a Puppet module**:

First create the module structure directory:

::

    # cd modules
    # mkdir localusers
    # cd localusers
    # mkdir {files,manifests,templates,tests}

The **manifests** directory must have a **init.pp** file (called high level class)

So create a ``manifests/init.pp`` file with the following content:

.. code-block:: ruby

    class localusers {
        user { 'admin':
                ensure          => present,
                shell           => '/bin/bash',
                home            => '/home/admin',
                gid             => 'wheel',
                managehome      => true,
                password        => '$6$wBjx0qjf$vfTbljHXtEci ... T0uwPwXI.'
        }

        user { 'jdoe':
                ensure          => present,
                shell           => '/bin/bash',
                home            => '/home/jdoe',
                groups          => ['wheel','finance'],
                managehome      => true,
                password        => '$6$wBjx0qjf$vfTbljHXtEci ... T0uwPwXI.'
        }

    }

Create a new directory: ``manifests/localusers/groups``. This directorory is going to have
all necesary groups. So create a file ``wheel.pp:`` with the following content:

.. code-block:: ruby

   class localusers::groups::wheel {
       group { 'wheel':
                ensure => present,
       }
   }


and another file ``finance.pp`` with a group named *finance*:

.. code-block:: ruby

   class localusers::groups::finance {
          group { 'finance':
                   ensure => present,
          }
   }


It is recommended after editing a ``pp`` file, check the syntax with ``puppet parser validate xxx.pp``

For example:

::

    # puppet parser validate init.pp
    # puppet parser validate groups/wheel.pp
    # puppet parser validate groups/finance.pp


Now it's time to test the module in the local machine, before applying it on Puppet nodes.
Here is where the **tests** directory is used.

Inside ``localusers/tests`` directory, create a ``init.pp`` file:

.. code-block:: ruby

    include localusers
    include localusers::group::wheel
    include localusers::group::finance

Check the syntax and test it:

::

    # puppet validate localusers/tests/init.pp
    # puppet apply --noop localusers/tests/init.pp
    # puppet apply localusers/tests/init.pp

As you can see, Puppet is smart to know that it has to create the **finance** group before
creating the user **jdoe**, since this user is going to neeed the **finance** group. So
it is not necesarry to take care about order. Puppet will decide the right order.


Relationships and ordering
--------------------------

By default, Puppet applies resources in the order they’re declared in their manifest.
However, if a group of resources need be managed in a specific order, you should explicitly
declare such relationships with relationship metaparameters, chaining **arrows**, and the
**require** function.

*Note:*

Metaparameters: some attributes in Puppet can be used with every resource type. These are called
**metaparameters**. They don't map directly to system state; instead, they specify how Puppet
should act toward the resource.

Relationship metaparameters
```````````````````````````

Puppet uses four metaparameters to establish relationships, and you can set each of them as an attribute
in any resource. The value of any relationship metaparameter should be a resource reference
(or array of references) pointing to one or more target resources.

- ``before``: Applies a resource before the target resource.
- ``require``:  Applies a resource after the target resource.
- ``notify``: Applies a resource before the target resource. The target resource refreshes if the notifying resource changes.
- ``subscribe``: Applies a resource after the target resource. The subscribing resource refreshes if the target resource changes.

If two resources need to happen in order, you can either put a ``before`` attribute in the prior one or
a ``require`` attribute in the subsequent one; either approach creates the same relationship. 
The same is true of ``notify`` and ``subscribe``.

Example:

.. code-block:: ruby

    package { 'openssh-server':
        ensure => present,
        before => File['/etc/ssh/sshd_config'],
    }

    file { '/etc/ssh/sshd_config':
        ensure  => file,
        mode    => '0600',
        source  => 'puppet:///modules/sshd/sshd_config',
        require => Package['openssh-server'],
    }


.. code-block:: ruby

    service { 'sshd':
        ensure  => running,
        require => [
            Package['openssh-server'],
            File['/etc/ssh/sshd_config'],
        ],
    }

    package { 'openssh-server':
        ensure => present,
        before => Service['sshd'],
    }

    file { '/etc/ssh/sshd_config':
        ensure => file,
        mode   => '0600',
        source => 'puppet:///modules/sshd/sshd_config',
        before => Service['sshd'],
    }


Chaining arrows
```````````````

You can create relationships between two resources or groups of resources using the ``->`` and ``~>`` operators

- ``->``: Applies the resource on the left before the resource on the right (ordering)

- ``~>``: Applies the resource on the left first. If the left-hand resource changes, the right-hand resource will
  refresh. (notifying)


.. code-block:: ruby

    # ntp.conf is applied first, and notifies the ntpd service if it changes:
    File['/etc/ntp.conf'] ~> Service['ntpd']



Case Statements
---------------

.. code-block:: ruby

    case $osfamily {
        'RedHat': {
                $ssh_name = 'sshd'
         }

         'Debian': {
                $ssh_name = 'ssh'
         }

         'default': {
                Warning('OS family does not match')
         }

    }


    service {'resource-name':
        name => $ssh_name
        ensure => running,
        enable => true,
    }

