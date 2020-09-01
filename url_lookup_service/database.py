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
            "database": 'urllookupservice'
        }
        self.connection = mysql.connector.connect(**config)
        self.cursor = self.connection.cursor(dictionary=True)

    def fetch_by_url(self, url):
        self.cursor.execute(GET_URL_QUERY, {"url": url})
        fetched = self.cursor.fetchone()
        return fetched

    def push_data_from_report(self, url, report):
        self.cursor.execute(
            INSERT_QUERY,
            {"url": url, "safe": report['safe'], "details": json.dumps(report['details'])}
        )
        self.connection.commit()
        self.cursor.close()
