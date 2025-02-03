import json
import os
from pathlib import Path

def merge_domain_files():
    # Get the script directory and construct paths
    script_dir = Path(__file__).parent
    domains_dir = script_dir.parent / 'domains'
    output_file = script_dir.parent / 'data' / 'all-records.json'

    # Ensure the data directory exists
    output_file.parent.mkdir(exist_ok=True)

    # Initialize a dictionary to store records by filename
    records_by_file = {}

    # Read and process all JSON files in the domains directory
    for json_file in domains_dir.glob('*.json'):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Store the data with filename as key
                records_by_file[json_file.name] = data
        except Exception as e:
            print(f"Error processing {json_file.name}: {str(e)}")

    # Sort the dictionary by keys to ensure consistent output
    records_by_file = dict(sorted(records_by_file.items()))

    # Write the combined records to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(records_by_file, f, ensure_ascii=False, indent=2)

    print(f"Successfully merged {len(records_by_file)} files into {output_file}")

if __name__ == "__main__":
    merge_domain_files() 