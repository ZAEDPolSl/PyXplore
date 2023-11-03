from datetime import datetime
import json
import logging
import pandas as pd
import re
import time
import traceback
from tqdm import tqdm

from utils.helpers import Record, create_payload, get_ieee_headers
from utils.session import Session


CONTENT_TYPE = [
        "ContentType:Conferences",
        "ContentType:Journals",
        "ContentType:Books",
        "ContentType:Magazines",
        "ContentType:Early Access Articles",
        "ContentType:Standards"
      ]

class IEEEXplorer:

    HOST = 'https://ieeexplore.ieee.org/rest/search'
    JS_RESULTS_REGEX = re.compile('xplGlobal.document.metadata=(?P<js_response>.*);')

    def __init__(
            self,
            keywords: list[str],
            start_year: int = 1884, #First record in IEEE Xplore.
            end_year: int = datetime.now().year,
            content_type: list[str] = CONTENT_TYPE
    ):
        self.keywords = keywords
        self.start_year = start_year
        self.end_year = end_year
        self.content_type = content_type
        self.session = Session()
        self.session.update_headers(get_ieee_headers())
        self.results_df = pd.DataFrame()

    def download_metadata(self) -> pd.DataFrame:
        start = time.time()
        payload = create_payload(
            keywords = self.keywords,
            start_year = self.start_year,
            end_year = self.end_year,
            content_type = self.content_type
        )
        response = self.session.post_json(self.HOST, data=json.dumps(payload))
        pages = response.get("totalPages")
        logging.info(f"Found {pages} pages with {response.get('totalRecords')} records!")
        for page in tqdm(range(pages+1)):
            payload['pageNumber'] = str(page)
            try:
                response = self.session.post_json(self.HOST, data=json.dumps(payload))
            except:
                logging.error(f'Cannot download metadate from page: {page}')
                continue
            for record in response.get('records', list()):
                try:
                    publication_url = f"https://ieeexplore.ieee.org{record.get('htmlLink')}"
                    publication_soup = self.session.get_soup(publication_url)
                    for script in publication_soup.find_all("script", {"type": "text/javascript"}):
                        match = re.search(self.JS_RESULTS_REGEX, script.text)
                        abstract = record.get('abstract')
                        if match:
                            api_response = json.loads(match.group('js_response'))
                            abstract = api_response.get('abstract', abstract)
                            keywords_list = [keyword for keywords in api_response.get('keywords', []) \
                                            for keyword in keywords.get("kwd", [])  \
                                            if keywords.get('type', '').strip() in ["IEEE Keywords", "Author Keywords"]] 
                            break
                    else:
                        logging.warning(f'JavaScript result with api response not found!')
                    publication = Record(
                                id = int(record.get('articleNumber')),
                                title = record.get('articleTitle'),
                                url = publication_url,
                                authors = [author.get('searchablePreferredName') or author.get('preferredName') for author in \
                                            record.get('authors', list())],
                                abstract = abstract,
                                kind = record.get('articleContentType'),
                                citations = int(record.get('citationCount', 0)),
                                source= record.get('publicationTitle'),
                                year = int(record.get('publicationYear'), 0),
                                keywords = list(set(keywords_list)) if "keywords_list" in locals() else list()
                                )
                    publication_df = pd.DataFrame([publication.to_dict()])
                    self.results_df = pd.concat([self.results_df, publication_df], ignore_index=True)
                    logging.info(f'Publication {publication.id} has been imported!')
                except Exception as exe:
                    logging.error(f'Unhandled exception - Import error!: {exe} Traceback: {traceback.format_exc()}')
        logging.info(f'Import end work in {(time.time()-start)/60} minutes! Imported: {len(self.results_df)} records.')