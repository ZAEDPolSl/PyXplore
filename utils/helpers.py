class Record:
    
    def __init__(self, 
                title: str = None,
                first_author: str = None,
                authors: list[str] = None,
                kind: str = None,
                name: str = None,
                github: str = None,
                ieee_citations: int = None,
                year: int = None,
                abstract: str = None,
                url: str = None,
                id: int = None,
                keywords: list[str] = None,
                url_from_abstract = None
    ):
        self.title = title
        self.first_author = first_author
        self.authors = authors
        self.kind = kind
        self.name = name
        self.github = github
        self.ieee_citations = ieee_citations
        self.year = year
        self.abstract = abstract
        self.url = url
        self.id = id
        self.keywords = keywords
        self.url_from_abstract = url_from_abstract

    def to_dict(self):
        return {
            "Title": self.title,
            "Year": self.year,
            "Kind": self.kind,
            "Name": self.name,
            "First author": self.first_author,
            "Authors": self.authors,
            "IEEE citations": self.ieee_citations,
            "Github": self.github,
            "Abstract": self.abstract,
            "Website": self.url,
            "Id": self.id,
            "Keywords": self.keywords,
            "URL from abstract": self.url_from_abstract
        }

def get_all_metadata(keyword: str) -> str:
    return f"\"All Metadata\": \"{keyword}\""
    
def create_query_text(keyword: str) -> str:
    """
    "(\"All Metadata\":deep learning) AND (\"All Metadata\":\"histopathological\" OR \"All Metadata\":\"h&e\") AND (\"All Metadata\":images)"
    """
    return f"({get_all_metadata(keyword)})"

def create_payload(config: dict) -> dict:
    query_text = []
    default_content = [
        "ContentType:Conferences",
        "ContentType:Journals",
        "ContentType:Books",
        "ContentType:Magazines",
        "ContentType:Early Access Articles",
        "ContentType:Standards"
      ]
    for keyword in config['keywords']:
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
            f"{config.get('start_year', 2000)}_{config.get('end_year', 2023)}_Year"
        ],
        "refinements": config.get("content_type", default_content),
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