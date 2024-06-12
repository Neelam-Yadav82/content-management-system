import os
import base64
import traceback
from typing import Dict


def file_to_base64(file_path: str) -> Dict[str, str]:
    """
    Convert a file to Base64 string.

    Args:
        file_path (str): Path to the file to be converted.

    Returns:
        dict: A dictionary containing the file name, extension, and Base64 string.
              Returns None if an error occurs.
    """
    try:
        # Extract file name and extension from file path
        file_name, file_extension = os.path.splitext(os.path.basename(file_path))

        with open(file_path, "rb") as file:
            # Read file data
            file_data = file.read()
            # Encode file data as Base64
            base64_encoded = base64.b64encode(file_data)
            # Decode bytes to string (Python 3)
            base64_encoded_string = base64_encoded.decode("utf-8")

            return {
                "file_name": file_name,
                "extension": file_extension,
                "base64_string": base64_encoded_string,
            }
    except Exception as e:
        print(e, traceback.format_exc())
        return None
