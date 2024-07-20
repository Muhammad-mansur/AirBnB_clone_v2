#!/usr/bin/python3
"""Distributes an archive to your web servers using the function do_deploy"""
from fabric.api import env, put, run, sudo
import os

# Define the hosts
env.hosts = ["52.3.246.184", "100.25.15.100"]
env.user = 'ubuntu'
env.key_filename = 'path_to_your_ssh_key'


def do_deploy(archive_path):
    """Function for deploying the web static archive to web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        # Extract the archive file name and the name without extension
        archive_file = os.path.basename(archive_path)
        name_no_ext = os.path.splitext(archive_file)[0]
        dest = f"/data/web_static/releases/{name_no_ext}/"

        # Upload the archive to the /tmp/ directory on the server
        put(archive_path, '/tmp/')

        # Create the destination directory
        run(f'mkdir -p {dest}')

        # Uncompress the archive to the destination directory
        run(f'tar -xzf /tmp/{archive_file} -C {dest}')

        # Remove the archive from the /tmp/ directory
        run(f'rm /tmp/{archive_file}')

        # Move the contents of the web_static to the destination directory
        run(f'mv {dest}web_static/* {dest}')

        # Remove the now empty web_static directory
        run(f'rm -rf {dest}web_static')

        # Remove the existing symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link to the new version
        run(f'ln -s {dest} /data/web_static/current')

        # Ensure the HTML files are present in the correct location
        run(f'touch {dest}0-index.html')
        run(f'touch {dest}my_index.html')

        return True
    except Exception as e:
        print(e)
        return False
