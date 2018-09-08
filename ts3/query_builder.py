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
:mod:`ts3.query_builder`
========================

This module contains a flexible query builder which is modeled after the
*COMMAND SYNTAX* section in the TS3 Server Query Manual.

:versionadded: 2.0.0
"""

# local
from .escape import escape
from .common import TS3Error


__all__ = [
    "TS3QueryBuilder"
]


class TS3QueryBuilder(object):
    """Simplifies building a valid TS3 query.

    .. code-block:: python

        # When you are interested in the whole response.
        resp = TS3QueryBuilder(ts3conn, "clientkick").pipe(pattern="Ben").fetch()

        # When you are only interested in the first item in the response.
        resp = TS3QueryBuilder(ts3conn, "serverlist").first()

        # When you are only interested in the items, but not in the actual
        # response object.
        resp = TS3QueryBuilder(ts3conn, "serverlist").all()

    Please note, that query builder objects are **not immutable**.

    :arg str cmd:
        The name of the command to execute, e.g. ``"clientkick"``.
    :arg ~ts3.query.TS3BaseConnection ts3conn:
        The TS3 connection which will be used to send the query.
    :arg list pipes:
        A list of ``(options, params)`` in which options is a
        *set* and *params* is a *dictionary*.

    :seealso: \
        :meth:`ts3.query.TS3BaseConnection.query`,
        :meth:`ts3.query.TS3BaseConnection.exec_query`

    :todo: What about the crazy *properties* in the documentation, what are they?
    """

    def __init__(self, cmd, ts3conn=None, pipes=None):
        self._ts3conn = ts3conn
        self._cmd = cmd

        # List of (options, params).
        self._pipes = pipes or [(set(), dict())]
        return None

    def pipe(self, *options, **params):
        """
        Starts a new pipe:

        .. code-block:: python

            >>> q = TS3QueryBuilder("clientkick").pipe(clid=1).pipe(clid=2)
            >>> print(q)
            'clientkick clid=1 | clid=2'
        """
        last_options, last_params = self._pipes[-1] if self._pipes else (None, None)

        if not self._pipes:
            self._pipes.append((set(options), params))
        elif last_options or last_params:
            self._pipes.append((set(options), params))
        else:
            last_options.update(options)
            last_params.update(params)
        return self

    def options(self, *options):
        """
        Adds the options to the last pipe:

        .. code-block:: python

            >>> q = TS3QueryBuilder("clientkick").options("foo").pipe().options("bar")
            >>> print(q)
            'clientkick -foo | -bar'

        You should prefer passing the options directly to :meth:`pipe` as it
        is more readable.

        .. note::

            Most commands do not support pipelining options.
        """
        last_options, _ = self._pipes[-1]
        last_options.update(options)
        return self

    def params(self, **params):
        """
        Adds the parameters to the last pipe:

        .. code-block:: python

            >>> q = TS3QueryBuilder("clientkick")\\
            ...     .pipe().params(clid=1)\\
            ...     .pipe().params(clid=2)
            >>> print(q)
            'clientkick clid=1 | clid=2'

        You should prefer passing the options directly to :meth:`pipe` as it
        is more readable.
        """
        _, last_params = self._pipes[-1]
        last_params.update(params)
        return self

    def compile(self):
        """
        Compiles the query into a TS3 query command and returns it:

        .. code-block:: python

            # Strings are escaped automatic.
            >>> q = TS3QueryBuilder("clientkick").params(reasonid=5, reasonmsg="Go away!")\\
            ...     .pipe(clid=1).pipe(clid=2)
            >>> q.compile()
            'clientkick reasonid=5 reasonmsg=Go\saway! | clid=1 | clid=2'

            # Booleans are turned into 0 or 1.
            >>> q = TS3QueryBuilder("clientupdate").params(client_input_muted=True)
            >>> q.compile()
            'clientupdate client_input_muted=1'

        :rtype: str
        :returns:
            A valid TS3 query command string with arguments and options.
        """
        res = self._cmd

        if self._pipes:
            last_pipe = self._pipes[-1]

            for pipe in self._pipes:
                options, params = pipe

                for key, value in params.items():
                    if isinstance(value, bool):
                        value = "1" if value else "0"
                    else:
                        value = escape(str(value))
                    res += " " + key + "=" + value

                for option in options:
                    res += " -" + option

                if pipe is not last_pipe:
                    res += " |"
        return res

    def __str__(self):
        return self.compile()

    def fetch(self):
        """Executes the query and returns the :class:`TS3QueryResponse`.

        :seealso: :meth:`TS3BaseConnection.exec_query`
        """
        return self._ts3conn.exec_query(self)

    def first(self):
        """Executes the query and returns the first item in the parsed
        response. Use this method if you are only interested in the
        first item of the response.

        If the response did not contain any items, then ``None`` is returned.

        :seealso: :meth:`ts3.query.TS3BaseConnection.exec_query`,\
            :attr:`ts3.query.TS3QueryResponse.parsed`
        """
        resp = self.fetch()
        return resp.parsed[0] if resp.parsed else None

    def all(self):
        """Executes the query and returns the parsed response. Use this
        method if you are interested in the parsed response rather than the
        resoonse object.

        :seealso: :meth:`ts3.query.TS3BaseConnection.exec_query`,\
            :attr:`ts3.query.TS3QueryResponse.parsed`
        """
        resp = self.fetch()
        return resp.parsed
