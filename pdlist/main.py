# -*- encoding: utf-8 -*-
# pdlist v0.1.0
# A passive sudomain lister
# Copyright © 2019, Giuseppe Nebbione.
# See /LICENSE for licensing information.

"""
Main routine of pdlist.

:Copyright: © 2019, gnc.
:License: BSD (see /LICENSE).
"""
import re
import argparse
import pdlist.source.crtsh as cr
import pdlist.source.urlscan as us
import pdlist.source.threatcrowd as tc
import pdlist.source.dnsdumpster as dd
import pdlist.source.certspotter as cs
import pdlist.source.hackertarget as ht
from pdlist.utils import (polish_subdomain_strings,
                          remove_unrelated_domains,
                          clean_domain_strings,
                          sort_domains)

__all__ = ('main',)


def show_banner():
    print("""
               _____      __
    ____  ____/ / (_)____/ /_
   / __ \/ __  / / / ___/ __/
  / /_/ / /_/ / / (__  ) /_
 / .___/\__,_/_/_/____/\__/
/_/

A passive domain sublister
Developed by gnc
    """)


def main():
    """Main routine of pdlist."""
    show_banner()
    parser = argparse.ArgumentParser(
        prog='pdlist', description='A passive subdomain enumerator')

    parser.add_argument(
        "domains",
        help="Specify the domain to enumerate",
        default=[],
        type=str,
        nargs='+',
    )
    parser.add_argument(
        "-s", "--strict",
        dest='is_strict',
        action='store_true',
        help="Enables strict mode, where only proper (and not also related)\
        subdomains will be saved",
        default=False,
    )
    parser.add_argument(
        "-o", "--output",
        dest='outputfile',
        help="Save results to the specified file",
        default=None,
        nargs='?',
        type=argparse.FileType(mode='wt',encoding='utf-8'),
    )

    args = parser.parse_args()
    subdomains = []
    domains = clean_domain_strings(args.domains)

    print(
        '\033[94m[*] \033[0m The analyzed domains will be: ' +
        ' '.join(domains))

    found_subdomains = []
    sources = [tc, ht, us, dd, cr, cs]
    for source in sources:
        name = re.sub(r' parser$', '', source.__doc__.strip().split('\n')[0])
        print('\033[32m[+] \033[0m Searching on {}...'.format(name))
        # Decomment here if you want to get the number of extracted
        # subdomains ...

        # found_subdomains += source.parse(domains)
        # print('\033[32m[+] \033[0m Found {} subdomains from {}'
        #         .format(len(found_subdomains), source))
        # subdomains += found_subdomains
        subdomains += source.parse(domains)

    print()
    print('\033[32m[+] \033[0m Printing domain list...')
    print()

    subdomains = polish_subdomain_strings(subdomains)

    if args.is_strict:
        subdomains = remove_unrelated_domains(subdomains, domains)
    
    # only get unique subdomains strings to avoid duplicates
    subdomains = list(set(subdomains))
    
    # sort subdomains
    subdomains = sort_domains(subdomains)

    print()

    if args.outputfile is not None:
        args.outputfile.write('\n'.join(subdomains))
    for subdomain in subdomains:
        print(subdomain)
