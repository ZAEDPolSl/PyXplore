# PyXplore - Description
Scientific Databases are often the main source for searching scientific literature in different fields. The ever-increasing number of scientific documents makes finding information of interest more time-consuming. Metadata provided in database queries allows for accurate information retrieval. In this work, we present a tool that allows searching scientific publications in the IEEE Xplore database based on input metadata. An example analysis of the results obtained through the proposed application was prepared for the subject of deep learning techniques in histopathology imaging. The
application can be used in any field including text detection or face recognition.

The proposed application allows performing complex search queries for all scientific documents in the IEEE Xplore using the API of the available database. The established records are serialized to a file and contain information such as title, unique identifier, link to the document in the database, number of citations, list of authors, keywords, abstract, type of publication, name of the journal/conference and link to the GitHub repository (if provided).

# Installation
If you are using the Poetry environment perform:
```
poetry install
```
otherwise run command:
```
pip install -r requirements.txt
```

# Usage
Define your query criteria in config.json file
```
{
    "keywords": ["deep", "learning", ["histopathological", "h&e"], "images"],
    "content_type": [
        "ContentType:Conferences",
        "ContentType:Journals",
        "ContentType:Books",
        "ContentType:Magazines",
        "ContentType:Early Access Articles",
        "ContentType:Standards"
      ],
    "start_year": 2000,
    "end_year": 2023
}
```

Keywords represented as inside list correspond to OR logical operation. All other words correspond to the logical operation AND. For example presented above, logical operations can be interpreted as:
"deep" AND "learning" AND ("histopahological" OR "h&e") AND "images"

# Contribution
This work was presented at the XXVII Gliwice Scientific Meetings conference. 
Feel free to contact me with any questions: Seweryn.Kalisz@polsl.pl