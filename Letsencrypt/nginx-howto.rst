Letsencrypt SSL/TLS Certificate for Nginx using Docker
======================================================

Let's Encrypt is a certificate authority that provides X.509 certificates for Transport Layer Security (TLS) encryption at
no charge. The certificate is valid for 90 days and then it needs to be renewed every 3 months.

This guide will use **Certbot** to fetch and deploys SSL/TLS certificates for your webserver from Let's Encrypt.
Certbot will also work with any other CAs that support the ACME protocol.

If you want to know how it works, please read this article: https://letsencrypt.org/how-it-works

Certbot performs an ACME challenge request to validate that you are in control of your domain. If the challenge request is 
successful, the Certbot agent will install a new SSL/TLS certificate on your server.
To achieve this ACME challenge request, the Certbot agent request to Let's Encrypt a token and then it puts the token at an
endpoint in your domain:

::

    http://example.org/.well-known/acme-challenge/{token}


If the token placed in this endpoint by the Certbot agent matches the token that was sent in the previews step, Let's Encrypt
will know that you are in control of your domain.

To make all this process works, you will needed a running web server. For this guide we are going to use Nginx running in a 
Docker container.
