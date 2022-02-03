from dataclasses import dataclass, field
import datetime
import random

import config


class Probe:
    def __init__(self):
        self.name = "probe"
        self.headers = {
            "user-agent": random.choice(config.user_agents)
        }

    def probe_username(self, username):
        raise NotImplementedError()

    def probe_mobilenumber(self, mobile_number):
        raise NotImplementedError()

    def probe_emailaddress(self, email_address):
        raise NotImplementedError()


class UnexpectedHTTPResponse(BaseException):
    def __init__(self, message):
        super().__init__(message)


class IdType:
    PHONE = "phone"
    EMAIL = "email"
    USERNAME = "username"


@dataclass
class ErrorResult:
    message: str
    status: str = "error"


@dataclass
class ProbeResult:
    source: str
    url: str
    timestamp: datetime.datetime
    id_checked: str
    id_found: bool
    other_data: dict = field(default_factory=dict)
    status: str = "success"
