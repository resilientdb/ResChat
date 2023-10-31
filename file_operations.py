# import os
#
#
# # Read file into a string
# def read_file(path: str) -> (str or None):
#     if os.path.exists(path):
#         with open(path, 'rb') as file:  # Use the variable path, not the string 'path_to_file'
#             file_content = file.read()
#
#         hex_string = file_content.hex()
#         return hex_string
#     else:
#         print(f"{path} does not exist!")
#         return None
#
#
# # Reconstruct file from string
# def write_file(path: str, hex_string: str):
#     try:
#         # Convert the hex string back to bytes
#         file_content = bytes.fromhex(hex_string)
#
#         # Write the bytes to the file
#         with open(path, 'wb') as file:
#             file.write(file_content)
#
#         print(f"File written successfully to {path}")
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#
#


import os


def read_file_to_bin_string(path: str) -> (str or None):
    if os.path.exists(path):
        with open(path, 'rb') as file:
            file_content = file.read()
            bin_string = ''.join(format(byte, '08b') for byte in file_content)
        return bin_string
    else:
        print(f"{path} does not exist!")
        return None


def write_bin_string_to_file(path: str, bin_string: str):
    try:
        file_content = bytes(int(bin_string[i:i+8], 2) for i in range(0, len(bin_string), 8))
        with open(path, 'wb') as file:
            file.write(file_content)
        print(f"File written successfully to {path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


