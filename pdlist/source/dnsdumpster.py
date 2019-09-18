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
from pdlist.utils import find
from dnsdumpster.DNSDumpsterAPI import DNSDumpsterAPI


def parse(domains):
    """
    This function performs a request to dnsdumpster and after having
    parsed its output returns a cleaned list of unique domains

    Args:
    domains -- the list of input domain to query

    Returns:
    a cleaned list of unique subdomains obtained after querying dnsdumpster
    """
    subdomains = []
    for domain in domains:
        results = DNSDumpsterAPI().search(domain)
        if not results: continue
        subdomains += list(set(find('domain', results['dns_records'])))
        subdomains += list(set(find('reverse_dns', results['dns_records'])))
    return subdomains
