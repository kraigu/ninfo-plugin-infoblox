from ninfo import PluginBase
import infoblox

class infoblox_plug(PluginBase):
    """This plugin looks up the argument on an Infoblox server"""

    name =         'infoblox'
    title =        'Infoblox'
    description =  'Retrieve information from Infoblox'
    cache_timeout =   60*60
    types =     ['hostname']
    remote =     False

    def setup(self):
        ibpass = self.plugin_config['password']
        ibuser = self.plugin_config['username']
        ibhost = self.plugin_config['hostname']
        ibuqd = self.plugin_config['uqdomain']
        self.session = infoblox.Session(ibhost,ibuser,ibpass)

    def get_info(self, arg):
        host = infoblox.Host(self.session,name=arg)
        host.fetch()
        return { 'items': host.items}

 plugin_class = infoblox_plug
