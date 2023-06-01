import os
from azure.storage.blob import BlobServiceClient

def uploadToBlobStorage():
    storage_account_key = os.environ.get('STORAGE_ACCOUNT_KEY')
    storage_account_name = os.environ.get('STORAGE_ACCOUNT_NAME')
    connection_string = os.environ.get('CONNECTION_STRING')
    container_name = os.environ.get('CONTAINER_NAME')
    file_path = './report.pdf' # Since the file is in the root, we can use './' to indicate the current directory
    file_name = 'report.pdf'

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container_name, file_name)

    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)

if __name__ == "__main__":
    uploadToBlobStorage()
