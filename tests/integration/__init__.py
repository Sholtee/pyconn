# RPC.NET-Connector integration tests
# __init__.py
# Author: Denes Solti

from os import getcwd, makedirs, path
from zipfile import ZipFile

cwd = getcwd()

if not path.exists(backend_dir := path.join(cwd, '.tmp', 'backend')):
    makedirs(backend_dir)
    with ZipFile(path.join(cwd, 'backend.zip') , 'r') as zip_file:
        zip_file.extractall(backend_dir)