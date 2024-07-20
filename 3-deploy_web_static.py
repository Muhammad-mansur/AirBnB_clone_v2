#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers.
"""
from fabric.api import local, put, run, env
from datetime import datetime
from os.path import exists

# Define your hosts and user
env.hosts = ['52.3.246.184', '100.25.15.100']
env.user = 'ubuntu'
env.key_filename = 'my_ssh_private_key'

def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""
    try:
        # Create versions directory if not exists
        local("mkdir -p versions")
        
        # Create the archive with timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = f"versions/web_static_{timestamp}.tgz"
        
        # Create the archive
        local(f"tar -cvzf {archive_path} web_static")
        
        # Check if the archive was created
        if exists(archive_path):
            print(f"Archive created at: {archive_path}")
            return archive_path
        else:
            print("Failed to create archive.")
            return None
    except Exception as e:
        print(f"An error occurred while packing: {e}")
        return None

def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    if not exists(archive_path):
        print(f"Archive path {archive_path} does not exist.")
        return False
    
    try:
        file_name = archive_path.split("/")[-1]
        name_no_ext = file_name.split(".")[0]
        dest = f"/data/web_static/releases/{name_no_ext}/"
        
        # Upload the archive
        put(archive_path, '/tmp/')
        
        # Uncompress the archive
        run(f"mkdir -p {dest}")
        run(f"tar -xzf /tmp/{file_name} -C {dest}")
        run(f"rm /tmp/{file_name}")
        
        # Move the contents and clean up
        run(f"mv {dest}web_static/* {dest}")
        run(f"rm -rf {dest}web_static")
        
        # Remove the current symlink and create a new one
        run("rm -rf /data/web_static/current")
        run(f"ln -s {dest} /data/web_static/current")
        
        print("Deployment successful!")
        return True
    except Exception as e:
        print(f"An error occurred while deploying: {e}")
        return False

def deploy():
    """Creates and distributes an archive to your web servers"""
    archive_path = do_pack()
    if not archive_path:
        return False
    
    return do_deploy(archive_path)
