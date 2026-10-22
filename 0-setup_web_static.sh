#!/usr/bin/env bash
# Prepare an Ubuntu web server to serve static files for the AirBnB clone.
# Run with: sudo bash ./0-setup_web_static.sh

warn() {
    printf 'Warning: %s\n' "$1" >&2
}

if [ "$(id -u)" -ne 0 ]; then
    warn 'Run this script with sudo so it can configure Nginx and /data.'
    exit 0
fi

if command -v apt-get >/dev/null 2>&1; then
    if ! command -v nginx >/dev/null 2>&1; then
        apt-get update || warn 'apt-get update failed.'
        DEBIAN_FRONTEND=noninteractive apt-get install -y nginx || warn 'Nginx installation failed.'
    fi
else
    warn 'apt-get is unavailable; this setup script expects Ubuntu or Debian.'
fi

mkdir -p /data/web_static/releases/test /data/web_static/shared || warn 'Could not create the web_static directories.'

if [ -d /data/web_static/releases/test ]; then
    cat > /data/web_static/releases/test/index.html <<'HTML'
<html>
  <head><title>Static deployment test</title></head>
  <body>AirBnB web_static is working!</body>
</html>
HTML
    [ $? -eq 0 ] || warn 'Could not write the test index.html.'
fi

rm -rf /data/web_static/current || warn 'Could not remove the previous current link.'
ln -s /data/web_static/releases/test /data/web_static/current || warn 'Could not create the current symlink.'
chown -R ubuntu:ubuntu /data || warn 'Could not set ownership of /data.'

if [ -d /etc/nginx/sites-available ]; then
    cat > /etc/nginx/sites-available/default <<'NGINX'
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;

    location /hbnb_static/ {
        alias /data/web_static/current/;
        autoindex off;
    }

    location / {
        return 404;
    }
}
NGINX
    [ $? -eq 0 ] || warn 'Could not write the Nginx default site configuration.'

    ln -sfn /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default || warn 'Could not enable the Nginx default site.'
else
    warn 'Nginx sites-available directory was not found.'
fi

if command -v nginx >/dev/null 2>&1 && nginx -t; then
    if command -v systemctl >/dev/null 2>&1; then
        systemctl restart nginx || warn 'Could not restart Nginx with systemctl.'
    else
        service nginx restart || warn 'Could not restart Nginx.'
    fi
else
    warn 'Nginx configuration check failed; Nginx was not restarted.'
fi

# The assignment requires a successful exit status even when a setup command
# fails. Warnings above identify any work that needs attention.
exit 0
