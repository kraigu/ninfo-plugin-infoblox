from ninfo import PluginBase
from ninfo import util
import infoblox

class infoblox_plug(PluginBase):
    """This plugin looks up the argument on an Infoblox server"""

    name =         'infoblox'
    title =        'Infoblox'
    description =  'Retrieve information from Infoblox'
    cache_timeout =   60*60
    types = ['hostname', 'ip']
    remote = False
    local = True

    def setup(self):
        ibpass = self.plugin_config['password']
        ibuser = self.plugin_config['username']
        ibhost = self.plugin_config['hostname']
        self.session = infoblox.Session(ibhost,ibuser,ibpass)

    def get_info(self, arg):
        argtype = util.get_type(arg)
        print "infoblox plugin type was " + argtype
        if argtype == 'hostname':
            host = infoblox.Host(self.session,name=arg)
        elif argtype == 'ip':
            host = infoblox.HostIPv4(self.session,ipv4addr=arg)
        elif argtype == 'ip6':
            host = infoblox.HostIPv6(self.session,ipv6addr=arg)
        else:
            print "infoblox plugin goes argh"
        host.fetch()
        return host.__dict__

plugin_class = infoblox_plug
