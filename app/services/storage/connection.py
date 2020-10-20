"""
Google Cloud Storage connection.
"""

# Settings
from config import settings

# Exceptions
from fastapi import HTTPException, status

# Cloud storage
from google.cloud import storage
from google.cloud.exceptions import GoogleCloudError


def get_gcp_bucket() -> any:
    """Connect with a GCP bucket and return the api instance.

    Return:
    -------
    - bucket: - The gcp bucket instance.
    """
    bucket_name = settings.GOOGLE_STORAGE_BUCKET

    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name=bucket_name)
    except GoogleCloudError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server error"
        )
    return bucket
