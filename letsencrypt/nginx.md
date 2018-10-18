# Letsencrypt SSL/TLS Certificate for Nginx using Docker

Let's Encrypt is a certificate authority that provides X.509 certificates for Transport Layer Security (TLS) encryption at
no charge. The certificate is valid for 3 months and then it needs to be renewed.

Certbot is an ACME client written in Python that is used to fetch SSL/TLS certificates from Let's Encrypt. This guide uses
Cerbot. For more information: https://certbot.eff.org/about/

Basically Certbot performs an ACME challenge request to validate that you have control of your domain. If the challenge
request is successful, the Certbot agent will fetch a new SSL/TLS certificate. To achieve this ACME challenge request, the
Certbot agent requests to Let's Encrypt a token and then it places the token file at an endpoint in your domain.

For example:

```
http://example.org/.well-known/acme-challenge/{token file}
```

Let's Encrypt must be able to connect to http://example.org/.well-known/acme-challenge/ and retrieve the token file. If the
token placed a the endpoint by Certbot matches, Let's Encrypt will know that you are in control of your domain.

If you want to know better how it works, please read this article: https://letsencrypt.org/how-it-works

To make all this process works, it is needed a running web server. This guide uses Nginx running in a Docker container.


## Get the ball rolling

We are going to work with host volume. A host volume lives on the Docker host's filesystem and can be accessed from within
the container. So let's start creating the volumen in the host filesystem:

```bash
$ sudo mkdir /volumes
```

This is just an example to make the guide simplier, but this is not a good path. You should choose a better location in your
host's filesystem.

Then, we are going to create a simple website and place it inside the host volume.


```
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>Let's Encrypt Hello World</title>
</head>
<body>
    <h1>Hello Let's Encrypt!</h1>
    <p>
        This is an example site to test the certificate issued by Let's Encrypt.
    </p>
</body>
</html>
```

We can save it under ``/volumes/usr/share/nginx/html/index.html``. I like to keep in the volume the same path as the
container filesystem, so it is esier to understand but you can use other path.

Now, we are going to create the Nginx server block configuration for this site in the volume
`/volumes/etc/nginx/conf.d/example.conf`:


```
server {
    listen 80;
    listen [::]:80;
    server_name www.example.org example.org;

    root /usr/share/nginx/html;
    index index.html;
}
```

The idea is to spin up a Nginx container to ensure that the site will run. In general I prefer to use the Alpine
version. There is a good video that explains good reasons: https://www.youtube.com/watch?v=wGz_cbtCiEA

Two host volumes will be mounted: the Nginx configuration and the website.

```
$ docker run -it --name nginx-test -v /volumes/etc/nginx/conf.d:/etc/nginx/conf.d \
-v /volumes/usr/share/nginx/html:/usr/share/nginx/html -p 80:80 nginx:alpine
```

If you go to http://www.example.org, you should get the page without certificate (HTTP). If it works, you can stop and remove
this container and change the Nginx server block configuration to run Certbot. Now the file
`/volume/etc/nginx/conf.d/example.conf` should look like this:

```
server {
    listen 80;
    listen [::]:80;
    server_name www.example.org example.org;

    # For the ACME Challenge
    location ~ /.well-known/acme-challenge {
        allow all;
        root /usr/share/nginx/html;
    }

    root /usr/share/nginx/html;
    index index.html;
}
```

We are giving Certbot agent access to `./well-known/acme-challenge`. We run again a new Ngnix container like we did before:

```
$ docker run -it --name nginx-dev -v /volume/etc/nginx/conf.d:/etc/nginx/conf.d \
-v /volume/usr/share/nginx/html:/usr/share/nginx/html -p 80:80 nginx:alpine
```

It\'s time to run Certbot container to get the SSL/TLS certificate. Take in mind that Let\'s Encrypt has rate limits.
Check the rate limits here: https://letsencrypt.org/docs/rate-limits. So if you exceeded the limit and you are having issues 
generating your certificate for whatever reason, you could run into trouble. So, it's always good idea to run the Cerbot agent with
the "--staging" argument which will allow you to test if your commands will execute properly before running Cerbots in the 
Let's Encrypt production enviroment. The limit is higher on Let\'s Encrypt\'s staging environment, so you can use that environment
to debug connectivity problems.

Run the Certbot agent in staging to issue a new Let's Encrypt certificate:

```
$ docker run -it --rm \
-v /volumes/etc/letsencrypt:/etc/letsencrypt \
-v /volumes/var/lib/letsencrypt:/var/lib/letsencrypt \
-v /volumes/var/log/letsencrypt:/var/log/letsencrypt \
-v /volumes/usr/share/nginx/html:/data/letsencrypt \
certbot/certbot \
certonly --webroot \
--register-unsafely-without-email --agree-tos \
--webroot-path=/data/letsencrypt \
--staging \
-d example.org \
-d www.example.org
```

If Cerbot ran successfully in staging, you can run Cerbot in production with some changes.

Wipe the staging files:

```
$ sudo rm -rf /volumes/etc/letsencrypt/* && sudo rm -rf /volumes/var/lib/letsencrypt/* && sudo rm -rf /volumes/var/log/letsencrypt/*
```

And run Cerbot agent again in production:

```
$ docker run -it --rm \
-v /volumes/etc/letsencrypt:/etc/letsencrypt \
-v /volumes/var/lib/letsencrypt:/var/lib/letsencrypt \
-v /volumes/var/log/letsencrypt:/var/log/letsencrypt \
-v /volumes/usr/share/nginx/html:/data/letsencrypt \
certbot/certbot \
certonly --webroot \
--email your@email.com --agree-tos --no-eff-email \
--webroot-path=/data/letsencrypt \
-d example.org \
-d www.example.org
```

Let's Encrypt will send you expiry notifications at your email address.

If everything ran successfully, you can stop the Nginx container and make some changes in the Nginx configuration
to use the certificate in production.


We will need generate a stronger DHE parameter and tell Nginx to use it for DHE key-exchange:

```
$ sudo mkdir -p /volumes/etc/ssl/certs
$ sudo openssl dhparam -out /volumes/etc/ssl/certs/dhparam-2048.pem 2048
```

Now we have to create a new Nginx configuration file:


```
# Redirect to HTTPS and Certificate renewal
server {
    listen      80;
    listen [::]:80;
    server_name example.org www.example.org;

    location / {
        rewrite ^ https://$host$request_uri? permanent;
    }

    # Used by Certbot renewal process
    location ~ /.well-known/acme-challenge {
        allow all;
        root /usr/share/nginx/html;
    }
}

# example.org
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name example.org;

    # Don't send the nginx version number in error pages and Server header
    server_tokens off;

    ssl on;

    ssl_certificate /etc/letsencrypt/live/example.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.org/privkey.pem;

    ssl_buffer_size 8k;

    # Diffie-Hellman parameter for DHE ciphersuites.
    ssl_dhparam /etc/ssl/certs/dhparam-2048.pem;

    # Disable SSLv3 (enabled by default since nginx 0.8.19). It's less secure then TLS
    ssl_protocols TLSv1.2 TLSv1.1 TLSv1;

    # Specifies that server ciphers should be preferred over client ciphers when using 
    # the SSLv3 and TLS protocols. It's used to protect from BEAST attack
    ssl_prefer_server_ciphers on;

    # Specifies the enabled ciphers
    ssl_ciphers ECDH+AESGCM:ECDH+AES256:ECDH+AES128:DH+3DES:!ADH:!AECDH:!MD5;

    ssl_ecdh_curve secp384r1;

    ssl_session_tickets off;

    # enable ocsp stapling (mechanism by which a site can convey certificate revocation
    # information to visitors in a privacy-preserving, scalable manner)
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 8.8.4.4;
    
    # All traffic for https://example.org/* will be redirected to https://www.example.org/*.
    return 301 https://www.example.org$request_uri;
}

# www.example.org
server {
    server_name www.example.org;
    listen 443 ssl http2;
    listen [::]:443 ssl http2;

    # Don't send the nginx version number in error pages and Server header
    server_tokens off;

    ssl on;

    ssl_certificate /etc/letsencrypt/live/example.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.org/privkey.pem;

    ssl_buffer_size 8k;

    # Diffie-Hellman parameter for DHE ciphersuites.
    ssl_dhparam /etc/ssl/certs/dhparam-2048.pem;

    # Disable SSLv3 (enabled by default since nginx 0.8.19). It's less secure then TLS
    ssl_protocols TLSv1.2 TLSv1.1 TLSv1;

    # Specifies that server ciphers should be preferred over client ciphers when using 
    # the SSLv3 and TLS protocols. It's used to protect from BEAST attack
    ssl_prefer_server_ciphers on;

    # Specifies the enabled ciphers
    ssl_ciphers ECDH+AESGCM:ECDH+AES256:ECDH+AES128:DH+3DES:!ADH:!AECDH:!MD5;

    ssl_ecdh_curve secp384r1;

    ssl_session_tickets off;

    # Enable ocsp stapling (mechanism by which a site can convey certificate revocation
    # information to visitors in a privacy-preserving, scalable manner)
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 8.8.4.4;

    root /usr/share/nginx/html;
    index index.html;
}
```

And finally we can run the Nginx container in production with the TLS/SSL certificate

```
$ docker run -it --name nginx-prod \
-v /volumes/etc/nginx/conf.d:/etc/nginx/conf.d \
-v /volumes/usr/share/nginx/html:/usr/share/nginx/html \
-v /volumes/etc/letsencrypt/live/example.org/fullchain.pem:/etc/letsencrypt/live/example.org/fullchain.pem \
-v /volumes/etc/letsencrypt/live/example.org/privkey.pem:/etc/letsencrypt/live/example.org/privkey.pem \
-v /volumes/etc/ssl/certs/dhparam-2048.pem:/etc/ssl/certs/dhparam-2048.pem \
-p 80:80 -p 443:443 nginx:stable-alpine
```
