import re, requests

from bs4 import BeautifulSoup
import sqlite3
from dateutil.parser import parse

USE_CACHE = False
SHOW_PREVIEW = True
DATABASE_NAME = 'data.sqlite'

BASE_URL = 'https://make.opendata.ch'
START_PAGE = BASE_URL + '/wiki/event:home'
FILTER_EVENTS = r'.*\/event:.*'
FILTER_PROJECTS = r'.*\/project:.*'
DATESTAMP_REGEXP = re.compile('^2')

fields = [
    'event',
    'event_url',
    'updated',
    'title',
    'url',
    'text',
    'html',
]

def run():
    # Set up a fresh database
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS data')
    fieldlist = " text, ".join(fields)
    c.execute(
        'CREATE TABLE data (' + fieldlist + ')'
    )
    conn.commit()

    # Download from cache
    if USE_CACHE:
        for page_count in range(0, 2):
            print ("Collecting page %d" % page_count)
            f = open('_cache/%d.html' % page_count, 'r')
            cache_data = f.read()
            soup = BeautifulSoup(cache_data, 'html.parser')
            rows = soup.select('tbody tr')
            save(c, rows)
            conn.commit()
            f.close()

    # Retrieve from server
    else:
        print ("Refreshing start page %s" % START_PAGE)
        page = requests.get(START_PAGE)
        soup = BeautifulSoup(page.content, 'html.parser')
        events = soup.select('a[href*="event:2"]')
        for e in events:
            name = e.get_text()
            url = e.get('href')
            if url.endswith('event:home'): continue
            if not url.startswith('http'): url = BASE_URL + url
            print ('Retrieving event: %s / %s' % (name, url))

            event_page = requests.get(url)
            event_soup = BeautifulSoup(event_page.content, 'html.parser')
            projects = event_soup.select('a[href*="wiki/project:"]')

            project_list = []
            for p in projects:
                p_name = p.get_text()
                p_url = p.get('href')
                if p_url.endswith('project:home'): continue
                if not p_url.startswith('http'): p_url = BASE_URL + p_url
                if not p_url in project_list:
                    project_list.append(p_url)
                    print("Downloading", p_url)
                    # extract meta
                    p_page = requests.get(p_url)
                    p_soup = BeautifulSoup(p_page.content, 'html.parser')
                    datestamp = p_soup.find('span', { 'title': DATESTAMP_REGEXP })
                    if datestamp:
                        datestamp = parse(datestamp.get_text())
                    else:
                        datestamp = '?'
                    content = p_soup.find('div', { 'class': 'dw-content' })
                    text = ''
                    if content is not None:
                        text = content.get_text()
                        content = content.encode_contents()
                    else:
                        content = ''
                    print (p_name, datestamp, len(text))

                c.execute(
                    '''
                    INSERT INTO data (
                        ''' + ','.join(fields) + '''
                    )
                    VALUES
                    (''' + '?,'*(len(fields)-1) + '''?)
                    ''',
                    [
                        name,
                        url,
                        datestamp,
                        p_name,
                        p_url,
                        text,
                        content,
                    ]
                )

            conn.commit()

    conn.close()

run()
