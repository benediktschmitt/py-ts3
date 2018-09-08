PyTS3
=====

`Installation <#installation>`_
~ `TS3 Server Whitelist <#ts3-server-whitelist>`_
~ `Introduction <#introduction>`_
~ `Examples <#examples>`_
~ `Changelog <https://py-ts3.readthedocs.io/en/v2/changelog.html>`_
~ `Bugs <#bugs>`_
~ `License <#license>`_

**>> Click** `here <https://py-ts3.readthedocs.io/en/v2/changelog.html>`_ **to find out what's new in version 2.0.0. <<**

This package provides a **Python 3 API** for

* TS3 query connections,
* TS3 query events,
* TS3 file transfers,
* the TS3 client query interface,
* and TS3 client events.

You can find a complete API documentation
`here <http://py-ts3.readthedocs.io/en/v2/>`_.

.. code-block:: python

	import ts3

	# Change the URI scheme from *ssh* to *telnet*, if your server does not
	# support ssh.
	with ts3.query.TS3ServerConnection("ssh://serveradmin:Z0YxRb7u@localhost:10022") as ts3conn:
		# use sid=1
		ts3conn.exec_("use", sid=1)

		# clientlist -away -uid
		clients = ts3conn.query("clientlist", "away", "uid").all()

Installation
------------

This package is registered on PyPi, so you're done with:

.. code-block:: bash

	$ pip3 install ts3

TS3 Server Whitelist
--------------------

If you want to send lots of queries to the TS3 server, make sure, that you're
connection is not closed by the **anti-flood protection** of the TS3 server.
So it may be wise to add the host that runs the TS3 queries to the
``query_ip_whitelist.txt`` of your TS3 server:

.. code-block:: bash

	$ echo "192.168.178.42" >> path/to/ts3/server/directory/query_ip_whitelist.txt

Introduction
------------

The easiest way to get to grips with this library is taking a look at the
`examples <https://github.com/benediktschmitt/py-ts3/tree/master/ts3/examples>`_ or
simply read through the small ones in this README.

If you need information about the possible query commands, take a look at the
**TS3 Server Query Manual**, which comes as a html file in the server installation
folder, or at the **TS3 Client Query Manual** which is located in the client
installation folder.

TS3 Query Commands
''''''''''''''''''
(Excerpt from the manual)

Query commands are made up of a command word, options and parameters (key-value pairs):

.. code-block:: raw

	command key1=value1 key2=value2 key3=value3 -option1 -option1

This syntax translates into *py-ts3* as follows:

.. code-block:: python

	ts3conn.exec_("command", "option1", "option2", key1=value1, key2=value2)
	ts3conn.query("command", "option1", "option2", key1=value1, key2=value2).fetch()

The *exec()* method executes the command immediately and is often sufficient,
while the *query()* method offers a slightly more sophisticated interface and
supports pipelining:

.. code-block:: python

	# clientkick reasonid=5 reasonmsg=Go\saway! clid=1|clid=2|clid=3
	resp = ts3conn.query("clientkick", reasonid=5, reasonmsg="Go away!")\
		.pipe(clid=1).pipe(clid=2).pipe(clid=3).fetch()

	# channellist -flags -icon
	resp = ts3conn.query("channellist", "flags", "icon").fetch()
	resp = ts3conn.query("channellist").options("flags", "icon").all()
	resp = ts3conn.query("channellist").options("flags", "icon").first()

As a general rule of thumb, use *exec_()* if you don't need pipelining.

Examples
''''''''

You can find more examples in the ``ts3.examples`` package.

*	Show all clients on the virtual server with the server id 1:

	.. code-block:: python

		#!/usr/bin/python3

		import ts3

		with ts3.query.TS3ServerConnection("telnet://serveradmin:Z0YxRb7u@localhost:10011") as ts3conn:
			ts3conn.exec_("use", sid=1)

			# exec_() returns a **TS3QueryResponse** instance with the response.
			resp = ts3conn.exec_("clientlist")
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

		with ts3.query.TS3ServerConnection("telnet://serveradmin:Z0YxRb7u@localhost:10011") as ts3conn:
			ts3conn.exec_("use", sid=1)

			for client in ts3conn.exec_("clientlist"):
				msg = "Hi {}".format(client["client_nickname"])
				ts3conn.exec_("clientpoke", clid=client["clid"], msg=msg)

*	Event handling (*Server Query*):

	.. code-block:: python

		#!/usr/bin/python3

		import time
		import ts3

		with ts3.query.TS3ServerConnection("telnet://serveradmin:Z0YxRb7u@localhost:10011") as ts3conn:
			ts3conn.exec_("use", sid=1)

			# Register for events
			ts3conn.exec_("servernotifyregister", event="server")

			while True:
				ts3conn.send_keepalive()

				try:
					event = ts3conn.wait_for_event(timeout=60)
				except ts3.query.TS3TimeoutError:
					pass
				else:
					# Greet new clients.
					if event[0]["reasonid"] == "0":
						print("client connected")
						ts3conn.exec_("clientpoke", clid=event[0]["clid"], msg="Hello :)")

*	A simple TS3 viewer:

	.. code-block:: python

		#!/usr/bin/python3

		import ts3

		# The examples package already contains this implementation.
		# Note, that the examples.viewer module has an helpful class to
		# build a complete channel tree of a virtual server: ChannelTreeNode
		#
		# You may have to download it from GitHub first.
		from ts3_examples.viewer import view

		with ts3.query.TS3ServerConnection("telnet://serveradmin:Z0YxRb7u@localhost:10011") as ts3conn:
			view(ts3conn, sid=1)

*	Download and upload files:

	.. code-block:: python

		#!/usr/bin/python3

		import ts3

		with ts3.query.TS3ServerConnection("telnet://serveradmin:Z0YxRb7u@localhost:10011") as ts3conn:
			ts3conn.exec_("use", sid=1)

			# Create a new TS3FileTransfer instance associated with the
			# TS3ServerConnection.
			ts3ft = ts3.filetransfer.TS3FileTransfer(ts3conn)

			# Upload the image *baz.png* to the channel with the id 2 on the
			# TS3 server.
			# Note the opening mode ("rb").
			with open("baz.png", "rb") as file:
				ts3ft.init_upload(input_file=file, name="/baz.png", cid=2)

			# Download the file into *baz1.png*.
			with open("baz1.png", "wb") as file:
				ts3ft.init_download(output_file=file, name="/baz.png", cid=2)

*	Event handling (*Client Query*):

	.. code-block:: python

		#!/usr/bin/python3

		import time
		import ts3

		with ts3.query.TS3ServerConnection("telnet://localhost:25639") as ts3conn:
			ts3conn.exec_("auth", apikey="AAAA-....-EEEE")

			# Register for events
			ts3conn.exec_("clientnotifyregister", event="any", schandlerid=0)

			while True:
				event = ts3conn.wait_for_event()
				print(event.parsed)

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
