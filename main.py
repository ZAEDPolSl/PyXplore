import json

from utils.ieee import IEEEXplorer


#region: load query configuration
with open('config.json') as config:
    config = json.load(config)
#endregion

importer = IEEEXplorer(**config)
importer.download_metadata()