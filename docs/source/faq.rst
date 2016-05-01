.. _faq:

Frequently Asked Questions (FAQ)
================================

If you need help or you think you found a bug, please take also a look at the
`GitHub issue page <https://github.com/benediktschmitt/py-ts3/issues>`_. If
you did not found a solution for your problem, do not hesitate to open a new
issue with the corresponding label (e.g. ``help wanted``, ``bug``, ...).

Please take also a look at :ref:`contribute`.

Unexpected disconnects
----------------------

anti-flood
~~~~~~~~~~

Check the **anti-flood** settings of your TS3 server. Per default, the server
limits the number of queries a host can send per minute. Take a look at the
TS3 query manual to get to know how you can increase this limit or simply add
the host, you are running the Python script from, to the query whitelist of
your TS3 server:

.. code-block:: bash

   $ # In your TS3 server folder:
   $ echo "192.168.178.42" >> query_ip_whitelist.txt

max-idle-time
~~~~~~~~~~~~~

The ts3 server closes idle connections after 10 minutes automatically. You can
use the :meth:`~query.TS3BaseConnection.send_keepalive` to sent an empty query
to the server and thus avoid automatic disconnect. Make sure to call it at least
once in 10 minutes.
