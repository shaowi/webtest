import requests
from flask import jsonify, request

from database import store_data_in_database
from globals import API_KEY

MAX_FILE_SIZE = 32 * 1024 * 1024  # 32MB


def handle_upload_file():
    def get_analysis_data(self_url):
        response = requests.get(self_url, headers={"x-apikey": API_KEY})
        return response.json()

    # Check if the POST request has the file part
    if "file" not in request.files:
        return False, "No file part", 400

    file = request.files["file"]

    # Check if the file is empty
    if file.filename == "":
        return False, "No selected file", 400

    # Check if the file is too large
    if file.content_length > MAX_FILE_SIZE:
        return False, "File is too large", 400

    # Process the file by making a POST request to the VirusTotal API
    files = {"file": (file.filename, file.stream)}
    headers = {"accept": "application/json", "x-apikey": API_KEY}
    response = requests.post(
        "https://www.virustotal.com/api/v3/files", files=files, headers=headers
    )

    # Check if the API request was successful
    if response.status_code == 200:
        # Get the analysis data and store it in the database
        api_response = response.json()
        analysis_data = get_analysis_data(api_response["data"]["links"]["self"])
        store_data_in_database(file.filename, analysis_data)
        return True, f"{file.filename}\n{analysis_data}", 200
    else:
        return False, "Failed to process file", 500
