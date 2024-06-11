import os


# External function
def read_file(path: str) -> (str or None):
    """Read file into a string"""
    if os.path.exists(path):
        with open(path, 'rb') as file:
            file_content = file.read()

        hex_string = file_content.hex()
        return hex_string.encode()
    else:
        print(f"{path} does not exist!")
        return None


# External function
def write_file(path: str, file_string: str) -> None:
    """Reconstruct file from string"""
    try:
        # Convert the hex string back to bytes
        file_content = bytes.fromhex(file_string)

        # Write the bytes to the file
        with open(path, 'wb') as file:
            file.write(file_content)

        print(f"File written successfully to {path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
