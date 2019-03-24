#!/usr/bin/env python3

# The MIT License (MIT)
#
# Copyright (c) 2013-2018 <see AUTHORS.txt>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
.. _api:

:mod:`ts3`
==========

.. toctree::
    :maxdepth: 1
    :titlesonly:
    :glob:

    common
    escape
    response
    definitions
    query
    query_builder
    filetransfer

This package contains a Python API for the:

    * TeamSpeak 3 Server Query,
    * TeamSpeak 3 Client Query,
    * TeamSpeak 3 Filetransfer Interface,
    * and TeamSpeak 3 Query Events.
"""


__version__ = "2.0.0b3"


# Only export some high level modules.
from . import common
from . import definitions
from . import escape
from . import filetransfer
from . import query
from . import response

# Only export some classes directly.
from .common import TS3Error
