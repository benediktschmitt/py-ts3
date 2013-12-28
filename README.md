# Py-TS3

**>>> This package is in an early state and not ready for productive use!<<<**

This package implements an API for the **TeamSpeak 3 Server Query** and the
**TeamSpeak 3 File Transfer Interface**. 
It's developed and tested under **Python 3**.

## Installation

1.	The master branch contains also the Python distutils package. So
	[download](https://github.com/benediktschmitt/emsm/archive/master.zip) it.
	
2.	Go to the download location and run the *setup.py* script:

	```Shell
	$ setup.py install
	```

## Examples
1. Show clients:

	```Python
	#!/usr/bin/python3

	from ts3 import query

	with query.TS3Connection("localhost") as ts3conn:
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

2. Kick all clients from the server:

	```Python
	#!/usr/bin/python3

	from ts3 import query

	with query.TS3Connection("localhost") as ts3conn:
		ts3conn.login("serveradmin", "FoOBa9")
		ts3conn.use(1)
		ts3conn.clientlist()
		
		resp = ts3conn.last_resp
		for client in resp.parsed:
			ts3conn.clientkick(clid=client["clid"], reasonid=5)
	```
	
You can find more examples in the **examples** directory.

## Bugs
This project is in an early state, so you'll probably find a bug. Please report
it.

## Versioning
For the version numbers, take a look at http://semver.org/.

## License
This package itself is licensed under the **MIT License**.