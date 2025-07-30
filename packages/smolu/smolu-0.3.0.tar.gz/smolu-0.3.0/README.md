# smolu

A file-based url shortener to self-host.

## About

smolu is a very simple piece of software that assume that anyone self-hosting
probably already have a http server running. Thus, this software really just
create a static html file for each short url.

This provide an unbeatable safety: urls are only managed by a user of the
machine (assuming ssh with private key authentication), so there is no roon for
SQL injection, complex authentication method, or fragile admin interface.

## Features

- Configurable short url length
- Opt-in QR code generation
- Self-hosted
- No SEO bullshit, analytics, tracking, ads, payed plan
- No database or longrunning process (apart from whatever http server you are running)
- No attack surface (assuming you are using a production grade http server such
  as nginx or caddy with TLS enabled)

## Installation

1. Install the package on your system (it is recommended that you do that as a
   non-root user):
```bash
pip install smolu
```
or

```bash
git clone https://git.sr.ht/~lattay/smolu
cd smolu
pip install .
```

Optionally you want to install `qrencode` to be able to generate QR codes.

2. Configure the http server to serve the /srv/http/u/ directory statically (or
   a different root of your choice, see section [Configuration](#Configuration))
   and set the `Content-Type` header properly (see [Sample server config](#Sample-server-config))


3. Ensure the user has write permissions (obviouly you can skip that step if you intend
   to run smolu as root):

```bash
# we use the www-data here, but any group name will do
sudo groupadd www-data
sudo chgrp -R www-data /srv/http/u
sudo chmod -R g+w /srv/http/u
sudo usermod -aG www-data $USER
```

Then logout and login to apply the group change to the user.

4. Configure the shortener (see section [Configuration](#Configuration))

## Usage

Run `smolu.py <target>`, it will print the short url to stdout.
If enabled, the QR code will be found at `<short_url>.png`

Note: this is designed for individual user, meaning it is not designed for
millions of urls, or for super fast generation. It will check for collisions
though (in a parallel unsafe way though, again a single user won't have a
problem). The default is to use 4 bytes of timestamp and 2 random bytes, however
even 2+1 should be just fine for personal use. The bytes are base64 encoded so
for each 3 bytes of the id, you get 4 characters in the url.

## Configuration

The configuration is done with `smolu -C`.
```
$ smolu -c
Configure wizard:
URL prefix?
Default: example.com/u/
> mydom.io/u/
Server root?
Default: /srv/http/u
>
Random byte length?
Default: 2
> 1
Timestamp byte length?
Default: 4
> 2
Generate QR code?
Default: no
> yes
Current configuration:
{
    "server_address_prefix": "mydom.io/u/",
    "server_root": "/srv/http/u",
    "template": "\n<!DOCTYPE HTML>\n<html lang=\"en-US\">\n    <head>\n        <meta charset=\"UTF-8\">\n        <meta http-equiv=\"refresh\" content=\"0; url={url}\">\n    </head>\n    <body>\n        If you are not redirected automatically, follow this <a href='{url}'>link</a>.\n    </body>\n</html>\n",
    "random_byte_length": 1,
    "timestamp_byte_length": 2,
    "gen_qr": true
}
```

You can also change the JSON file manually at `~/.config/smolu.json`

The template is changed with a separate flag:
```
$ smolu -T <<EOF
<!DOCTYPE HTML>
<html lang="en-US">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="0; url={url}">
    </head>
    <body><a href='{url}'>link</a>.</body>
</html>
EOF
```

Currently the only field supported by the template is `{url}`.
This is a python `.format` style template, so if you need literal `{` or `}` you
need to double then.

## Sample server config

As mentioned before, smolu only creates file, but you are responsible for
serving them.
What the server must do is:
- serve static files found in `/srv/http/u/` or whatever root you have configured
- set the `Content-Type` header of the generated files to `text/html; charset=utf-8` (because they have no extension)
- set the `Content-Type` header of the `/u/*.png` files to `image/png` (that's
usually automatic, but you need to make sure the other action does not override
the normal behaviour)

Here are some examples of achieving that with two of the very best open-source
http servers out there.

### [Caddy](https://caddyserver.com/)

[doc for the Caddyfile](https://caddyserver.com/docs/caddyfile):

```
example.com:443 {
	root * /srv/http
	@html {
		path /u/*
		not path *.png
	}
	header @html Content-Type "text/html; charset=utf-8"
	file_server
}
```

### [Nginx](https://nginx.org/)

[doc for the static file part](https://docs.nginx.com/nginx/admin-guide/web-server/serving-static-content/):

```
server {
    listen 443 ssl;
    server_name example.com;

    root /srv/http;

    ssl_certificate /path/to/fullchain.pem;
    ssl_certificate_key /path/to/privkey.pem;

    location ~ ^/u/.*\.png$ {
        # nothing special
    }

    location /u/ {
        add_header Content-Type "text/html; charset=utf-8";
    }
}

server {
    listen 80;
    server_name example.com;
    return 301 https://$host$request_uri;
}
```
