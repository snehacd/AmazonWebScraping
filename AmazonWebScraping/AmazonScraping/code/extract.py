#The below code is to convert gzip of ndjson file to json file to verify the data
import gzip
import json
import os

def ndjson_to_json(ndjson_file, json_file):
    # Get the absolute path of the data directory
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')

    # Construct the absolute paths for the input and output files
    ndjson_file_path = os.path.join(data_dir, ndjson_file)
    json_file_path = os.path.join(data_dir, json_file)

    with gzip.open(ndjson_file_path, 'rt', encoding='utf-8') as f:
        data = [json.loads(line) for line in f]
    
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Convert NDJSON.gz to JSON
ndjson_to_json('working.ndjson.gz', 'workingabc.json')
