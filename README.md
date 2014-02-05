# PyTS3
This package provides a *thread-safe* **Python 3 API** for:

* TS3 query connections
* TS3 query events
* TS3 file transfers

You can find a complete API documentation 
[here](http://benediktschmitt.de/docs/pyts3).


## Reference
* [Installation](#installation)
* [Introduction](#introduction)
* [Bugs](#bugs)
* [Versioning](#versioning)
* [License](#license)


## Installation

1.	[Download](https://github.com/benediktschmitt/emsm/archive/master.zip) the
	master branch.
	
2.	You can either install the package with *distutils*
	
	```Shell
	$ setup.py install
	```
	
	or you copy the *ts3* directory into your application's include path:
	
	```Shell
	$ cp -r ts3/ /foo/bar/my_lib/
	```
	
	If you choose the portable installation mode, you may not be able to import
	the *examples* sub-package.


## Introduction
The easiest way to get to grips with this library is taking a look at the
[examples](ts3/examples/).

If you need information about the possible query commands, take a look at the 
**TS3 Server Query Manual**.


### Examples
You can find more examples in the [examples directory](ts3/examples).

*	Show all clients on the virtual server with the server id 1:

	```Python
	#!/usr/bin/python3

	import ts3

	with ts3.query.TS3Connection("localhost") as ts3conn:
		# Note, that the client will wait for the response and raise a
		# **TS3QueryError** if the error id of the response is not 0.
		try:
			ts3conn.login(client_login_name="serveradmin", 
			              client_login_password="FoOBa9")
		except ts3.query.TS3QueryError as err:
			print("Login failed:", err.resp.error["msg"])
			exit(1)
		
		ts3conn.use(1)
		
		# Each query method will return a **TS3QueryResponse** instance,
		# with the response.
		resp = ts3conn.clientlist()
		print("Clients on the server:", resp.parsed)
		print("Error:", resp.error["id"], resp.error["msg"])
		
		# Note, the TS3Response class and therefore the TS3QueryResponse class
		# too, can work as a rudimentary container. So, these two commands are
		# equal:
		for client in resp.parsed:
			print(client)
		for client in resp:
			print(client)
	```

*	Say hello to all clients:

	```Python
	#!/usr/bin/python3

	import ts3

	with ts3.query.TS3Connection("localhost") as ts3conn:
		ts3conn.login(client_login_name="serveradmin", 
		              client_login_password="FoOBa9")
		ts3conn.use(sid=1)
		
		for client in ts3conn.clientlist():
			msg = "Hi {}".format(client["client_nickname"])
			ts3conn.clientpoke(client["clid"], msg)
	```
	
*	Event handling:

	```Python
	#!/usr/bin/python3

	import time
	import ts3
	
	def my_event_handler(ts3conn, event):
		"""
		*event* is a ts3.response.TS3Event instance, that contains the name of the
        event and the data.
		"""
		print("Event:")
		print("\t", event.event)
		print("\t", event.parsed)
		return None
	
	with ts3.query.TS3Connection("localhost") as ts3conn:
		ts3conn.login(client_login_name="serveradmin", 
		              client_login_password="FoOBa9")
		ts3conn.use(sid=1)
		
		# Replace the default handler
		ts3conn.on_event = my_event_handler
		
		# Register for events
		ts3conn.servernotifyregister(event="server")
		
		# Start the recv loop to catch all events.
		ts3conn.recv_in_thread()
      
        # Note, that you can still use the ts3conn to send queries:
        ts3conn.clientlist()
		
		# The recv thread can be stopped with:
		# >>> ts3conn.stop_recv()
		# Note, that the thread will be stopped automatically when the client
		# disconnects.
		
		# Block to avoid leaving the *with* statement and therefore closing the
		# connection.
		input("> Hit enter to finish.")
	```
	
*	A simple TS3 viewer:

	```Python
	#!/usr/bin/python3
	
	import ts3
	
	# The examples package already contains this implementation. 
	# Note, that the ts3.examples.viewer module has an helpful class to build 
	# a complete channel tree of a virtual server: ChannelTreeNode
	from ts3.examples.viewer import view
	
	with ts3.query.TS3Connection("localhost") as ts3conn:
		ts3conn.login(client_login_name="serveradmin",
					  client_login_password="FoOBa9")
		view(ts3conn, sid=1)
	```
	
*	Download and upload files:

	```Python
	#!/usr/bin/python3
	
	import ts3
	
	with ts3.query.TS3Connection("localhost") as ts3conn:
		ts3conn.login(client_login_name="serveradmin",
					  client_login_password="FoOBa9")
		view(ts3conn, sid=1)
		
		# Create a new TS3FileTransfer instance associated with the
		# TS3Connection.
		ts3ft = ts3.filetransfer.TS3FileTransfer(ts3conn)
		
		# Upload the image *baz.png* to the channel with the id 2 on the
		# TS3 server.
		# Note, the the opening mode ("rb").
		with open("baz.png", "rb") as file:
			ts3ft.init_upload(input_file=file, name="/baz.png", cid=2)
		
		# Download the file into *baz1.png*.
		with open("baz1.png", "wb") as file:
			ts3ft.init_download(output_file=file, name="/baz.png", cid=2)
	```

	
## Bugs
This project is in an early state, so you'll probably find a bug. Please report
it or fork this repo, fix the bug and create a pull request. 

If you found a grammar or spelling error, please report it too.


## Versioning
For the version numbers, take a look at http://semver.org/.


## License
This package is licensed under the [MIT License](LICENSE). 

The docstrings copied from the TS3 Server Query Manual are the property of the
[TeamSpeak Systems GmbH](http://www.teamspeak.com/).