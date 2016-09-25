Puppet cheat sheet
==================

This is not a HOWTO. It is only a cheat sheet to remember common procedures.
It only intends to be a personal help guide (for pesonal use). If you are going to
use it, please take in mind that I am not a Puppet expert. Each item of this cheat
sheet was tested on Ubuntu 16.04.

Working with certs
------------------

Listing certificates
--------------------

On puppet master List certificate requests:

.. code-block:: bash

   $ sudo puppet cert list

List all signed certificates and unsigned certificate requests. Signed certificates
are also listed, prefixed by '+', and revoked or invalid certificates are prefixed by '-' 
(the verification outcome is printed in parenthesis). If '--human-readable' or '-H' is specified,
certificates are formatted in a way to improve human scan-ability. If '--machine-readable' or '-m'
s specified, output is formatted concisely for consumption by a script.

.. code-block:: bash

    $ sudo puppet cert list --all


Regenerating a Puppet agent certificate
---------------------------------------

You may encounter a situation in which you need to regenerate a certificate for a Puppet agent node.
The following steps explain how to regenerate a certificate for a Puppet agent node using PE’s
built-in certificate authority (CA).

**Unless otherwise indicated, the following steps should be performed on your agent nodes**

1. **On the Puppet master**, clear the cert for the agent node. Run puppet cert clean <CERTNAME>.
2. Stop the Puppet agent, MCollective, and pxp-agent services

   ::

       # puppet resource service puppet ensure=stopped
       # puppet resource service mcollective ensure=stopped
       # puppet resource service pxp-agent ensure=stopped

3. Delete the agent’s SSL directory. On *nix nodes, run:

   :: 

       # rm -rf /etc/puppetlabs/puppet/ssl
       # find /etc/puppetlabs/puppet/ssl -name <fqdn>.pem -delete

4. Remove the agent’s cached catalog. On *nix nodes,run:
   
   :: 

       # rm -f /opt/puppetlabs/puppet/cache/client_data/catalog/<CERTNAME>.json.

5. Re-start the Puppet agent and MCollective services.
   
   ::

       # puppet resource service puppet ensure=running
       # puppet resource service mcollective ensure=running

After the Puppet agent starts, it will automatically generate keys and request
a new certificate from the CA Puppet master.

6. **On the Puppet master** sign each agent node’s certificate request.

   ::

       # puppet cert list
       # puppet cert sign <NAME>

7. Test the Puppet agent:

   ::

       # puppet agent --test


Resource Types
--------------

Puppet code is composed primarily of resource declarations. A resource describes
something about the state of the system, such as a certain user or file should exist,
or a package should be installed.

Resource types are single units of configuration composed by:
- A type (package, service, file, user, mount, exec ...)
- A title (how is called and referred)
- Zero or more arguments

::

    resource_type { 'title':
      attribute  => value,
      other_attribute => value,
    }


Example of a resource is:

::

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


**Examples:**

Installation of OpenSSH package

::

   package { 'openssh':
     ensure => present,
   }

Creation of ``/etc/motd`` file:

::

    file { 'motd':
      path => '/etc/motd',
    }

Start of *httpd* service:

::

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

::

    puppet resource user
    puppet resource user root
    puppet resource service
    puppet resource service ssh

Or to directly modify resources:

::

    # puppet resource service ssh ensure=running enable=true
    # systemctl is-enable ssh
    # puppet resource service ssh ensure=running enable=false
    # puppet resource service ssh
    # systemctl is-enable ssh



Manifests
---------

Puppet programs are called manifests. Manifests are composed of puppet code and their filenames
use the .pp extension. The default main manifest in Puppet installed via apt-get is
``/etc/puppet/manifests/site.pp`` or ``/etc/puppetlabs/code/environments/production/manifests/site.pp``


Classes - Definition
--------------------

Classes are containers of different resources. They are code blocks that can
be called in a code elsewhere.

This is a class declaration:

::

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

::

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

::

   class localusers::groups::wheel {
       group { 'wheel':
                ensure => present,
       }
   }


and another file ``finance.pp`` with a group named *finance*:

::

   class localusers::groups::finance {
          group { 'finance':
                   ensure => present,
          }
   }


It is recommended after editing a ``pp`` file, check the syntax with ``puppet validate xxx.pp``

For example:

::

    # puppet parse validate init.pp
    # puppet parse validate groups/wheel.pp
    # puppet parse validate groups/finance.pp


Now it's time to test the module in the local machine, before applying it on Puppet nodes.
Here is where the **tests** directory is used.

Inside ``localusers/tests`` directory, create a ``init.pp`` file:

::

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
