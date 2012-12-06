gnippy: GNIP + Python
=====================

gnippy provides an easy way to access the `Power Track <http://gnip.com/twitter/power-track/>`_ stream provided by GNIP.

Installation:

.. code-block:: pycon

    pip install gnippy

Usage:

.. code-block:: pycon

    #!/usr/bin/env python

    import time
    from gnippy import PowerTrackClient

    # Define a callback
    def callback(activity):
        print activity

    # Create the client
    url = "http://my.gnip.powertrack/url.json"
    auth = ('MyUserName', 'MyPassword')
    client = PowerTrackClient(url, auth, callback)
    client.connect()
    
    # Wait for 2 minutes and then disconnect
    time.sleep(120)
    client.disconnect()

That's it!

Source available on GitHub: http://github.com/abh1nav/gnippy/
