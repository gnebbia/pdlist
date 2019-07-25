# -*- encoding: utf-8 -*-
    
# dplist v0.1.0
# A passive sudomain lister
# Copyright © 2019, Giuseppe Nebbione.
# See /LICENSE for licensing information.

"""
Threatcrowd parser

:Copyright: © 2019, Giuseppe Nebbione.
:License: BSD (see /LICENSE).
"""
import requests
import json
from dnsdumpster.DNSDumpsterAPI import DNSDumpsterAPI

def find(key, dictionary):
    if isinstance(dictionary,dict):
        for k, v in dictionary.items():
            if k == key:
                yield v
            elif isinstance(v, dict):
                for result in find(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in find(key, d):
                        yield result



def parse(domains):
    subdomains = []
    for d in domains:
        results = DNSDumpsterAPI().search(d)
        subdomains += list(set(find('domain', results['dns_records'])))
        subdomains += list(set(find('reverse_dns', results['dns_records'])))
    return subdomains


