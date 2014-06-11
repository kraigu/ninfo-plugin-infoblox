DNS name: ${dns_name}
IPv4 addresses: ${ipv4addrs}
Some Extensible Attributes:
% if 'Technical Contact' in extattrs:
Technical Contact: ${extattrs['Technical Contact']['value']}
% endif
% if 'Business Contact' in extattrs:
Business Contact: ${extattrs['Business Contact']['value']}
% endif
% if 'Pol8 Classification' in extattrs:
Policy 8 Classification: ${extattrs['Pol8 Classification']['value']}
% endif
% if 'Legacy-AdminID' in extattrs:
Legacy Admin: ${extattrs['Legacy-AdminID']['value']}
% endif
% if 'Legacy-ContactID' in extattrs:
Legacy Contact: ${extattrs['Legacy-ContactID']['value']}
% endif
