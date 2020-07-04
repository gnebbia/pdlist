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
import sys
import json
import requests


def parse(domains):
    """
    This function performs a request to crt.sh and after having
    parsed its output returns a cleaned list of unique domains

    Args:
    domains -- the list of input domain to query

    Returns:
    a cleaned list of unique subdomains obtained after querying crt.sh
    """
    ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
    subdomains = []
    crt_namevalues = []
    for domain in domains:
        url = "https://crt.sh/?q={}&output=json".format(domain)
        req = requests.get(url, headers={'User-Agent':ua})
        if req.ok:
            try:
                json_resp = json.loads(req.content.decode('utf-8'))
                crt_namevalues = [e['name_value'] for e in json_resp]
                subdomains += [x for s in crt_namevalues for x in s.split()]
            except json.decoder.JSONDecodeError:
                print("ERROR: crt.sh response may be too long or badly formatted",
                        file=sys.stderr)
    return list(set(subdomains))
