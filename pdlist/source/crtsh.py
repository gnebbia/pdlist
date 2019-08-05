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
    subdomains = []
    for domain in domains:
        url = 'https://crt.sh/?q=%%25.{}&output=json'.format(domain)
        json_resp = json.loads(requests.get(url).text)
        subdomains = [e['name_value'] for e in json_resp]
    return list(set(subdomains))
