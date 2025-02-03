import os
import json
import sys
import re
from typing import Tuple, Dict, Any, Union

def validate_filename(filename: str) -> Tuple[bool, Union[str, None]]:
    """
    Validates domain filename against specified rules.
    
    Args:
        filename: The filename to validate
        
    Returns:
        Tuple[bool, Union[str, None]]: (is_valid, error_message)
    """
    if not filename or filename == ".json":
        return False, "Filename is too short"

    if filename != filename.lower():
        return False, "Filename contains uppercase letters"

    if ".." in filename:
         return False, "Filename contains consecutive dots"

    if filename.startswith("."):
        return False, "Filename starts with a dot"
    
    if " " in filename:
        return False, "Filename contains a space"

    if not re.match(r"^[a-z0-9.-]+\.json$", filename):
        return False, "Filename contains invalid characters or invalid extension"

    if filename.count(".json") > 1:
        return False, "Filename contains more than one .json extension"
    
    if ".is-a.dev" in filename:
        return False, "Filename contains `.is-a.dev`"

    return True, None

def validate_record_type(record_data: Dict[str, Any], record_type: str) -> Tuple[bool, Union[str, None]]:
    """
    Validates a specific type of DNS record.
    
    Args:
        record_data: The record data to validate
        record_type: The record type (A, AAAA, CNAME etc.)
        
    Returns:
        Tuple[bool, Union[str, None]]: (is_valid, error_message)
    """
    value = record_data[record_type]
    
    validators = {
        "A": _validate_a_record,
        "AAAA": _validate_aaaa_record,
        "CNAME": _validate_cname_record,
        "URL": _validate_url_record,
        "MX": _validate_mx_record,
        "TXT": _validate_txt_record,
        "NS": _validate_ns_record,
        "SRV": _validate_srv_record,
        "CAA": _validate_caa_record
    }
    
    if record_type in validators:
        return validators[record_type](value)
    
    return False, f"Unsupported record type: {record_type}"

def _validate_a_record(value: Any) -> Tuple[bool, Union[str, None]]:
    if not isinstance(value, list):
        return False, "A record value must be a list of IPv4 addresses"
    
    for ip in value:
        if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
            return False, "Invalid IPv4 address in A record"
    
    return True, None

def _validate_aaaa_record(value: Any) -> Tuple[bool, Union[str, None]]:
    if not isinstance(value, list):
        return False, "AAAA record value must be a list of IPv6 addresses"
    
    for ip in value:
        if not re.match(r'^[0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4}){7}$', ip) and not re.match(r'^([0-9a-fA-F]{1,4}:){1,7}:$', ip):
            return False, "Invalid IPv6 address in AAAA record"
    
    return True, None

def _validate_cname_record(value: Any) -> Tuple[bool, Union[str, None]]:
    if not isinstance(value, str):
        return False, "CNAME record value must be a string (hostname)"
    return True, None

def _validate_url_record(value: Any) -> Tuple[bool, Union[str, None]]:
    if not isinstance(value, str):
        return False, "URL record value must be a string (URL)"
    if not re.match(r'^https?://', value):
        return False, "URL record value must be a valid URL"
    return True, None

def _validate_mx_record(value: Any) -> Tuple[bool, Union[str, None]]:
    if not isinstance(value, list):
        return False, "MX record value must be a list of hostnames"
    return True, None

def _validate_txt_record(value: Any) -> Tuple[bool, Union[str, None]]:
    if not isinstance(value, str) and not isinstance(value, list):
        return False, "TXT record value must be a string or a list of strings"
    if isinstance(value, list):
        for item in value:
            if not isinstance(item, str):
                return False, "TXT record value (list) must contain only strings"
    return True, None

def _validate_ns_record(value: Any) -> Tuple[bool, Union[str, None]]:
    if not isinstance(value, list):
        return False, "NS record value must be a list of hostnames"
    return True, None

def _validate_srv_record(value: Any) -> Tuple[bool, Union[str, None]]:
    if not isinstance(value, list):
        return False, "SRV record value must be a list of service records"
    for srv_record in value:
        if not isinstance(srv_record, dict):
            return False, "SRV record must be an object"
        if not all(key in srv_record for key in ["priority", "weight", "port", "target"]):
            return False, "SRV record is missing required fields (priority, weight, port, target)"
        if not all(isinstance(srv_record[key], int) for key in ["priority", "weight", "port"]):
            return False, "SRV record fields priority, weight and port must be integers"
        if not isinstance(srv_record["target"], str):
            return False, "SRV record target field must be a string (hostname)"
    return True, None

def _validate_caa_record(value: Any) -> Tuple[bool, Union[str, None]]:
    if not isinstance(value, list):
        return False, "CAA record value must be a list of CAA records"
    for caa_record in value:
        if not isinstance(caa_record, dict):
            return False, "CAA record must be an object"
        if not all(key in caa_record for key in ["flags", "tag", "value"]):
            return False, "CAA record is missing required fields (flags, tag, value)"
        if not isinstance(caa_record["flags"], int):
            return False, "CAA record flag field must be a integer"
        if not isinstance(caa_record["tag"], str):
            return False, "CAA record tag field must be a string"
        if not isinstance(caa_record["value"], str):
            return False, "CAA record value field must be a string"
    return True, None

def validate_json_content(filepath: str) -> Tuple[bool, Union[str, None]]:
    """
    Validates JSON file content against specified structure.
    
    Args:
        filepath: Path to the JSON file
        
    Returns:
        Tuple[bool, Union[str, None]]: (is_valid, error_message)
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return False, "Invalid JSON format"
    
    # Validate basic structure
    if not _validate_basic_structure(data):
        return False, "Invalid basic structure"
    
    # Validate record types
    valid_record_types = ["CNAME", "A", "AAAA", "URL", "MX", "TXT", "NS", "SRV", "CAA"]
    found_record_types = [key for key in data["record"].keys() if key in valid_record_types]
    
    if not found_record_types:
        return False, "Missing valid record type"
    
    if len(found_record_types) > 1 and "CNAME" in found_record_types:
        return False, "CNAME record cannot be used with other record types"
    
    # Validate proxied field if present
    if "proxied" in data:
        if not isinstance(data["proxied"], bool):
            return False, "proxied field must be a boolean"
        
        if data["proxied"]:
            proxy_eligible_records = {"A", "AAAA", "CNAME"}
            has_proxy_eligible = any(rt in proxy_eligible_records for rt in found_record_types)
            if not has_proxy_eligible:
                return False, "Proxied is true but there are no records that can be proxied (A, AAAA, CNAME expected)"
    
    # Validate each record type
    for record_type in found_record_types:
        is_valid, error = validate_record_type(data["record"], record_type)
        if not is_valid:
            return False, error
    
    return True, None

def _validate_basic_structure(data: Dict[str, Any]) -> bool:
    """Validates the basic structure of JSON data."""
    if "owner" not in data or not isinstance(data["owner"], dict):
        return False
    
    if "username" not in data["owner"] or "email" not in data["owner"]:
        return False
    
    if "record" not in data or not isinstance(data["record"], dict):
        return False
    
    return True

def main():
    """Main function: validates all domain files."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    domains_dir = os.path.join(script_dir, "../domains")
    reserved_file = os.path.join(script_dir, "../util", "reserved.json")

    try:
        with open(reserved_file, 'r') as f:
            reserved_domains = json.load(f)
    except FileNotFoundError:
        print(f"Error: Reserved domains file not found at {reserved_file}")
        sys.exit(1)
    except json.JSONDecodeError:
         print(f"Error: Invalid JSON in {reserved_file}")
         sys.exit(1)

    has_error = False
    for filename in os.listdir(domains_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(domains_dir, filename)
            
            # Check if domain is reserved
            domain_prefix = filename[:-5]
            if domain_prefix in reserved_domains:
                print(f"Error: {filename} is a reserved domain.")
                has_error = True
                continue

            # Validate filename
            is_valid_filename, filename_error = validate_filename(filename)
            if not is_valid_filename:
                print(f"Error: {filename} - {filename_error}")
                has_error = True
                continue
                
            # Validate json content
            is_valid_json, json_error = validate_json_content(filepath)
            if not is_valid_json:
                print(f"Error: {filename} - {json_error}")
                has_error = True
    
    if has_error:
      sys.exit(1)
    else:
      print("All JSON files validated successfully.")


if __name__ == "__main__":
    main()