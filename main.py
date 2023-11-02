import json
import pandas as pd
import re
import time
import datetime
from utils.session import Session
from utils.logger import ConsoleLogger
from utils.helpers import Record, create_payload, get_ieee_headers

#region: config
HOST = 'https://ieeexplore.ieee.org/rest/search'
results_df = pd.DataFrame()
logger = ConsoleLogger()
start = time.time()
#endregion

#region: regex
JS_RESULTS_REGEX = re.compile('xplGlobal.document.metadata=(?P<js_response>.*);')
GITHUB_REGEX = re.compile(r'github.com.*')
SUB_REGEX = re.compile(r'<sub .*</sub>')
URL_REGEX = re.compile(r'http.*')
#endregion

#region: load query configuration
with open('config.json') as config:
    config = json.load(config)
#endregion

file_name = f"{datetime.datetime.now().date().strftime('%Y%m%d')}_results.parquet"
with Session(logger) as session:
    #results_df = pd.DataFrame()
    session.update_headers(get_ieee_headers())
    payload= create_payload(config)
    response = session.post_json(HOST, data=json.dumps(payload))
    pages = response.get("totalPages")
    logger.info(f"Found {pages} pages with {response.get('totalRecords')} records!")
    for page in range(pages+1):
        payload['pageNumber'] = str(page)
        time.sleep(10)
        try:
            response = session.post_json(HOST, data=json.dumps(payload))
        except:
            logger.error(f'Cannot download metadate from page: {page}')
            continue
        for record in response.get('records', list()):
            try:
                publication = Record()
                publication.id = int(record.get('articleNumber'))
                publication.abstract = record.get('abstract')
                publication.kind = record.get('articleContentType')
                publication.title = record.get('articleTitle')
                publication.ieee_citations = int(record.get('citationCount'))
                publication.name = record.get('publicationTitle')
                publication.year = int(record.get('publicationYear'))
                publication.url = f"https://ieeexplore.ieee.org{record.get('htmlLink')}"
                publication.authors = list()
                for author in record.get('authors', list()):
                    author = author.get('searchablePreferredName') or author.get('preferredName')
                    if publication.first_author is None:
                        publication.first_author = author #set first author from collection
                    publication.authors.append(author)
                publication_soup = session.get_soup(publication.url)
                api_response = ''
                for script in publication_soup.find_all("script", {"type": "text/javascript"}):
                    match = re.search(JS_RESULTS_REGEX, script.text)
                    if match:
                        api_response = json.loads(match.group('js_response'))
                        break
                if api_response:
                    publication.abstract = api_response.get('abstract')
                    keywords_list = list()
                    for keywords in api_response.get('keywords', []):
                        if keywords.get('type', '').strip() in ["IEEE Keywords", "Author Keywords"]:
                            keywords_list += keywords.get('kwd',[])
                    publication.keywords = list(set(keywords_list))
                else:
                    session.logger.warning(f'JavaScript result with api response not found!')
                if publication.abstract: 
                    publication.abstract = re.sub(SUB_REGEX, '', publication.abstract)
                    github_match = re.search(GITHUB_REGEX, publication.abstract)
                    if github_match:
                        publication.github = github_match[0]
                    http_match = re.search(URL_REGEX, publication.abstract)
                    if http_match:
                        publication.url_from_abstract = http_match[0]
                publication_df = pd.DataFrame([publication.to_dict()])
                results_df = pd.concat([results_df, publication_df], ignore_index=True)
                logger.info(f'Publication {publication.id} has been imported! Imported: {len(results_df)}')
                if  not (len(results_df) % 1000):
                    results_df.to_parquet(file_name, engine="pyarrow")
            except Exception as exe:
                logger.error(f'Import error!: {exe}')
        logger.info(f'Page: {page} has been imported. Status: {page}/{pages}.')
    results_df.to_parquet(f"{file_name}", engine="pyarrow")
end = time.time()
logger.info(f'Import end work in {(end-start)/60} minutes! Imported: {len(results_df)} records.')
