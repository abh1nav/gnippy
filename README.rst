gnippy: Python library for GNIP
===============================

.. image:: https://badge.fury.io/py/gnippy.svg
    :target: https://pypi.python.org/pypi/gnippy

.. image:: https://img.shields.io/pypi/dm/gnippy.svg
    :target: https://pypi.python.org/pypi/gnippy

.. image:: https://travis-ci.org/abh1nav/gnippy.svg?branch=master
    :target: https://travis-ci.org/abh1nav/gnippy

gnippy provides an easy way to access the `Power Track <http://gnip.com/twitter/power-track/>`_ stream provided by GNIP.
You can also use gnippy to programatically add rules to your Power Track stream.

Install
-------
.. code-block:: python

    pip install gnippy

Quickstart
----------
Create a .gnippy file and place it in your home directory. It should contain the following:

.. code-block:: text

    [Credentials]
    username = user@company.com
    password = mypassword

    [PowerTrack]
    url = https://my.gnip.powertrack/url.json
    rules_url = https://api.gnip.powertrack/rules.json

Fire up the client:

.. code-block:: python

    #!/usr/bin/env python
    import time
    from gnippy import PowerTrackClient

    # Define a callback
    def callback(activity):
        print activity

    # Create the client
    client = PowerTrackClient(callback)
    client.connect()
    
    # Wait for 2 minutes and then disconnect
    time.sleep(120)
    client.disconnect()

Configuration
-------------

If you don't want to create a config file or you want it put it in another location:

.. code-block:: python

    client = PowerTrackClient(callback, config_file_path="/etc/gnippy")
    # OR ... provide the url and authentication credentials to override any config files
    client = PowerTrackClient(callback, url="http://my.gnip.powertrack/url.json", auth=("uname", "pwd"))

You can also configure gnippy using environment variables:

.. code-block:: text

    GNIPPY_URL
    GNIPPY_RULES_URL
    GNIPPY_AUTH_USERNAME
    GNIPPY_AUTH_PASSWORD





Adding PowerTrack Rules
-----------------------

If you want to add `rules <http://support.gnip.com/apis/powertrack/rules.html>`_ to your PowerTrack:

.. code-block:: python

    from gnippy import rules
    from gnippy.errors import RuleAddFailedException

    # Synchronously add rules
    try:
        rules.add_rule('(Hello OR World OR "this is a test") lang:en', tag="MyRule")
        rules.add_rule('Rule without a tag')
    except RuleAddFailedException:
        pass

    # OR ... synchronously add multiple rules at once
    rule_list = []
    rule_list.append(rules.build("Hello World", tag="asdf"))
    rule_list.append(rules.build("Rule Without a Tag"))
    try:
        rules.add_rules(rule_list)
    except RuleAddFailedException:
        pass

    # OR ... manually pass in params - overrides any config files
    rules.add_rule("My Rule String", tag="mytag", rules_url="https://api.gnip.powertrack/rules.json", \
                   auth=("uname", "pwd"))


Listing Active PowerTrack Rules
-------------------------------

.. code-block:: python

  from gnippy import rules
  from gnippy.errors import RulesGetFailedException

  try:
      rules_list = rules.get_rules()
      # rules_list is in the format:
      # [
      #    { "value": "(Hello OR World) AND lang:en" },
      #    { "value": "Hello", "tag": "mytag" }
      # ]
  except RulesGetFailedException:
      pass

Deleting PowerTrack Rules
-------------------------

.. code-block:: python

    from gnippy import rules
    from gnippy.errors import RuleDeleteFailedException, RulesGetFailedException

    try:
        rules_list = rules.get_rules()
        # Suppose I want to delete the first rule in the list
        rules.delete_rule(rules_list[0])
        # OR ... I want to delete ALL rules
        rules.delete_rules(rules_list)

    except RuleDeleteFailedException, RulesGetFailedException:
        pass

Source available on GitHub: http://github.com/abh1nav/gnippy/
