#This code is to convert the json file to gzip of ndjson file
import json
import gzip
import os

def json_to_ndjson_gz(input_file, output_file):
    # Get the absolute path of the data directory
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')

    # Construct the absolute paths for the input and output files
    input_file_path = os.path.join(data_dir, input_file)
    output_file_path = os.path.join(data_dir, output_file)

    with open(input_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    with gzip.open(output_file_path, 'wt', encoding='utf-8') as ndjson_gz_file:
        for item in data:
            ndjson_gz_file.write(json.dumps(item) + '\n')

# Convert JSON to NDJSON.gz
json_to_ndjson_gz('all_laptop_data.json', 'deviveryDateAndAdressfinal.ndjson.gz')