#!/usr/bin/env python3
"""Pack web_static and deploy the archive to both web servers."""

import os
import importlib.util

from fabric.api import task


_directory = os.path.dirname(os.path.abspath(__file__))


def _load_module(name, path):
    """Load a sibling module whose filename begins with a number."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_pack_module = _load_module(
    "pack_web_static", os.path.join(_directory, "1-pack_web_static.py")
)
_deploy_module = _load_module(
    "deploy_web_static", os.path.join(_directory, "2-do_deploy_web_static.py")
)


@task
def deploy():
    """Create an archive, then deploy it; return the deployment result."""
    archive_path = _pack_module.do_pack()
    if not archive_path:
        return False
    return _deploy_module.do_deploy(archive_path)
