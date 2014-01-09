# Py-TS3
This package implements an API for the **TeamSpeak 3 Server Query** and the
**TeamSpeak 3 File Transfer Interface**. 
It's developed and tested under **Python 3**.

## Installation

### Distutils
The master branch is a valid *distutils* package. So simply download and install
it:

1.	[Download](https://github.com/benediktschmitt/emsm/archive/master.zip) the
    master branch.
	
2.	Go to the download location and run the *setup.py* script:

	```Shell
	$ setup.py install
	```
	
### As portable library
You can simply download the master branch and copy the *ts3* directory in
your projects folder or wherever you need it.

**Note,** that importing the **examples** package might fail.

## Quick Introduction
The easiest way to get to grips with this library is taking a look at the
*examples*.
If you need information about the possible query commands, take a look at the 
*TS3 Server Query Manual*.

### Examples
1. Show all clients on the virtual server 1:

	```Python
	#!/usr/bin/python3

	import ts3

	with ts3.TS3Connection("localhost") as ts3conn:
		# Note, that the client will wait for your responses and raise a
		# **TS3QueryException** if the error id of the response is not 0.
		# 
		# You can use the *quiet_mode* flag to avoid such exceptions by the 
		# client.
		# >>> ts3conn.quiet_mode = True
		# 
		# If you don't want or need to wait for the response of the server,
		# you can set the *patient_mode* flag to false. Note, that the client
		# will still wait for the responses if *quiet_mode* is true.
		# >>> ts3conn.patient_mode = False
		ts3conn.login("serveradmin", "FoOBa9")
		ts3conn.use(1)
		ts3conn.clientlist()
		
		# One last important thing: The parser will parse the response the first
		# time you use *resp.parsed*. If the response could not be parsed,
		# *resp.parsed* is None.
		resp = ts3conn.last_resp
		for client in resp.parsed:
			print(client["cid"], client["client_nickname"])	
	```

2. Greet every client:

	```Python
	#!/usr/bin/python3

	import ts3

	with ts3.TS3Connection("localhost") as ts3conn:
		ts3conn.login("serveradmin", "FoOBa9")
		ts3conn.use(1)
		ts3conn.clientlist()
		
		resp = ts3conn.last_resp
		for client in resp.parsed:
			msg = "Hi {}".format(client["client_nickname"])
			ts3conn.clientpoke(clid=client["clid"], msg=msg)
	```
	
3. A simple TS3 viewer:

	```Python
	#!/usr/bin/python3
	
	import ts3
	
	# The examples package already contains this implementation. 
	# Note, that the ts3.examples.viewer module has an helpful class to build 
	# channel tree of a virtual server: *ChannelTreeNode*.
	from ts3.examples.viewer import view
	
	with ts3.TS3Connection("localhost") as ts3conn:
		ts3conn.login("serveradmin", "FoOBa9")
		view(ts3conn, sid=1)
	```
	
More examples are in the **examples package** (```import ts3.examples```).

## Bugs
This project is in an early state, so you'll probably find a bug. Please report
it. 

If you found a grammar or spelling error, please report it too.

## Versioning
For the version numbers, take a look at http://semver.org/.

## License
This package is licensed under the **MIT License**. 
