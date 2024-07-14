#!/usr/bin/env bash
# This script sets up web servers for the deployment of web_static


# Update and install Nginx if it is not already installed
if ! which nginx > /dev/null 2>&1; then
    sudo apt-get update -y
    sudo apt-get install -y nginx
fi

# Create required directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file to test Nginx configuration
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create a symbolic link, recreating it if it already exists
if [ -L /data/web_static/current ]; then
    sudo rm /data/web_static/current
fi
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ folder to ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve content of /data/web_static/current/ to hbnb_static
sudo sed -i '/listen 80 default_server;/a location /hbnb_static/ { alias /data/web_static/current/; autoindex off; }' /etc/nginx/sites-available/default

# Restart Nginx to apply the changes
sudo service nginx restart

# Exit successfully
exit 0
