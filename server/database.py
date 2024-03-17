import json

import psycopg2

from globals import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER


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
