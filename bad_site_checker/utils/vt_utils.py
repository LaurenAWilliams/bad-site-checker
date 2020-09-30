"""
Utility to provide an interface for lookup up URLs on VirusTotal.
This is currently implemented using the free tier, so we're limited
to 4 lookups per minute.
"""

import json
import os
import time
from urllib import request, parse

from dotenv import load_dotenv

load_dotenv()

VT_API_KEY = os.getenv("VT_API_KEY")


def post_url_scan(query_string):
    """

    :param query_string: url we want to lookup
    :return: scan_id, status_code: scan id returned by virus total so we can
             lookup the scan later
    """
    url = "https://www.virustotal.com/vtapi/v2/url/scan"

    data_dict = {"apikey": VT_API_KEY, "url": query_string}
    data = parse.urlencode(data_dict).encode()
    req = request.Request(url=url, data=data)
    resp = request.urlopen(req)

    if resp.getcode() == 200:
        data = resp.read()
        decoded_data = json.loads(data)
        return decoded_data['scan_id'], 200
    else:
        return None, resp.getcode()


def get_url_scan_report(scan_id):
    """

    :param scan_id: scan id of previous scan we submitted
    :return: dict, status_code: success or failure response, with reasoning
    """
    url = "https://www.virustotal.com/vtapi/v2/url/report?apikey=%s&resource=%s"
    query_url = url % (VT_API_KEY, scan_id)
    resp = request.urlopen(query_url)
    failed_scans = dict()

    if resp.getcode() == 200:
        data = resp.read()
        decoded_data = json.loads(data)
        for _ in range(0, 5):
            if 'positives' in decoded_data:
                break
            time.sleep(1)
        else:
            return None, resp.getcode()
        if decoded_data['positives'] != 0:
            safe = False
            scans = decoded_data['scans']
            for scan in scans:
                if scans[scan]['detected']:
                    failed_scans[scan] = scans[scan]['result']
        else:
            safe = True

        return {
                   "safe": safe,
                   "details": failed_scans,
               }, 200

    else:
        return None, resp.getcode()
