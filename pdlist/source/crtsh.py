# -*- encoding: utf-8 -*-
# dplist v0.1.0
# A passive sudomain lister
# Copyright © 2019, Giuseppe Nebbione.
# See /LICENSE for licensing information.

"""
crt.sh parser

:Copyright: © 2019, Giuseppe Nebbione.
:License: BSD (see /LICENSE).
"""
import requests
import json




def parse(domains):
    subdomains = []
    for d in domains:
        url = 'https://crt.sh/?q=%%25.{}&output=json'.format(d)
        json_resp = json.loads(requests.get(url).text)
        subdomains = [ e['name_value'] for e in json_resp ]
    return list(set(subdomains))


