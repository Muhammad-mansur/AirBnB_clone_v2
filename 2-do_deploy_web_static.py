#!/usr/bin/python3
"""Distributes an archive to your web servers, using the function do_deploy"""
from fabric.api import Connection, task
import os

# Define the hosts
env_hosts = ["52.3.246.184", "100.25.15.100"]


@task
def do_deploy(c, archive_path):
    """Function for deploy"""
    if not os.path.exists(archive_path):
        return False

    # Extract the archive file name and the name without extension
    archive_file = os.path.basename(archive_path)
    name_no_ext = os.path.splitext(archive_file)[0]

    # Define the destination directory
    dest = f"/data/web_static/releases/{name_no_ext}/"

    try:
        # Loop through each host and perform operations
        for host in env_hosts:
            conn = Connection(
                host,
                user=c.user,
                connect_kwargs={
                    "key_filename": c.connect_kwargs["key_filename"]})

            # Upload the archive to the /tmp/ directory on the server
            conn.put(archive_path, '/tmp/')

            # Create the destination directory
            conn.run(f'mkdir -p {dest}')

            # Uncompress the archive to the destination directory
            conn.run(f'tar -xzf /tmp/{archive_file} -C {dest}')

            # Remove the archive from the /tmp/ directory
            conn.run(f'rm /tmp/{archive_file}')

            # Move the contents of the web_static to the destination directory
            conn.run(f'mv {dest}web_static/* {dest}')

            # Remove the now empty web_static directory
            conn.run(f'rm -rf {dest}web_static')

            # Remove the existing symbolic link
            conn.run('rm -rf /data/web_static/current')

            # Create a new symbolic link to the new version
            conn.run(f'ln -s {dest} /data/web_static/current')

        return True
    except Exception as e:
        print(e)
        return False
