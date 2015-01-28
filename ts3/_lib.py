#!/usr/bin/env python3

# The MIT License (MIT)
# 
# Copyright (c) 2013-2015 Benedikt Schmitt <benedikt@benediktschmitt.de>
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
This module contains some small helpers for the ts3 package, which are not part
of the API.
"""


# Modules
# ------------------------------------------------

# std
import queue
import threading


# Classes
# ------------------------------------------------

__all__ = [
    "SignalDispatcher"
    ]


# Classes
# ------------------------------------------------

class SignalDispatcher(object):
    """
    This is a simple worker thread which is dedicated to call *blinker* signals
    in a thread.

    .. code-block::

        >>> dispatcher = SignalDispatcher()
        >>>
        >>> # create a listener
        >>> my_func = lambda *sender, **kargs: print("my_func:", sender, kargs)
        >>>
        >>> blinker.signal("my_signal").connect(my_func)
        >>>
        >>> # start the dispatcher
        >>> dispatcher.start()
        >>>
        >>> # send a signal in another thread using the dispatcher
        >>> dispatcher.send(blinker.signal("my_signal"), None, a=1, b=2)
    """

    def __init__(self):
        """
        """
        self.__signal_queue = queue.Queue()

        # Some events which allow us to stop the thread.
        self.__stop_event = threading.Event()
        self.__waiting_for_stop = False

        # The thread which dispatches the events.
        self.__thread = None
        return None

    def is_running(self):
        """
        Returns ``True`` if the worker thread is running. Otherwise ``False``.
        """
        return self.__thread is not None

    def send(self, signal, *sender, **kwargs):
        """
        Puts the *signal* on the signal queue, so that it will be dispatched
        in the worker thread.

        .. code-block::

            >>> # Usual blinker call:
            >>> signal.send(*sender, **kwargs)
            ...
            >>> # Sending the signal using the signal dispatcher:
            >>> signal_dispatcher.send(signal, *sender, **kwargs)
            ...

        :raises RuntimeError:
            if the event dispatcher is not running.
        """
        if not self.is_running():
            raise RuntimeError("event dispatcher has not been started.")
        if self.__waiting_for_stop:
            raise RuntimeError("event dispatcher is about to stop.")
        
        self.__signal_queue.put((signal, sender, kwargs))
        return None

    def stop(self):
        """
        Stops the event dispatcher and blocks until the worker thread finished.
        """
        if self.is_running():
            # Signalize the worker thread to stop.
            self.__stop_event.clear()
            self.__waiting_for_stop = True
            self.__stop_event.wait()

            # Assert all signals have been processed.
            assert self.__signal_queue.empty()

            self.__thread = None
        return None

    def start(self):
        """
        Starts the event dispatcher.
        """
        if not self.is_running():
            self.__waiting_for_stop = False
            self.__thread = threading.Thread(target=self._run)
            self.__thread.start()
        return None

    def _run(self):
        """
        Waits for new signals to dispatch and dispatchs them until the stop
        flag is set.
        """
        # Run as long as there are unprocessed signals or the stop has not been
        # requested.
        while (not self.__waiting_for_stop) \
              or (not self.__signal_queue.empty()):
            try:
                signal, sender, kwargs = self.__signal_queue.get(
                    block = True,
                    timeout = 0.1
                    )
            except queue.Empty:
                continue
            else:
                signal.send(*sender, **kwargs)

        # Set the stop flag.
        self.__stop_event.set()
        return None
