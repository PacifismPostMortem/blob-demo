import os
import uuid

from azure.storage.blob import BlobServiceClient

connection_string = os.environ.get('BLOB_CONNECTION_STRING')
blob_container_name = os.environ.get('BLOB_CONTAINER_NAME')
blob_service_client = None


def setup():
    """ Sets up the blob service client and container client for the blob manager."""
    global blob_service_client, blob_container_name
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)


def upload_blob(file):
    """ :param file:
        :type file: File object from a POST request from an HTML form
        :returns: The blob url to access the file at, or None if failed
        :rtype: str or None if failed
    Uploads a blob to the container."""
    try:
        container_client = blob_service_client.get_container_client(blob_container_name)

        # must be unique from other blobs, adding the file extension from the filename
        # import for when someone downloads the blob, the extension will be correct
        blob_id = str(uuid.uuid4()) + file.filename.split('.')[-1]

        container_client.upload_blob(blob_id, file)
        blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{blob_container_name}/{blob_id}"
        return blob_url
    except Exception as e:
        print(e)
    return None


def delete_blob(blob_url):
    """ :param blob_url: The url of the blob to delete
        :type blob_url: str
        :returns: True or false for whether the blob was deleted successfully or not
        :rtype: bool
    Deletes a blob from the container."""
    global blob_service_client

    # parse the blob url by: https://<account_name>.blob.core.windows.net/<container_name>/<blob_name>
    split_url = blob_url.split('/')
    blob_name = split_url[-1]
    container_name = split_url[-2]

    try:
        container_client = blob_service_client.get_container_client(container_name)
        return container_client.delete_blob(blob_name)
    except Exception as e:
        print(e)
    return False
