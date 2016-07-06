from ninfo import PluginBase
from ninfo import util
import infoblox
import warnings
import socket
import requests
from requests.packages.urllib3.exceptions import InsecurePlatformWarning

class infoblox_plug(PluginBase):
    """This plugin looks up the argument on an Infoblox server"""

    name =         'infoblox'
    title =        'Infoblox'
    description =  'Retrieve information from Infoblox'
    cache_timeout =   60*60
    types = ['ip', 'hostname']
    #remote = False
    #local = True

    def setup(self):
        self.api = infoblox.Infoblox(self.plugin_config['hostname'],self.plugin_config['username'],self.plugin_config['password'], '1.6', '', 'default')

    def format_out(self, host, extattrs):
        # This code appears to work well, assuming that the extattrs thing exists. 
        # TO DO: I need to check what happens if I ask for extattrs for something that doesn't have any.
        o = {}
        o['_ref'] = host['_ref']
        if (o['_ref'] == None):
            return o
        if 'Pol8 Classification' in extattrs:
            o['classification'] = extattrs['Pol8 Classification']
        else:
            o['classification'] = 'NA'
        if 'Business Contact' in extattrs:
            o['businesscontact'] = extattrs['Business Contact']
        elif 'LEGACY-AdminID' in extattrs:
            o['businesscontact'] = extattrs['LEGACY-AdminID']
        else:
            o['businesscontact'] = 'NA'

        if 'Technical Contact' in extattrs:
            o['technicalcontact'] = extattrs['Technical Contact']
        elif 'LEGACY-ContactID' in extattrs:
            o['technicalcontact'] = extattrs['LEGACY-ContactID']
        else:
            o['technicalcontact'] = 'NA'

        # convert into comma delimited list of contacts, rather than a unicode list.
        o['technicalcontact'] = self.list_to_csv(o['technicalcontact'])
        o['businesscontact'] = self.list_to_csv(o['businesscontact'])

        return o

    def list_to_csv(self, thelist):
        # first checking to see if it's actually a list
        if isinstance(thelist, list):
            s = ''
            for i in thelist:
                s = s + i + ','
            return s[0:-1] #stripping last comma
        else:
            return thelist

    def get_info(self, arg):
        with warnings.catch_warnings():
            # catching the super annoying warnings regarding insecure connections.
            warnings.filterwarnings("ignore", ".*Unverified.*")
            argtype = util.get_type(arg)

            if argtype == 'hostname':
                # If we have a hostname, it might be a CNAME, so naively try resolving it.
                # CNAMEs aren't host records according to Infoblox, so just searching
                # for the CNAME will return nothing. If we do hostname -> IP and back again,
                # that should work.
                try:
                    hname = socket.gethostbyaddr(socket.gethostbyname(arg))[0]
                    host = self.api.get_host(hname)
                    extattrs = self.api.get_host_extattrs(hname)
                except:
                    # Something's gone really wrong
                    return {'_ref': None }
            elif argtype == 'ip':
                try:
                    res = socket.gethostbyaddr(ipaddr)
                    return self.get_info(res[0])
                except:
                    pass
                    try:
                        hostname = self.api.get_host_by_ip(arg)[0]
                        return self.get_info(hostname)
                    except:
                        return {'_ref' : None }

            out = self.format_out(host, extattrs)

            if (out['_ref'] == None):
                return out
            out['type'] = 'hostname'
            out['dns_name'] = host['ipv4addrs'][0]['host']
            out['ipv4addr'] = host['ipv4addrs'][0]['ipv4addr']
        return out

plugin_class = infoblox_plug
