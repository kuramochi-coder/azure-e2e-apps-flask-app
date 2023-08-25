""" Backend service for azure blob storage """
#  backend.py
# pylint: disable=import-error

from flask import Flask, request
from flask_cors import CORS

from azure.storage.blob import (
    BlobClient,
)

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    """Healthcheck endpoint"""

    return "Ok!"


@app.route("/api/files", methods=["POST"])
def upload_files():
    """Uploads a file to azure blob storage via a post request endpoint"""

    # Get the file from post request
    image_file = request.files.get("file", "")
    # Get the sas token url from post request
    sas_token_url = request.form.get("sasTokenUrl", "")

    # Upload the file to azure blob storage
    upload_blob_stream(sas_token_url, image_file.stream)

    # Return the file name and status
    return {"filename": image_file.filename, "status": "success"}


def upload_blob_stream(sas_token_url: str, file_stream):
    """Function to upload a file to azure blob storage"""

    blob_client = BlobClient.from_blob_url(sas_token_url)
    blob_client.upload_blob(file_stream, blob_type="BlockBlob")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8999)
