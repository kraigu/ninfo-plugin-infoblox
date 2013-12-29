ninfo-plugin-infoblox
=====================

Infoblox (REST API) plugin for ninfo

Plugin Configuration
--------------------

```
[plugin:infoblox]
username = userid
hostname = InfobloxServerName
password = guesswhat
uqdomain = assume this for unqualified hostnames
```

uqdomain is not actually used yet. Once ninfo supports it, this configuration will change to point to a .infobloxrc file.
