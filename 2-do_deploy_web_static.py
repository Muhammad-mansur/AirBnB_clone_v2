#!/usr/bin/python3
""" Distributes an archive to your web servers, using the function do_deploy """
from fabric.api import env, put, run
import os


# Define the web servers
env.hosts = ['54.236.26.75', '54.157.148.181']

def do_deploy(archive_path):
    """Distributes an archive to web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        archive_filename = os.path.basename(archive_path)
        archive_foldername = archive_filename.split('.')[0]
        tmp_path = f"/tmp/{archive_filename}"

        put(archive_path, tmp_path)

        # Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension>
        release_folder = f"/data/web_static/releases/{archive_foldername}"
        run(f"mkdir -p {release_folder}")
        run(f"tar -xzf {tmp_path} -C {release_folder}")
        run(f"rm {tmp_path}")
        run(f"mv {release_folder}/web_static/* {release_folder}")
        run(f"rm -rf {release_folder}/web_static")

        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current on the web server, linked to the new version
        run(f"ln -s {release_folder} /data/web_static/current")

        return True

    except:
        return False
