===============
GNIP for Python
===============

GNIP for Python provides an easy way to access the PowerTrack stream provided by GNIP.

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