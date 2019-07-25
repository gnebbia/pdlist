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




def parse(domains):
    subdomains = []
    for d in domains:
        url = 'https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={}'.format(d)
        resp = requests.get(url)
        subdomains += (json.loads(resp.text)['subdomains'])
    return subdomains


