"""
Functions to generate PDFs.
"""

# Build in

# PDF tools
from services.pdf.generator import PDFBuilder, PDFTypes


def get_mosine_gafete(qr_code: str, date: str) -> bytes:
    """Create the `gafete` PDF of passed angel.

    Params:
    -------
    - qr_code: str - QR code image in base64 str format.
    - name: str - Angel name.

    Return:
    -------
    - pdf: bytes - The pdf file.
    """
    gafete_vars = {"date": date, "qr_code": qr_code}
    pdf_builder = PDFBuilder(pdf_name=PDFTypes.GAFETE, pdf_vars=gafete_vars)
    pdf = pdf_builder.build()
    return pdf
