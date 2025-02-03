import os
import json
import sys
from typing import Dict, Any

def format_json_file(filepath: str) -> bool:
    """
    Format a single JSON file.
    
    Args:
        filepath: Path to the JSON file
        
    Returns:
        bool: Whether formatting was successful
    """
    try:
        # Read JSON file
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Rewrite file with consistent formatting
        # indent=4 for 4-space indentation
        # ensure_ascii=False to handle Unicode characters correctly
        # sort_keys=True for consistent key ordering
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False, sort_keys=True)
            # Add newline at end of file
            f.write('\n')
        
        return True
    except Exception as e:
        print(f"Error: Failed to process file {filepath} - {str(e)}")
        return False

def main():
    """Main function: format all domain files"""
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Get domains directory path
    domains_dir = os.path.join(script_dir, "../domains")

    if not os.path.exists(domains_dir):
        print(f"Error: Domains directory not found: {domains_dir}")
        sys.exit(1)

    has_error = False
    formatted_count = 0

    # Process all JSON files
    for filename in os.listdir(domains_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(domains_dir, filename)
            print(f"Formatting: {filename}")
            
            if format_json_file(filepath):
                formatted_count += 1
            else:
                has_error = True

    # Print summary
    print(f"\nFormatting complete:")
    print(f"Successfully processed files: {formatted_count}")
    
    if has_error:
        print("Warning: Some files failed to process")
        sys.exit(1)
    else:
        print("All files formatted successfully")

if __name__ == "__main__":
    main() 