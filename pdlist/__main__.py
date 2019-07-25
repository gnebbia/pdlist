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
import argparse
import pdlist.source.threatcrowd as tc
import pdlist.source.hackertarget as ht
import pdlist.source.dnsdumpster as dd
import pdlist.source.crtsh as cr
import pdlist.source.certspotter as cs
import pdlist.source.urlscan as us


__all__ = ('main',)


def main(args):
    """Main routine of pdlist."""
    subdomains = []
    domains = args.domains

    print('\033[94m[*] \033[0m The analyzed domains will be: '+ ' '.join(domains))

    print('\033[32m[+] \033[0m Searching on threatcrowd...')
    subdomains += tc.parse(domains)

    print('\033[32m[+] \033[0m Searching on hackertarget...')
    subdomains += ht.parse(domains)

    print('\033[32m[+] \033[0m Searching on dnsdumpster...')
    subdomains += dd.parse(domains)
    
    print('\033[32m[+] \033[0m Searching on crt.sh...')
    subdomains += cr.parse(domains)

    print('\033[32m[+] \033[0m Searching on certspotter...')
    subdomains += cs.parse(domains)

    print('\033[32m[+] \033[0m Printing domain list')
    print()
    
    if args.outputfile is not None:
        args.outputfile.write('\n'.join(list(set(subdomains))))
    for x in list(set(subdomains)):
        print(x)


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


if __name__ == '__main__':
    show_banner()
    parser = argparse.ArgumentParser(prog='pdlist',
                                     description='A passive subdomain enumerator')

    parser.add_argument(
        "domains",
        help="Specify the domain to enumerate",
        default=[],
        type=str,
        nargs='+',
        )
    parser.add_argument(
        "-o","--output",
        dest='outputfile',
        help="Save results to standard output",
        default=None,
        nargs='?',
        type=argparse.FileType('w'),
        )


    args = parser.parse_args()

    main(args)
