gnippy: GNIP + Python
=====================

gnippy provides an easy way to access the `Power Track <http://gnip.com/twitter/power-track/>`_ stream provided by GNIP.

Installation:

.. code-block:: python

    pip install gnippy

Quickstart:

.. code-block:: python

    #!/usr/bin/env python

    import time
    from gnippy import PowerTrackClient

    # Define a callback
    def callback(activity):
        print activity

    # Create the client
    url = "http://my.gnip.powertrack/url.json"
    auth = ('MyUserName', 'MyPassword')
    client = PowerTrackClient(callback, url=url, auth=auth)
    client.connect()
    
    # Wait for 2 minutes and then disconnect
    time.sleep(120)
    client.disconnect()

If no credentials/url is/are provided, gnippy will look for a boto-style .gnippy file in the user's home directory.
The structure of a .gnippy file is as follows:

.. code-block:: text

    [Credentials]
    username = user@company.com
    password = mypassword

    [PowerTrack]
    url = https://my.gnip.powertrack/url.json

This file can be stored in an alternate location and be passed in as a parameter to the constructor.

.. code-block:: python

    client = PowerTrackClient(callback) # if you have a ~/.gnippy file ready to rock

    # OR

    client = PowerTrackClient(callback, config_file_path="/etc/.gnippy")


Source available on GitHub: http://github.com/abh1nav/gnippy/
