# -*- encoding: utf-8 -*-
# dplist v0.1.0
# A passive sudomain lister
# Copyright © 2019, Giuseppe Nebbione.
# See /LICENSE for licensing information.

"""
UrlScan parser

:Copyright: © 2019, Giuseppe Nebbione.
:License: BSD (see /LICENSE).
"""
import requests
import json


def find(key, dictionary):
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
        url = 'https://urlscan.io/api/v1/search/?q=domain:{}'.format(d)
        json_resp = json.loads(requests.get(url).text)
        subdomains += list(set(find('domain', json_resp)))
    return list(set(subdomains))


