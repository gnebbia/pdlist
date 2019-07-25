# -*- encoding: utf-8 -*-
# dplist v0.1.0
# A passive sudomain lister
# Copyright © 2019, Giuseppe Nebbione.
# See /LICENSE for licensing information.

"""
Hackertarget parser

:Copyright: © 2019, Giuseppe Nebbione.
:License: BSD (see /LICENSE).
"""
import requests
import json


def parse(domains):
    subdomains = []
    for d in domains:
        url = 'https://api.hackertarget.com/hostsearch/?q={}'.format(d)
        resp = requests.get(url)
        lines = resp.text.split()
        for l in lines:
            subdomains.append(l.split(',')[0])
    return subdomains
