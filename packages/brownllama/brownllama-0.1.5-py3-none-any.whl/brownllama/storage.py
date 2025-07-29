"""
Storage utilities for Cloud Storage operations.

This module provides a class for interacting with Google Cloud Storage.
"""

from __future__ import annotations

import json
import tempfile
import uuid
from pathlib import Path

import pandas as pd
from google.cloud import storage
from google.cloud.exceptions import GoogleCloudError, NotFound

from brownllama.logger import get_logger

logger = get_logger(__name__)


class StorageController:
    """
    Google Cloud Storage manager for staging data.

    Attributes:
        project_id (str): Google Cloud project ID
        bucket_name (str): Cloud Storage bucket name

    """

    def __init__(
        self,
        project_id: str,
        bucket_name: str | None,
    ) -> None:
        """
        Initialize the Cloud Storage client and get or create the bucket.

        Args:
            project_id: Google Cloud project ID
            bucket_name: Cloud Storage bucket name

        """
        self.project_id = project_id
        self.bucket_name = bucket_name

        # Initialize the Storage client
        self.storage_client = storage.Client(
            project=self.project_id,
        )

        # Get or create the bucket
        try:
            self.bucket = self.storage_client.get_bucket(bucket_name)

        except NotFound:
            self.bucket = self.storage_client.create_bucket(bucket_name)
            logger.info(f"{'=' * 10} Created new bucket: {bucket_name} {'=' * 10}")

    def upload_to_gcs(
        self, data: dict | list[dict] | pd.DataFrame, prefix: str = "data"
    ) -> str:
        """
        Upload data to Google Cloud Storage.

        Args:
            data (Union[dict, list[dict], pd.DataFrame]): Data to upload (dict, list of dicts, or pandas DataFrame).
            prefix (str): Prefix for the filename in GCS. Defaults to "data".

        Returns:
            str: URI of the uploaded file in GCS.

        Raises:
            Exception: If an error occurs during the upload process.

        """
        logger.debug(f"{'=' * 10} Exporting data to GCS {'=' * 10}")
        temp_file_path: Path | None = None
        # Generate a unique filename
        filename = f"{prefix}_{uuid.uuid4().hex}.json"

        # Convert data to a pandas DataFrame if it's not already
        if isinstance(data, (dict, list)):
            dataframe_data = (
                pd.DataFrame(data) if isinstance(data, list) else pd.DataFrame([data])
            )
        else:
            dataframe_data = data

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                delete=False,
                suffix=".json",
                encoding="utf-8",
            ) as temp_file:
                dataframe_data.to_json(temp_file.name, orient="records", lines=True)
                temp_file_path = Path(temp_file.name)  # Changed to Path object

            # Upload the file to GCS
            blob = self.bucket.blob(filename)
            blob.upload_from_filename(temp_file_path)

            # Log success
            logger.info(
                f"Successfully uploaded data to gs://{self.bucket_name}/{filename}"
            )

        except Exception:
            logger.exception("Error uploading to GCS.")
            raise

        else:
            return f"gs://{self.bucket_name}/{filename}"

        finally:
            # Clean up the temporary file
            if temp_file_path and temp_file_path.exists():
                temp_file_path.unlink()

    def download_from_gcs(self, file_path: str | None, file_name: str) -> dict:
        """
        Download data from Google Cloud Storage and return it as a pandas DataFrame.

        Args:
            file_path (str): Path of the file in GCS to download.
            file_name (str): Name of the file to download.

        Returns:
            dict: Data parsed from the downloaded file.

        Raises:
            FileNotFoundError: If the file is not found in GCS.
            GoogleCloudError: If a Google Cloud related error occurs.
            Exception: If an error occurs during the download process or data parsing.

        """
        logger.debug(f"{'=' * 10} Downloading data from GCS {'=' * 10}")
        temp_file_path: Path | None = None

        try:
            blob_name = (
                f"{file_path.rstrip('/')}/{file_name}" if file_path else file_name
            )

            blob = self.bucket.blob(blob_name)

            # Check if the blob exists
            if not blob.exists():
                error_message = f"File not found in GCS: {file_name}"
                raise FileNotFoundError(error_message)

            with tempfile.NamedTemporaryFile(
                mode="wb", delete=False, encoding=None
            ) as temp_file:
                blob.download_to_file(temp_file)
                temp_file_path = Path(temp_file.name)

            # Read the data into a pandas DataFrame
            dataframe_data = pd.read_csv(temp_file_path, encoding="utf-16")

            # Convert dataframe to JSON String
            json_data = dataframe_data.to_json(orient="records")
            return json.loads(json_data)

        except NotFound as e:
            error_message = f"File not found in GCS: {file_name}"
            raise FileNotFoundError(error_message) from e
        except GoogleCloudError:
            logger.exception(f"Google Cloud error downloading file {file_name}.")
            raise
        except Exception:
            logger.exception(
                f"An unexpected error occurred while downloading or parsing file {file_name}."
            )
            raise

        # Clean up the temporary file
        finally:
            if temp_file_path and temp_file_path.exists():
                temp_file_path.unlink()

    def delete_file(self, gcs_uri: str) -> None:
        """
        Delete a file from Google Cloud Storage.

        Args:
            gcs_uri: URI of the file in GCS to delete

        """
        logger.debug(f"{'=' * 10} Deleting data from GCS {'=' * 10}")
        try:
            # Extract blob name from URI
            blob_name = gcs_uri.replace(f"gs://{self.bucket_name}/", "")

            # Delete the blob
            self.bucket.blob(blob_name).delete()
            logger.info(f"Deleted file: {gcs_uri}")

        except NotFound:
            # File not found is often acceptable for cleanup operations
            logger.warning(
                f"File not found during deletion: {gcs_uri}. It may have already been deleted."
            )
        except GoogleCloudError:
            # Catch other Google Cloud related errors
            logger.exception(f"Google Cloud error deleting file {gcs_uri}.")
        except Exception:
            # Catch any other unexpected exceptions.
            logger.exception(
                f"An unexpected error occurred while deleting file {gcs_uri}."
            )
