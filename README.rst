PyTS3
=====

This package provides a **Python 3 API** for:

* TS3 query connections
* TS3 query events
* TS3 file transfers

You can find a complete API documentation
`here <http://py-ts3.readthedocs.org>`_.

Installation
------------

This package is registered on PyPi, so you're done with:

.. code-block:: bash

	$ pip3 install ts3

TS3 Server configuration
------------------------

If you want to send lots of queries to the TS3 server, make sure, that you're
connection is not closed by the **anti-flood protection** of the TS3 server.
So it may be wise to add the host that runs the TS3 queries to the
``query_ip_whitelist.txt`` of your TS3 server:

.. code-block:: bash

	$ echo "192.168.178.42" >> path/to/ts3/server/directory/query_ip_whitelist.txt

Introduction
------------

The easiest way to get to grips with this library is taking a look at the
`examples <https://github.com/benediktschmitt/py-ts3/tree/master/ts3/examples>`_.

If you need information about the possible query commands, take a look at the
**TS3 Server Query Manual**.

Examples
''''''''

You can find more examples in the ``ts3.examples`` package.

*	Show all clients on the virtual server with the server id 1:

	.. code-block:: python

		#!/usr/bin/python3

		import ts3

		with ts3.query.TS3Connection("localhost") as ts3conn:
			# Note, that the client will wait for the response and raise a
			# **TS3QueryError** if the error id of the response is not 0.
			try:
				ts3conn.login(
					client_login_name="serveradmin",
					client_login_password="FoOBa9"
				)
			except ts3.query.TS3QueryError as err:
				print("Login failed:", err.resp.error["msg"])
				exit(1)

			ts3conn.use(sid=1)

			# Each query method will return a **TS3QueryResponse** instance,
			# with the response.
			resp = ts3conn.clientlist()
			print("Clients on the server:", resp.parsed)
			print("Error:", resp.error["id"], resp.error["msg"])

			# Note, the TS3Response class and therefore the TS3QueryResponse
			# class too, can work as a rudimentary container. So, these two
			# commands are equal:
			for client in resp.parsed:
				print(client)
			for client in resp:
				print(client)

*	Say hello to all clients:

	.. code-block:: python

		#!/usr/bin/python3

		import ts3

		with ts3.query.TS3Connection("localhost") as ts3conn:
			ts3conn.login(
				client_login_name="serveradmin",
				client_login_password="FoOBa9"
			)
			ts3conn.use(sid=1)

			for client in ts3conn.clientlist():
				msg = "Hi {}".format(client["client_nickname"])
				ts3conn.clientpoke(clid=client["clid"], msg=msg)

*	Event handling:

	.. code-block:: python

		#!/usr/bin/python3

		import time
		import ts3

		with ts3.query.TS3Connection("localhost") as ts3conn:
			ts3conn.login(
				client_login_name="serveradmin",
				client_login_password="FoOBa9"
			)
			ts3conn.use(sid=1)

			# Register for events
			ts3conn.servernotifyregister(event="server")

			while True:
				event = ts3conn.wait_for_event()

				# Greet new clients.
				if event[0]["reasonid"] == "0":
					print("client connected")
					ts3conn.clientpoke(clid=event[0]["clid"], msg="Hello :)")

*	A simple TS3 viewer:

	.. code-block:: python

		#!/usr/bin/python3

		import ts3

		# The examples package already contains this implementation.
		# Note, that the ts3.examples.viewer module has an helpful class to
		# build a complete channel tree of a virtual server: ChannelTreeNode
		from ts3.examples.viewer import view

		with ts3.query.TS3Connection("localhost") as ts3conn:
			ts3conn.login(
				client_login_name="serveradmin",
				client_login_password="FoOBa9"
			)
			view(ts3conn, sid=1)

*	Download and upload files:

	.. code-block:: python

		#!/usr/bin/python3

		import ts3

		with ts3.query.TS3Connection("localhost") as ts3conn:
			ts3conn.login(
				client_login_name="serveradmin",
				client_login_password="FoOBa9"
			)

			# Create a new TS3FileTransfer instance associated with the
			# TS3Connection.
			ts3ft = ts3.filetransfer.TS3FileTransfer(ts3conn)

			# Upload the image *baz.png* to the channel with the id 2 on the
			# TS3 server.
			# Note the opening mode ("rb").
			with open("baz.png", "rb") as file:
				ts3ft.init_upload(input_file=file, name="/baz.png", cid=2)

			# Download the file into *baz1.png*.
			with open("baz1.png", "wb") as file:
				ts3ft.init_download(output_file=file, name="/baz.png", cid=2)

Bugs
----

If you found a bug please report it or sent a pull request.

Please report grammar or spelling errors too.

Versioning
----------

For the version numbers, take a look at http://semver.org/.

License
-------

This package is licensed under the MIT License.

The docstrings copied from the TS3 Server Query Manual are the property of the
`TeamSpeak Systems GmbH <http://www.teamspeak.com/>`_.
