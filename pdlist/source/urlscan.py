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
import json
import requests
from pdlist.utils import find


def parse(domains):
    """
    This function performs a request to urlscan and after having
    parsed its output returns a cleaned list of unique domains

    Args:
    domains -- the list of input domain to query

    Returns:
    a cleaned list of unique subdomains obtained after querying urlscan
    """
    subdomains = []
    for domain in domains:
        url = 'https://urlscan.io/api/v1/search/?q=domain:{}'.format(domain)
        json_resp = json.loads(requests.get(url).text)
        subdomains += list(set(find('domain', json_resp)))
    return list(set(subdomains))
