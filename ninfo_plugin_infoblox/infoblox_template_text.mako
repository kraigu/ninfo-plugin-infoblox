DNS name: ${dns_name}
IPv4 addresses: ${ipv4addrs}
Some Extensible Attributes:
% if len(extattrs['Technical Contact']) > 1:
    % for kk in extattrs['Technical Contact']['value']:
Technical Contact ${loop.index}: ${kk}
    % endfor
% else:
Technical Contact: ${extattrs['Technical Contact']['value']}
% endif
% if len(extattrs['Business Contact']) > 1:
    % for kk in extattrs['Business Contact']['value']:
Business Contact ${loop.index}: ${kk}
    % endfor
% else:
Business Contact: ${extattrs['Business Contact']['value']}
% endif
Policy 8 Classification: ${extattrs['Pol8 Classification']['value']}
