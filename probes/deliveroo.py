import logging

import core
from core import ProbeResult, Probe, IdType
import datetime

import requests

log = logging.getLogger(__name__)


def get_probe():
    return Deliveroo()


class Deliveroo(Probe):
    def __init__(self):
        super().__init__()
        self.name = "Deliveroo"

    def probe_username(self, username):
        self.probe_emailaddress(username)

    def probe_emailaddress(self, email_address):
        url = "https://consumer-ow-api.deliveroo.com/orderapp/v2/check-email"
        log.info(f"Requesting {url}")
        resp = requests.get(url, headers=self.headers)
        log.info(f"Response received:\n{resp.text}")
        if resp.status_code == 200:
            result = ProbeResult(self.name, url, datetime.datetime.now(), IdType.EMAIL, True)
        elif resp.status_code == 404:
            result = ProbeResult(self.name, url, datetime.datetime.now(), IdType.EMAIL, False)
        else:
            raise core.UnexpectedHTTPResponse(resp.text)
        return result