# Py-TS3
This package implements an API for the **TeamSpeak 3 Server Query** and the
**TeamSpeak 3 File Transfer Interface**. 
It's developed and tested under **Python 3**.

## Installation
The master branch is a valid *distutils* package. So simply download and install
it:

1.	[Download](https://github.com/benediktschmitt/emsm/archive/master.zip) the
    master branch.
	
2.	Go to the download location and run the *setup.py* script:

	```Shell
	$ setup.py install
	```

## Quick Introduction
The easiest way to get to grips with this library is taking a look at the
*examples*.
If you need information about the possible query commands, take a look at the 
*TS3 Server Query Manual*.

### Examples
1. Show all clients on the virtual server 1:

	```Python
	#!/usr/bin/python3

	from ts3.query import TS3Connection

	with TS3Connection("localhost") as ts3conn:
		# Note, that the client will not wait for the response, unless you
		# set the response flag *ts3conn.wait_for_resp = True* or you call
		# *ts3conn.last_resp* after each command.
		ts3conn.login("serveradmin", "FoOBa9")
		ts3conn.use(1)
		ts3conn.clientlist()
		
		# Now, we need the response:
		resp = ts3conn.last_resp
		for client in resp.parsed:
			print(client["cid"], client["client_nickname"])	
	```

2. Greet every client:

	```Python
	#!/usr/bin/python3

	from ts3 import query

	with query.TS3Connection("localhost") as ts3conn:
		ts3conn.login("serveradmin", "FoOBa9")
		ts3conn.use(1)
		ts3conn.clientlist()
		
		resp = ts3conn.last_resp
		for client in resp.parsed:
			msg = "Hi {}".format(client["client_nickname"])
			ts3conn.clientpoke(clid=client["clid"], msg=msg)
	```
	
More examples are in the **examples directory**.

## Bugs
This project is in an early state, so you'll probably find a bug. Please report
it. 

If you found a grammar or spelling error, please report it too.

## Versioning
For the version numbers, take a look at http://semver.org/.

## License
This package is licensed under the **MIT License**. 
