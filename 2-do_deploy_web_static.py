#!/usr/bin/env python3
"""Upload and deploy a web_static archive to both web servers."""

import os

from fabric.api import env, put, run, task


hosts = os.environ.get("HBNB_WEB_HOSTS", "")
env.hosts = [host.strip() for host in hosts.split(",") if host.strip()]


@task
def do_deploy(archive_path):
    """Deploy an existing archive to the configured hosts."""
    if not archive_path or not os.path.isfile(archive_path):
        return False
    if not env.hosts:
        print("Set HBNB_WEB_HOSTS to the comma-separated addresses of both servers.")
        return False

    archive_name = os.path.basename(archive_path)
    if not archive_name.endswith(".tgz"):
        return False
    release_name = archive_name[:-4]
    remote_archive = "/tmp/{}".format(archive_name)
    release_path = "/data/web_static/releases/{}".format(release_name)
    current_path = "/data/web_static/current"

    try:
        put(archive_path, remote_archive)
        # The archive contains web_static/ at its root. Strip that component
        # while extracting so hidden files are deployed too.
        run(
            "set -e; mkdir -p {release}; "
            "tar --strip-components=1 -xzf {archive} -C {release}; "
            "rm -f {archive}; rm -rf {current}; "
            "ln -s {release} {current}".format(
                release=release_path,
                archive=remote_archive,
                current=current_path,
            )
        )
        print("New version deployed!")
        return True
    except Exception as error:
        print("Deployment failed on a host: {}".format(error))
        return False
