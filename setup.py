#!/usr/bin/python3


# Modules
# ------------------------------------------------
from distutils.core import setup
from ts3 import __version__


# Main
# ------------------------------------------------
setup(
    name = "ts3",
    version = __version__,
    description = "TS3 Server Query API",
    long_description = open("README.md").read(),
    author = "Benedikt Schmitt",
    author_email = "benedikt@benediktschmitt.de",
    url = "https://github.com/benediktschmitt/py-ts3",
    download_url = "https://github.com/benediktschmitt/Py-TS3/archive/master.zip",
    packages = ["ts3"],
    license = open("LICENSE").read(),
    )
    
