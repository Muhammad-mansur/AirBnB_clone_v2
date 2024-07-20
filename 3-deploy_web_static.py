#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to web servers"""

from fabric.api import env
from fabric.api import local
from fabric.api import run
from fabric.api import put
import os
from datetime import datetime

# Define the list of hosts
env.hosts = ['52.3.246.184', '100.25.15.100']

def do_pack():
    """Creates a .tgz archive from the contents of web_static folder"""
    date_str = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = f"web_static_{date_str}.tgz"
    archive_path = f"versions/{archive_name}"

    # Create the versions directory if it does not exist
    if not os.path.exists("versions"):
        os.makedirs("versions")

    # Create the archive
    result = local(f"tar -cvzf {archive_path} web_static", capture=True)

    # Check if the archive was created successfully
    if result.failed:
        return None

    return archive_path

def do_deploy(archive_path):
    """Distributes an archive to web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        file_name = os.path.basename(archive_path)
        no_ext = os.path.splitext(file_name)[0]
        release_path = f"/data/web_static/releases/{no_ext}"

        # Upload the archive to the /tmp/ directory on the server
        put(archive_path, '/tmp/')

        # Create the release directory and unpack the archive
        run(f'mkdir -p {release_path}')
        run(f'tar -xzf /tmp/{file_name} -C {release_path}')

        # Remove the archive from /tmp/
        run(f'rm /tmp/{file_name}')

        # Move the contents of web_static to the release directory
        run(f'mv {release_path}/web_static/* {release_path}/')
        run(f'rm -rf {release_path}/web_static')

        # Remove the existing symbolic link and create a new one
        run(f'rm -rf /data/web_static/current')
        run(f'ln -s {release_path} /data/web_static/current')

        return True
    except Exception as e:
        print(e)
        return False

def deploy():
    """Creates and deploys an archive"""
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
