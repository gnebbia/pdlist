#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# pdlist test suite
# Copyright © 2019, Giuseppe Nebbione.
# See /LICENSE for licensing information.


import pdlist
import pdlist.source.threatcrowd as tc
import pdlist.source.hackertarget as ht
import pdlist.source.dnsdumpster as dd
import pdlist.source.crtsh as cr
import pdlist.source.certspotter as cs
import pdlist.source.urlscan as us



def test_main():
    """Test adding source."""
    domain = 'localhost'
    subdomains = []

    print('[+] Searching on threatcrowd...')
    subdomains += tc.parse(['localhost'])
    print(subdomains)

    print('[+] Searching on hackertarget...')
    subdomains += ht.parse(['localhost'])
    print(subdomains)

    print('[+] Searching on dnsdumpster...')
    subdomains += dd.parse(['localhost'])
    print(subdomains)
    
    print('[+] Searching on cert.sh...')
    subdomains += cr.parse(['localhost'])
    print(subdomains)

    print('[+] Searching on certspotter...')
    subdomains += cs.parse(['localhost'])
    print(subdomains)


def test_import():
    """Test imports."""
    pdlist
    pdlist.source
