from datetime import datetime
import json

from utils.ieee import IEEEXplorer


#region: load query configuration
with open('config.json') as config:
    config = json.load(config)
#endregion

importer = IEEEXplorer(**config)
importer.download_metadata()
file_name = datetime.strftime(datetime.now(), '%Y%m%d%H%M')
importer.results_df.to_parquet(f"{file_name}_search.parquet")
importer.results_df.to_csv(f"{file_name}_search.csv")