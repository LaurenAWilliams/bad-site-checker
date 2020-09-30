"""
Database Class

Abstracts mysql interactions for storing and retrieving info about the specified URL.
"""

import json
import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()

INSERT_QUERY = """
INSERT INTO lookup (url, safe, details)
VALUES (%(url)s, %(safe)s, %(details)s)
"""

GET_URL_QUERY = """
SELECT * FROM lookup WHERE url=%(url)s
"""


class Database:
    def __init__(self):
        config = {
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASS"),
            "host": 'db',
            "port": '3306',
            "database": 'badsitechecker'
        }
        self.connection = mysql.connector.connect(**config)
        self.cursor = self.connection.cursor(dictionary=True)

    def fetch_by_url(self, url):
        """
        Check if url is already present in the db
        :param url: url we are searching for in the db
        :return: None if no url found, dict of values if found
        """
        self.cursor.execute(GET_URL_QUERY, {"url": url})
        fetched = self.cursor.fetchone()
        return fetched

    def push_data_from_report(self, url, report):
        """
        Insert url, whether it's safe and details about the scans into the db
        :param url: url we are inserting into the db
        :param report: report returned by VirusTotal
        :return: None
        """
        self.cursor.execute(
            INSERT_QUERY,
            {"url": url, "safe": report['safe'], "details": json.dumps(report['details'])}
        )
        self.connection.commit()
        self.cursor.close()
