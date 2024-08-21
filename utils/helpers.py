from dataclasses import dataclass, asdict
import re
from typing import Optional

GITHUB_REGEX = re.compile(r"(github.com|git.io)/.*")
TAG_REGEX = re.compile(r'<[^>]+>')
SUB_REGEX = re.compile(r'<sub .*</sub>')
URL_REGEX = re.compile(r'http.*')

@dataclass
class Record:
    """Metadata for scientific records."""

    id: int
    title: str
    url : str
    authors: list[str]
    kind: Optional[str] = None
    source: Optional[str] = None
    github: Optional[str] = None
    citations: Optional[int] = None
    year: Optional[int] = None
    abstract: Optional[str] = None   
    keywords: Optional[list[str]] = None
    url_from_abstract: Optional[str] = None

    def __post_init__(self):
        if self.abstract:
            self.abstract = re.sub(SUB_REGEX, '', self.abstract)
            github_match = re.search(GITHUB_REGEX, self.abstract)
            if github_match:
                self.github = TAG_REGEX.sub('',github_match[0])
            http_match = re.search(URL_REGEX, self.abstract)
            if http_match:
                self.url_from_abstract = http_match[0]

    def to_dict(self) -> dict:
        return asdict(self)


def get_all_metadata(keyword: str) -> str:
    return f"\"All Metadata\": \"{keyword}\""
    
def create_query_text(keyword: str) -> str:
    """
    "(\"All Metadata\":deep learning) AND (\"All Metadata\":\"histopathological\" OR \"All Metadata\":\"h&e\") AND (\"All Metadata\":images)"
    """
    return f"({get_all_metadata(keyword)})"

def create_payload(keywords: list[str],
                   start_year: int,
                   end_year: int,
                   content_type: list[str]) -> dict:
    query_text = []
    for keyword in keywords:
        if isinstance(keyword, list):
            query = [get_all_metadata(text) for text in keyword]
            query = " OR ".join(query)
            query_text.append(f"({query})")
        else:
            query_text.append(create_query_text(keyword))
    payload =  {
        "action": "search",
        "newsearch": True,
        "matchBoolean": True,
        "pageNumber": "1",
        "queryText": (" AND ".join(query_text)),
        "ranges": [
            f"{start_year}_{end_year}_Year"
        ],
        "refinements":content_type,
        "highlight": True,
        "returnFacets": [
            "ALL"
        ],
        "returnType": "SEARCH",
        "matchPubs": True
    }
    return payload

def get_ieee_headers() -> dict:
    return {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "Referer": "https://ieeexplore.ieee.org/search/searchresult.jsp"
            }