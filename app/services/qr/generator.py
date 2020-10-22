"""
QR code generator.
"""

# Qr tools
from pyqrcode import QRCode


def _create_qr_base64(content: str) -> str:
    """Create a base64 valid str format to render in html with
    the passed content.

    Params:
    -------
    - content: str - The info to encode.

    Return:
    -------
    - qr_code: Encoded QR code.
    """
    qr_instance = QRCode(content)
    qr_srt_base64 = qr_instance.png_as_base64_str(scale=8)
    qr_code = f"data:image/png;base64,{qr_srt_base64}"
    return qr_code


def generate_qr_base64_web(url: str) -> str:
    """Generate a qr code with content passed in base 64 format.
    The resulted qr redirect to the passed url when is scaned.

    Params:
    -------
    - url: str - The url to redirect.

    Return:
    -------
    - qr_code: str - Encode in base64 QR code image.
    """
    if not url.startswith("https://"):
        raise Exception("A valid url is needed")

    return _create_qr_base64(url)


def generate_qr_base64_contact(
    firstname: str, lastname: str, cel: str, angel_url_profile: str
) -> str:
    """Generate a qr code with content passed in base 64 format.
    The resulted qr create the contact in user phone when is scaned.

    Params:
    -------
    - firstname: str - The guardian firstname.
    - lastname: str - The guardian lastname.
    - cel: str - The guardian cel.
    - angel_url_profile: str - The angel profile_url.

    Return:
    -------
    - qr_code: str - Encode in base64 QR code image.
    """
    cel_str = cel
    if cel_str.startswith("+"):
        cel_str = cel_str[1:]
    try:
        int(cel_str)
    except ValueError:
        raise Exception("Enter valid number")

    me_card = f"MECARD:N:{lastname},{firstname};TEL:{cel};URL:{angel_url_profile};;"
    return _create_qr_base64(me_card)
