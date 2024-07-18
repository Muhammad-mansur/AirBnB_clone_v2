from fabric import Connection, task
import os

env_hosts = ['xx-web-01', 'xx-web-02']

def do_deploy(archive_path):
    """Distributes an archive to web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        # Archive path components
        archive_filename = os.path.basename(archive_path)
        archive_foldername = archive_filename.split('.')[0]
        tmp_path = f"/tmp/{archive_filename}"
        release_folder = f"/data/web_static/releases/{archive_foldername}"

        for host in env_hosts:
            # Establish connection to the host
            conn = Connection(host)

            # Upload the archive to the /tmp/ directory of the web server
            conn.put(archive_path, tmp_path)

            # Uncompress the archive to the release folder
            conn.run(f"mkdir -p {release_folder}")
            conn.run(f"tar -xzf {tmp_path} -C {release_folder}")
            conn.run(f"rm {tmp_path}")

            # Move contents out of the web_static folder
            conn.run(f"mv {release_folder}/web_static/* {release_folder}/")
            conn.run(f"rm -rf {release_folder}/web_static")

            # Delete the symbolic link /data/web_static/current from the web server
            conn.run("rm -rf /data/web_static/current")

            # Create a new symbolic link /data/web_static/current on the web server, linked to the new version
            conn.run(f"ln -s {release_folder} /data/web_static/current")

        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

@task
def deploy(c, archive_path):
    """Task to deploy the archive to the servers"""
    if do_deploy(archive_path):
        print("Deployment successful")
    else:
        print("Deployment failed")
