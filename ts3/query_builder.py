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

This module contains a flexible query builder which is modeled after the *COMMAND SYNTAX* section
in the TS3 Server Query Manual.

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

    Please note, that query builder objects are *immutable*.

    :arg ~ts3.query.TS3BaseConnection ts3conn:
        The TS3 connection which will be used to send the query.
    :arg str cmd:
        The name of the command to execute, e.g. ``"clientkick"``.
    :arg list pipes:
        A list of ``(options, params)`` in which options is a
        *set* and *params* is a *dictionary*.

    :seealso: \
        :meth:`ts3.query.TS3BaseConnection.query`,
        :meth:`ts3.query.TS3BaseConnection.exec_query`

    :todo: What about the crazy *properties*??
    """

    def __init__(self, ts3conn, cmd, pipes=None):
        self._ts3conn = ts3conn
        self._cmd = cmd

        # List of (options, params).
        self._pipes = pipes or []
        return None

    def copy(self):
        """Returns a copy of the query builder."""
        pipes_cp = [
            (options.copy(), params.copy()) for options, params in self._pipes
        ]
        return TS3QueryBuilder(self._ts3conn, self._cmd, pipes_cp)

    def pipe(self, *options, **params):
        """
        Starts a new pipe:

        .. code-block:: python

            q = ts3conn.query("clientkick").pipe(clid=1).pipe(clid=2).pipe(clid=3)
        """
        cp = self.copy()
        cp._pipes.append((options, params))
        return cp

    def options(self, *options):
        """
        Adds the options to the last pipe:

        .. code-block:: python

            q = q.pipe().options("foo").pipe().options("bar").pipe().options("baz")

        You should prefer passing the options directly to :meth:`pipe` as it
        is more readable.
        """
        cp = self.copy()
        last_options, _ = cp.pipes[-1]
        last_options.update(options)
        return cp

    def params(self, **params):
        """
        Adds the parameters to the last pipe:

        .. code-block:: python

            q = ts3conn.query("clientkick").pipe().options(clid=1).pipe().options(clid=2)

        You should prefer passing the options directly to :meth:`pipe` as it
        is more readable.
        """
        cp = self.copy()
        _, last_params = cp.pipes[-1]
        last_params.update(params)
        return cp

    def compile(self):
        """
        Compiles the query into a TS3 query command and returns it:

        .. code-block:: python

            >>> q = TS3QueryBuilder("clientkick", reasonid=5, reasonmsg="Go away!")\\
            ...     .pipe(clid=1).pipe(clid=2).pipe(clid=3)
            >>> q.compile()
            'clientkick reasonid=5 reasonmsg=Go\saway! clid=1|clid=2|clid=3'
        """
        # NOTE: If it turns out, that string addition is too slow, we can still
        #       use other means.
        res = self._cmd

        if self._pipes:
            last_pipe = self._pipes[-1]

            for pipe in self._pipes:
                options, params = pipe

                for option in options:
                    res += " -" + option

                for key, value in params.items():
                    if isinstance(value, bool):
                        value = "1" if value else "0"
                    else:
                        value = escape(str(value))
                    res += " " + key + "=" + value

                    if pipe is not last_pipe:
                        res += " |"

        res += "\n\r"
        return res.encode()

    def __str__(self):
        return self.compile()

    def fetch(self):
        """Executes the query and returns the :class:`TS3QueryResponse`.

        :seealso: :meth:`TS3BaseConnection.exec_query`
        """
        return self._ts3conn.exec_query(self)

    #: Alias for :meth:`fetch`, but indicates that the result is not needed.
    exec = fetch

    def first(self):
        """Executes the query and returns the first item in the parsed
        response. Use this method if you are only interested in the
        first item of the response.

        If the response did not contain any items, then ``None`` is returned.

        :seealso: :meth:`TS3BaseConnection.exec_query`,\
            :attr:`TS3QueryResponse.parsed`
        """
        resp = self.fetch()
        return resp.parsed[0] if resp.parsed else None

    def all(self):
        """Executes the query and returns the parsed response. Use this
        method if you are interested in the parsed response rather than the
        resoonse object.

        :seealso: :meth:`TS3BaseConnection.exec_query`,\
            :attr:`TS3QueryResponse.parsed`
        """
        resp = self.fetch()
        return resp.parsed
