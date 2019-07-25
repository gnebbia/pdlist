# -*- encoding: utf-8 -*-
    
# dplist v0.1.0
# A passive sudomain lister
# Copyright © 2019, Giuseppe Nebbione.
# See /LICENSE for licensing information.

"""
DnsDumpster parser

:Copyright: © 2019, Giuseppe Nebbione.
:License: BSD (see /LICENSE).
"""
import requests
import json
from pdlist.utils import find
from dnsdumpster.DNSDumpsterAPI import DNSDumpsterAPI



def parse(domains):
    subdomains = []
    for d in domains:
        results = DNSDumpsterAPI().search(d)
        subdomains += list(set(find('domain', results['dns_records'])))
        subdomains += list(set(find('reverse_dns', results['dns_records'])))
    return subdomains


