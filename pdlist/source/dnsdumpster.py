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
import re
import requests
from pdlist.utils import find
from bs4 import BeautifulSoup



def retrieve_results(table):
    """
    Function copied from DNSDumpster API to cancel
    errors related to index list out of range
    """

    res = []
    trs = table.findAll('tr')
    for tr in trs:
        tds = tr.findAll('td')
        pattern_ip = r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})'
        try:
            ip = re.findall(pattern_ip, tds[1].text)[0]
            domain = str(tds[0]).split('<br/>')[0].split('>')[1]
            header = ' '.join(tds[0].text.replace('\n', '').split(' ')[1:])
            reverse_dns = tds[1].find('span', attrs={}).text

            additional_info = tds[2].text
            country = tds[2].find('span', attrs={}).text
            autonomous_system = additional_info.split(' ')[0]
            provider = ' '.join(additional_info.split(' ')[1:])
            provider = provider.replace(country, '')
            data = {'domain': domain,
                    'ip': ip,
                    'reverse_dns': reverse_dns,
                    'as': autonomous_system,
                    'provider': provider,
                    'country': country,
                    'header': header}
            res.append(data)
        except:
            pass
    return res


def retrieve_txt_record(table):
    """
    Function copied from DNSDumpster API to cancel
    errors related to index list out of range
    """
    res = []
    for td in table.findAll('td'):
        res.append(td.text)
    return res

def search(domain):
    """
    Function copied from DNSDumpster API to cancel
    errors related to index list out of range
    """
    dnsdumpster_url = 'https://dnsdumpster.com/'
    
    session = requests.Session()
    req = session.get(dnsdumpster_url)
    soup = BeautifulSoup(req.content, 'html.parser')
    csrf_middleware = soup.findAll('input', attrs={'name': 'csrfmiddlewaretoken'})[0]['value']
    
    cookies = {'csrftoken': csrf_middleware}
    headers = {'Referer': dnsdumpster_url}
    data = {'csrfmiddlewaretoken': csrf_middleware, 'targetip': domain}
    req = session.post(dnsdumpster_url, cookies=cookies, data=data, headers=headers)
    
    if req.status_code != 200:
        print(
            "Unexpected status code from {url}: {code}".format(
                url=dnsdumpster_url, code=req.status_code),
            file=sys.stderr,
        )
        return []
    
    if 'error' in req.content.decode('utf-8'):
        print("There was an error getting results", file=sys.stderr)
        return []
    
    soup = BeautifulSoup(req.content, 'html.parser')
    tables = soup.findAll('table')
    
    res = {}
    res['domain'] = domain
    res['dns_records'] = {}
    res['dns_records']['dns'] = retrieve_results(tables[0])
    res['dns_records']['mx'] = retrieve_results(tables[1])
    res['dns_records']['txt'] = retrieve_txt_record(tables[2])
    res['dns_records']['host'] = retrieve_results(tables[3])
    
    # Network mapping image
    try:
        tmp_url = 'https://dnsdumpster.com/static/map/{}.png'.format(domain)
        image_data = base64.b64encode(session.get(tmp_url).content)
    except:
        image_data = None
    finally:
        res['image_data'] = image_data
    
    # XLS hosts.
    # eg. tsebo.com-201606131255.xlsx
    try:
        pattern = r'https://dnsdumpster.com/static/xls/' + domain + '-[0-9]{12}\.xlsx'
        xls_url = re.findall(pattern, req.content.decode('utf-8'))[0]
        xls_data = base64.b64encode(session.get(xls_url).content)
    except Exception as err:
        xls_data = None
    finally:
        res['xls_data'] = xls_data
    
    return res



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
        results = search(domain)
        if not results:
            continue
        subdomains += list(set(find('domain', results['dns_records'])))
        subdomains += list(set(find('reverse_dns', results['dns_records'])))
    return subdomains
