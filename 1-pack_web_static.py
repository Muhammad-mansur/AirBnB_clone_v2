#!/usr/bin/python3
""" generates a .tgz archive from the contents of the web_static folder """
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    # Create versions directory if it doesn't exist
    local("mkdir -p versions")

    # Get current time for the archive name
    now = datetime.now()
    time_format = now.strftime("%Y%m%d%H%M%S")
    archive_name = f"web_static_{time_format}.tgz"
    archive_path = os.path.join("versions", archive_name)

    # Create the archive
    result = local(f"tar -cvzf {archive_path} web_static")

    # Check if the archive was created successfully
    if result.failed:
        return None
    return archive_path
