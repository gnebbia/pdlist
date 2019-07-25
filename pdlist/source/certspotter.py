# -*- encoding: utf-8 -*-
# dplist v0.1.0
# A passive sudomain lister
# Copyright © 2019, Giuseppe Nebbione.
# See /LICENSE for licensing information.

"""
certspotter parser

:Copyright: © 2019, Giuseppe Nebbione.
:License: BSD (see /LICENSE).
"""
import requests
import json




def parse(domains):
    subdomains = []
    for d in domains:
        url = 'https://certspotter.com/api/v0/certs?domain={}'.format(d)
        json_resp = json.loads(requests.get(url).text)
        doms = [ e['dns_names'] for e in json_resp ]
        for s in doms:
            subdomains += s
    return list(set(subdomains))


