"""
Class PDF generator.
"""

# Build in
import os
from enum import Enum
from string import Template
from typing import Dict, Union

# PDF
import pdfkit

# Template location.
pdf_dir = f"{os.getcwd()}/services/pdf"


class PDFTypes(str, Enum):
    """Define the available pdf names.

    Each enum correspond with an available template in
    templates folder.
    """

    GAFETE = "gafete"


class PDFBuilder:
    """Pdf builder class."""

    def __init__(
        self, pdf_name: PDFTypes, pdf_vars: Dict[str, Union[str, int]]
    ) -> None:
        """PDF builder instance.

        Params:
        -------
        - pdf_name: PDFTypes - The desired template.
        - pdf_vars: dict - A dict with the vars to substitu in the template.
        """
        self.pdf_name = pdf_name
        self.pdf_vars = pdf_vars
        self.templates_dir = f"{pdf_dir}/templates"
        self.tmp_dir = f"{pdf_dir}/tmp"
        self.get_template()

    def get_template(self) -> None:
        """Get the desired template and susbstitu the required vars."""
        with open(f"{self.templates_dir}/{self.pdf_name}.html") as f:
            self.html_str = f.read()

        self.template = Template(self.html_str)
        self.template = self.template.substitute(**self.pdf_vars)

    def build(self) -> str:
        """Creates a PDF file and return it.

        Return:
        -------
        - path: str - The path to pdf file.
        """
        options = {
            "page-size": "Letter",
            "margin-top": "0.75in",
            "margin-right": "0.75in",
            "margin-bottom": "0.75in",
            "margin-left": "0.75in",
            "encoding": "UTF-8",
            "no-outline": None,
        }

        self.path = f"{self.tmp_dir}/{PDFTypes.GAFETE}.pdf"

        self.pdf = pdfkit.from_string(
            self.template,
            self.path,
            css=f"{self.templates_dir}/{PDFTypes.GAFETE}.css",
            options=options,
        )
        return self.path
