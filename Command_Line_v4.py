import sys
import os
import json
from datetime import datetime
import base64

from encryption import generate_keys, check_keys_exist
from file_operations import convert_file_to_binary_string
from db import get_page_data, set_page_data

def main():
    if len(sys.argv) < 4:
        print("Usage: kv_service_tools <command> '<page name> <page num>' '<page string>'")
        sys.exit(1)

    command = sys.argv[1]
    page_name, page_num = sys.argv[2].split()
    page_string = sys.argv[3]

    if not check_keys_exist():
        print("Public and private keys do not exist. Generating new keys...")
        generate_keys()

    if command == "set":
        handle_set_command(page_name, page_num, page_string)
    elif command == "get":
        handle_get_command(page_name, page_num)
    else:
        print("Invalid command. Use 'set' or 'get'.")

def handle_set_command(page_name, page_num, page_string):
    page_data = parse_page_string(page_string)
    # Serialize page data and store it
    set_page_data(page_name, page_num, json.dumps(page_data))
    print(f"Page data set for {page_name} {page_num}")

def handle_get_command(page_name, page_num):
    page_data = get_page_data(page_name, page_num)
    if page_data:
        print(f"Page data for {page_name} {page_num}: {page_data}")
    else:
        print(f"No data found for {page_name} {page_num}")

def parse_page_string(page_string):
    parts = page_string.split(',')
    page_data = {
        "receiver_public_key": parts[0],
        "message_type": parts[1],
        "timestamp": parts[2],
        "message_type_extension": parts[3],
        "message": parts[4]
    }
    # Handle file message type
    if page_data['message_type'].lower() == 'file':
        page_data['message'] = convert_file_to_binary_string(page_data['message'])
    return page_data

if __name__ == "__main__":
    main()
