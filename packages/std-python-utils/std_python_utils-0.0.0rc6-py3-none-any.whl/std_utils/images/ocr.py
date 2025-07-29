import base64
from io import BytesIO

import pytesseract
from PIL import Image


def get_image_text_from_b64_img(data_uri):
    """
    Extracts text from a base64-encoded image string using OCR.

    Args:
    - data_uri (str): The base64-encoded image string, including the 'data:image/png;base64,' part.

    Returns:
    - str: The text extracted from the image.
    """
    # Regex to extract the base64-encoded data part
    data_key = "base64,"
    data_index = data_uri.index(data_key) + len(data_key)
    b64_data_prefix = data_uri[:data_index]
    b64_data = data_uri[data_index:]
    b64_data_len = len(b64_data)

    if b64_data_len % 4 != 0:
        msg1 = f'After Stripping {b64_data_prefix} found data of length {b64_data_len}'
        msg2 = 'Invalid base64 string length: must be a multiple of 4'
        msg = '\n'.join([msg1, msg2])
        raise ValueError(msg)  # Raise an error if the length is not a multiple of 4

    image_data = base64.b64decode(b64_data)
    image = Image.open(BytesIO(image_data))
    return pytesseract.image_to_string(image)