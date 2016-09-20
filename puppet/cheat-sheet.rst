*****************
Puppet cheat sheet
*****************

This is not a HOWTO. It is only a cheat sheet to remember common procedures.
It only intends to be a personal help guide (for pesonal use). If you are going to
use it, please take in mind that I am not a Puppet expert. Each item of this cheat
sheet was tested on Ubuntu 16.04.

Working with certs
##################

Listing certificates
********************

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
***************************************
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

