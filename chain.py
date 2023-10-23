import os
import base64
def read_file(path):
    if os.path.exists(path):
        with open('path_to_file', 'rb') as file:
            file_content = file.read()

        hex_string = file_content.hex()
        return hex_string
    else:
        print(f"{path} does not exist!")
        return 0


