#!/usr/bin/python3

from fabric import Connection, task
import os

""" Distributes an archive to your web servers,
using the function do_deploy """

env_hosts = ["52.3.246.184", "100.25.15.100"]


@task
def do_deploy(c, archive_path):
    """Function for deploy"""
    if not os.path.exists(archive_path):
        return False

    data_path = '/data/web_static/releases/'
    tmp = archive_path.split('.')[0]
    name = tmp.split('/')[1]
    dest = data_path + name

    try:
        # Loop through each host and perform operations
        for host in env_hosts:
            conn = Connection(
                host,
                user=c.user,
                connect_kwargs={
                    "key_filename": c.connect_kwargs["key_filename"]})
            conn.put(archive_path, '/tmp')
            conn.run(f'mkdir -p {dest}')
            conn.run(f'tar -xzf /tmp/{name}.tgz -C {dest}')
            conn.run(f'rm -f /tmp/{name}.tgz')
            conn.run(f'mv {dest}/web_static/* {dest}/')
            conn.run(f'rm -rf {dest}/web_static')
            conn.run('rm -rf /data/web_static/current')
            conn.run(f'ln -s {dest} /data/web_static/current')
        return True
    except Exception as e:
        print(e)
        return False
