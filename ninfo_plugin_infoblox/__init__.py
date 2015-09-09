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
        ibpass = self.plugin_config['password']
        ibuser = self.plugin_config['username']
        ibhost = self.plugin_config['hostname']
        self.session = infoblox.Session(ibhost,ibuser,ibpass)

    def format_out(self, thehost):
	thehost.fetch()
	thedict = thehost.__dict__

	# final output dictionary is placed in the o variable
	o = {}
	o['_ref'] = thedict['_ref']
	if (o['_ref'] == None):
	    return o
	print thedict	
        if 'extattrs' in thedict:
		extattrs = thedict['extattrs']
		if 'Pol8 Classification' in extattrs:
	            o['classification'] = extattrs['Pol8 Classification']['value']
		else:
		    o['classification'] = 'NA'
		if 'Business Contact' in extattrs:
	            o['businesscontact'] = extattrs['Business Contact']['value']
		elif 'LEGACY-AdminID' in extattrs:
		    o['businesscontact'] = extattrs['LEGACY-AdminID']['value']
		else:
		    o['businesscontact'] = 'NA'

		if 'Technical Contact' in extattrs:
	            o['technicalcontact'] = extattrs['Technical Contact']['value']
		elif 'LEGACY-ContactID' in extattrs:
		    o['technicalcontact'] = extattrs['LEGACY-ContactID']['value']
		else:
		    o['technicalcontact'] = 'NA'
        else:
            o['classification'] = 'NA'
            o['businesscontact'] = 'NA'
            o['technicalcontact'] = 'NA'
	return o

    def get_info(self, arg):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", ".*Unverified.*")
            argtype = util.get_type(arg)
            if argtype == 'hostname':
            	host = infoblox.Host(self.session,name=arg)
            elif argtype == 'ip':
		# attempting to resolve the hostname, since stuff is better tracked that way.
		try:
		    res = socket.gethostbyaddr(arg)
		    return self.get_info(res[0])
		except:
                    host = infoblox.HostIPv4(self.session,ipv4addr=arg)
	    out = self.format_out(host)
	    if (out['_ref'] == None):
		return out
	    hdict = host.__dict__
	    if argtype == 'hostname':
		out['type'] = 'hostname'
		out['dns_name'] = hdict['dns_name']
		out['ipv4addr'] = hdict['ipv4addrs'][0]['ipv4addr']
	    elif argtype == 'ip':
	    # TO DO: QUERY FOR THE HOSTNAME AND THEN PROCESS LIKE THIS IF IT DOESN'T WORK
		out['type'] = 'ip'
                out['dns_name'] = hdict['host']
                out['ipv4addr'] = hdict['ipv4addr']
	    else:
	        print "infoblox plugin goes argh"
	return out

plugin_class = infoblox_plug

