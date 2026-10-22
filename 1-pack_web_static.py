#!/usr/bin/env python3
"""Create a timestamped archive of the web_static directory."""

import os
from datetime import datetime

from fabric.api import local, task


@task
def do_pack():
    """Archive web_static and return its path, or None on failure."""
    if not os.path.isdir("web_static"):
        print("web_static directory is missing")
        return None

    versions_dir = "versions"
    archive_name = "web_static_{}.tgz".format(datetime.now().strftime("%Y%m%d%H%M%S"))
    archive_path = os.path.join(versions_dir, archive_name).replace("\\", "/")

    try:
        local("mkdir -p {}".format(versions_dir))
        result = local("tar -czf {} web_static".format(archive_path), capture=True)
        if result.failed or not os.path.isfile(archive_path):
            print("Failed to create {}".format(archive_path))
            return None
        print("web_static packed: {} -> {} bytes".format(
            archive_path, os.path.getsize(archive_path)
        ))
        return archive_path
    except Exception as error:
        print("Failed to pack web_static: {}".format(error))
        return None
