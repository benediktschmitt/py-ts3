#!/usr/bin/python3


# Modules
# ------------------------------------------------
from distutils.core import setup
from source import __version__


# Main
# ------------------------------------------------
setup(
    name = "ts3",
    version = __version__,
    description = "TS3 Server Query API",
    author = "Benedikt Schmitt",
    author_email = "benedikt@benediktschmitt.de",
    url = "https://github.com/benediktschmitt/py-ts3",
    download_url = "https://github.com/benediktschmitt/Py-TS3/archive/master.zip",
    packages = ["source"],
##    package_dir = {"source": "ts3"},
    license = open("LICENSE").read(),
    )
    
