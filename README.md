ninfo-plugin-infoblox
=====================

Infoblox (using the REST API) plugin for ninfo.

See: https://github.com/JustinAzoff/ninfo

Plugin Configuration
--------------------

```
[general]
local_networks = 10.0.0.0/8,172.16.0.0/12

[plugin:infoblox]
username = userid
hostname = InfobloxServerName
password = guesswhat
```

Without local_networks defined, you will not be able to look up hosts by IP address.

Once it's supported, this configuration will change to point to a .infobloxrc file rather than embedding credentials directly in the main configuration file.

There is currently no IPv6 support, and due to some bugs somewhere (sorry, see issues) the plugin may bomb out unexpectedly when retrieving information on a host with v6 addresses assigned.
