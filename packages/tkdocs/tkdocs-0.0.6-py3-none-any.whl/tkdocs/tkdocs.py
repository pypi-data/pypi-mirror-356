"""Download and parse parliamentary documents from the Dutch Lower House website"""

import datetime
from pathlib import Path
from pathlib import PosixPath
from urllib.parse import urlencode
import time
import re
import locale
from dateutil import tz
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
locale.setlocale(locale.LC_ALL, 'nl_NL')


BASE = 'https://www.tweedekamer.nl'
QUERY_URL_BASE = 'https://www.tweedekamer.nl/zoeken'
DOC_TYPES = ['Moties', 'Amendementen']


def create_url(params):
    """Create query url"""
    params_dict = {'srt': 'date:desc:date'}
    errors = False
    sep = ' + OR + '
    if 'operator' in params:
        operator = params['operator']
        if not isinstance(operator, str) or operator.upper() not in ['OR', 'AND']:
            print('Please provide operator as either OR or AND')
            errors = True
        else:
            sep = f' + {operator.upper()} + '
    if 'query' in params:
        query_terms = [term.strip() for term in params['query'].split(',')]
        params_dict['qry'] = sep.join(query_terms)
    if 'fromdate' in params:
        fromdate = params['fromdate']
        if pd.isna(pd.to_datetime(fromdate, errors='coerce')):
            print('Please provide `fromdate` as valid date, yyyy-mm-dd')
            errors = True
        else:
            params_dict['fromdate'] = fromdate
    if 'todate' in params:
        todate = params['todate']
        if pd.isna(pd.to_datetime(todate, errors='coerce')):
            print('Please provide `todate` as valid date, yyyy-mm-dd')
            errors = True
        else:
            params_dict['todate'] = todate
    if 'doc_type' in params:
        doc_type = params['doc_type']
        if doc_type.lower() in ['motie', 'moties']:
            doc_type = 'Moties'
        if doc_type.lower() in ['amendement', 'amendementen']:
            doc_type = 'Amendementen'
        if doc_type.lower() in ['motie', 'moties']:
            doc_type = 'Moties'
        if doc_type in DOC_TYPES:
            params_dict['fld_prl_kamerstuk'] = doc_type
        else:
            print(f'doc_type {doc_type} not implemented (yet)')
            print('Please use one of the following doc_types:')
            print('\t', ', '.join(DOC_TYPES))
            errors = True
    if errors:
        return None
    return f'{QUERY_URL_BASE}?{urlencode(params_dict)}'


def extract_next_link(soup):
    """Find link to next page with result, if exists"""
    next_link = soup.find('a', {'rel': 'next'})
    if not next_link:
        return None
    next_link = next_link.get('href')
    return  f'https://www.tweedekamer.nl/zoeken{next_link}'


def extract_result_urls(soup):
    """Find urls of pages listing votes"""
    h4s = soup.find_all('h4')
    urls = [
        h4.find('a').get('href')
        for h4 in h4s
    ]
    urls = [
        f'{BASE}{url}'
        for url
        in urls
        if '/kamerstukken/' in url # KEEP THIS?
    ]
    return urls


def get_result_urls(current):
    """Navigate through result pages and extract urls"""
    result_urls = []
    while current:
        resp = requests.get(current, timeout=30)
        soup = bs(resp.text, 'lxml')
        result_urls.extend(extract_result_urls(soup))
        current = extract_next_link(soup)
        time.sleep(1)

    return result_urls


def clean_title(title):
    """Remove clutter"""
    if not title:
        return None
    title = title.replace('\n', '')
    if title.startswith('Motie:'):
        title = title.replace('Motie:', '')
    if title.startswith('Amendement:'):
        title = title.replace('Amendement:', '')
    return title.strip()



def clean_sponsor(sponsor):
    """Remove clutter"""
    for label in ['Indiener', 'Eerste ondertekenaar', 'Medeindiener', 'Mede ondertekenaar']:
        if sponsor.startswith(label):
            sponsor = sponsor.replace(label, '').strip()
    sponsor = ' '.join([
        element.strip()
        for element
        in sponsor.split('\n')
    ])
    return sponsor.strip()


def process_m_card(m_card, details):
    """Extract meeting details"""
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    utc = pd.to_datetime(m_card.find('time')['datetime'])
    utc = utc.replace(tzinfo=from_zone)
    h3_txt = m_card.find('h3').text.strip()
    if h3_txt == 'Stemmingen' or 'STEMMINGEN' in h3_txt:
        suffix = 'voting'
    else:
        suffix = 'debate'
    details[f'date_{suffix}'] = utc.astimezone(to_zone).strftime('%Y-%m-%d')
    details[f'url_{suffix}'] = BASE + m_card.find('a').get('href')
    return details


def extract_details(url):
    """Get voting details"""
    resp = requests.get(url, timeout=30)
    soup = bs(resp.text, 'lxml')
 
    details = {}
 
    # Title
    try:
        details['title'] = clean_title(soup.find('h1').text)
    except AttributeError:
        pass
 
    # Sponsors
    sponsors = soup.find_all('li', class_='m-list__item--variant-member')
    sponsor_lst = []
    co_sponsor_lst = []
    for sponsor in sponsors:
        sponsor_text = sponsor.text.strip()
        if sponsor_text.startswith('Indiener') or sponsor_text.startswith('Eerste ondertekenaar'):
            sponsor_lst.append(clean_sponsor(sponsor_text))
        if sponsor_text.startswith('Medeindiener') or sponsor_text.startswith('Mede ondertekenaar'):
            co_sponsor_lst.append(clean_sponsor(sponsor_text))
    details['sponsors'] = '|'.join(sponsor_lst)
    details['co_sponsors'] = '|'.join(co_sponsor_lst)
 
    # Dates and urls
    details['url'] = url
    m_cards = soup.find_all(class_='m-card')
    for m_card in m_cards:
        details = process_m_card(m_card, details)
    for a_download in soup.find_all('a', {'href': re.compile(r'/download.*?')}):
        details['download_link'] = BASE + a_download.get('href')
        break
 
    # Result
    for h3 in soup.find_all('h3'):
        h3_text = h3.text.strip()
        if h3_text.startswith('Aangenomen') or h3_text.startswith('Verworpen'):
            details['result'] = h3_text
            break
    for div in soup.find_all('div', class_='m-vote-result__label'):
        div_text = div.text.strip()
        if div_text.startswith('Voor:'):
            details['total_support'] = int(div_text.split(':')[-1].strip())
 
    # Party votes
    vote_table = soup.find('table')
   
    if vote_table:
        for row in vote_table.find_all('tr'):
            party_details = [td.text for td in row.find_all('td')]
            if not party_details:
                continue
            party = party_details[0]
            vote = party_details[2]
            seats = party_details[1]
            if not seats.isnumeric() and 'hoofdelijk' in soup.text:
                details['hoofdelijk'] = True
                print('hoofdelijk:', url)
                break
            if seats == '':
                seats = None
            else:
                seats = int(seats)
            if len(party_details) == 4 and 'Niet deelgenomen' in party_details[3]:
                vote = 'Niet deelgenomen'
            details[f'{party}_vote'] = vote
            details[f'{party}_seats'] = seats
 
    return details


def process_results(df):
    """Adjust order of columns and add columns for terms contained"""
    ordered_columns = [
        'title',
        'sponsors',
        'co_sponsors',
        'url',
        'date_debate',
        'url_debate',
        'date_voting',
        'url_voting',
        'download_link',
        'result',
        'total_support',
    ]
    seat_cols = {
        col: df[col].dropna().median()
        for col in df.columns
        if col.endswith('_seats')
    }
    seat_cols = sorted(seat_cols.items(), key=lambda x:x[1], reverse=True)
    for tup in seat_cols:
        col = tup[0]
        ordered_columns.append(col.replace('_seats', '_vote'))
        ordered_columns.append(col)
    ordered_columns = [col for col in ordered_columns if col in list(df.columns)]


    df = df[ordered_columns].copy()

    return df


def query_tk(**params):
    """Download and store results for query
    :param dir_results: directory where results will be stored (default value: ../data)
    :param query: search terms, separated with a comma (optional)
    :param fromdate: from date (yyyy-mm-dd, optional)
    :param todate: to date (yyyy-mm-dd, optional)
    :param operator: whether to combine search terms using OR or AND (default value: OR)
    :param doc_type: document type (e.g. Moties, Amendementen, optional)
    :param update_urls: if True, search query will be refreshed so new results may be added
        (default value: True)
    :param update_results: if True, previously downloaded results will be updated
        (default value: False)
    :param download_files: if True, pdf files will be downloaded (default value: False)

    """

    if 'dir_results' not in params:
        print('Please provide directory to store results as `dir_results`')
        return
    dir_results = params['dir_results']
    if not isinstance(dir_results, PosixPath):
        dir_results = Path(dir_results)
    dir_results.mkdir(exist_ok=True)

    query_url = create_url(params)
    if not query_url:
        return

    update_urls = params.get('update_urls', True)
    update_results = params.get('update_results', False)
    download_files = params.get('download_files', False)

    print(datetime.datetime.now())
    print(query_url)

    path_result_urls = dir_results / 'result_urls.txt'
    if path_result_urls.is_file() and not update_urls:
        result_urls = path_result_urls.read_text().split('\n')
    else:
        result_urls = get_result_urls(query_url)
        path_result_urls.write_text('\n'.join(result_urls))

    path_results = dir_results / 'results.xlsx'
    if path_results.is_file() and not update_results:
        prev_results = pd.read_excel(path_results)
        done = list(prev_results.url)
    else:
        prev_results = pd.DataFrame()
        done = []
    todo = [url for url in result_urls if url not in done]

    new_results_list = []
    for i, url in enumerate(todo):
        if i % 10 == 0:
            print(i, '/', len(todo), datetime.datetime.now())
        if i % 10 == 0 and new_results_list:
            results = pd.concat([prev_results, pd.DataFrame(new_results_list)], axis=0)
            results = process_results(results)
            results.to_excel(path_results, index=False)
        new_results_list.append(extract_details(url))
        time.sleep(1)
    results = pd.concat([prev_results, pd.DataFrame(new_results_list)], axis=0)
    results = process_results(results)
    results.to_excel(path_results, index=False)

    if download_files:
        print('Downloading files')
        dir_files = dir_results / 'files'
        dir_files.mkdir(exist_ok=True)
        todo = results.download_link.dropna()
        for i, url in enumerate(todo):
            if i % 10 == 0:
                print(i, '/', len(todo), datetime.datetime.now())
            filename = ''.join([char for char in url.split("/")[-1] if char.isalnum()])
            path = dir_files / f'{filename}.pdf'
            if path.is_file():
                continue
            resp = requests.get(url, timeout=30)
            with open(path, 'wb') as f:
                f.write(resp.content)
            time.sleep(1)
    return
