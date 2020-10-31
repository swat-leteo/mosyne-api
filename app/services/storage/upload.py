"""
Google Cloud storage uploads functions.
"""

# Built in
import base64
import os
from datetime import datetime
from uuid import uuid4

# Utils
import six

# Settings
from config import settings
from fastapi import HTTPException, status
from google.cloud.exceptions import ClientError

# GCP storage bucker
from .connection import get_gcp_bucket

######################
# Auxiliar Functions #
######################


def _check_extension(extension: str) -> None:
    """Check if the extension is allowed.
    If not, raise a bad request exception.

    Params:
    -------
    - extension: str - The file extension.
    """

    if extension not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Extension not allowed.",
        )


def _unique_filename(filename: str) -> str:
    """Generates a unique filename that is unlikely
    to collide with existing objects in Google Cloud Storage.

    Params:
    -------
    - filename: str - The current filename.

    Return:
    -------
    - filename: str - A unique filename.
    """
    date = datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
    basename, extension = filename.rsplit(".", 1)
    return "{0}-{1}-{2}.{3}".format(basename, date, str(uuid4()), extension)


#####################
# Storage Functions #
#####################


def upload_file(file_base64: str) -> str:
    """Uploads a file to the given Cloud Storage bucket
    and returns the public url to the new object.

    Params:
    -------
    - file_base64: str - The file to upload encoded in base 64 format.

    Return:
    -------
    url: str - The file public url.
    """

    # Get metada according to type file.
    metadata_and_image = file_base64.split(";base64,")
    content_type = metadata_and_image[0].split(":")[1]
    file_data = base64.b64decode(metadata_and_image[1])
    ext = content_type.split("/")[1]
    filename = f"mosyne-avatar.{ext}"

    # Pre upload actions.
    _check_extension(ext)
    filename = _unique_filename(filename)

    bucket = get_gcp_bucket()

    try:
        blob = bucket.blob(filename)
        blob.upload_from_string(file_data, content_type=content_type)
        url = blob.public_url
    except ClientError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error",
        )

    if isinstance(url, six.binary_type):
        url = url.decode("utf-8")
    return url


def get_or_update_image(encoded_image_or_url: str) -> str:
    """Return the image URL.

    If the passed string is a encoded image, upload the file, and
    return the url, else return the url string.

    Params:
    ------
    - encoded_image_or_url: str - The encoded image or a image url

    Return:
    ------
    - url: str - The url to image.
    """
    if encoded_image_or_url.startswith("https://"):
        # The image is a already a URL.
        return encoded_image_or_url

    # First the file is upload, then the generated url is returned.
    url = upload_file(file_base64=encoded_image_or_url)
    return url
