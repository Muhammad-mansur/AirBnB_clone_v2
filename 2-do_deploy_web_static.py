from fabric import Connection, task
from os.path import exists
import os

env_hosts = ['52.3.246.184', '100.25.15.100']

@task
def do_deploy(c, archive_path):
    """Distributes an archive to the web servers"""
    if not exists(archive_path):
        return False

    try:
        file_n = os.path.basename(archive_path)
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"

        for host in env_hosts:
            conn = Connection(host)
            conn.put(archive_path, '/tmp/')
            conn.run(f'mkdir -p {path}{no_ext}/')
            conn.run(f'tar -xzf /tmp/{file_n} -C {path}{no_ext}/')
            conn.run(f'rm /tmp/{file_n}')
            conn.run(f'mv {path}{no_ext}/web_static/* {path}{no_ext}/')
            conn.run(f'rm -rf {path}{no_ext}/web_static')
            conn.run('rm -rf /data/web_static/current')
            conn.run(f'ln -s {path}{no_ext}/ /data/web_static/current')

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
