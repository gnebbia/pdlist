# -*- encoding: utf-8 -*-
# dplist v0.1.0
# A passive sudomain lister
# Copyright © 2019, Giuseppe Nebbione.
# See /LICENSE for licensing information.

"""
utils functions for pdlist

:Copyright: © 2019, Giuseppe Nebbione.
:License: BSD (see /LICENSE).
"""
import re


def remove_unrelated_domains(subdomains, domains):
    subdomains = [s for s in subdomains if s.endswith(tuple(domains))]
    return subdomains
    

def polish_subdomain_strings(subdomains):
    subdomains = [item.strip() for item in subdomains]
    subdomains = [item.rstrip('\.') for item in subdomains]
    subdomains = [re.sub("^.* ", "", item) for item in subdomains]
    subdomains = [re.sub("^[\.\*]\.", "", item) for item in subdomains]
    return subdomains

def find(key, dictionary):
    if isinstance(dictionary, dict):
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

def clean_domain_strings(domains):
    domains = [item.rstrip('\/') for item in domains]
    domains = [re.sub("(http://|https://)", "", item) for item in domains]
    return domains
