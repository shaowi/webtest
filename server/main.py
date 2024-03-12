import json
import os
from flask import Flask, request, jsonify
import requests
import psycopg2
from dotenv import load_dotenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes

# Load environment variables from .env file
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
API_KEY = os.getenv("API_KEY")


# Endpoint for uploading files
@app.route("/upload", methods=["POST"])
def upload_file():
    # Check if the POST request has the file part
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

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
        return response.text
    else:
        return jsonify({"error": "Failed to process file"}), 500


def get_analysis_data(self_url):
    response = requests.get(self_url, headers={"x-apikey": API_KEY})
    return response.json()


def store_data_in_database(filename, api_response):
    with psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    ) as conn:

        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO files (filename, api_response) VALUES (%s, %s)",
                (filename, json.dumps(api_response)),
            )

        conn.commit()


def create_database():
    with psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST
    ) as conn:

        with conn.cursor() as cursor:
            # Drop the table if it already exists and create a new one
            cursor.execute("DROP TABLE IF EXISTS files")
            cursor.execute(
                """
				CREATE TABLE IF NOT EXISTS files (
					id SERIAL PRIMARY KEY,
					filename TEXT,
					api_response JSONB
				)
				"""
            )

        conn.commit()

    print("Database and table created successfully!")


if __name__ == "__main__":
    create_database()
    app.run(debug=True)
