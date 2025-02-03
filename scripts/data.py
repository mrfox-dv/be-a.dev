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

    # Initialize an empty list to store all records
    all_records = []

    # Read and process all JSON files in the domains directory
    for json_file in domains_dir.glob('*.json'):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # If the file contains a list, extend all_records
                if isinstance(data, list):
                    all_records.extend(data)
                # If it's a single record, append it
                else:
                    all_records.append(data)
        except Exception as e:
            print(f"Error processing {json_file.name}: {str(e)}")

    # Sort records to ensure consistent output
    all_records.sort(key=lambda x: str(x))

    # Write the combined records to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_records, f, ensure_ascii=False, indent=2)

    print(f"Successfully merged {len(all_records)} records into {output_file}")

if __name__ == "__main__":
    merge_domain_files() 