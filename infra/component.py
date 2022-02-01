import logging

from infra.report_utils import add_file

log = logging.getLogger('components')


class ApiMember:

    def __init__(self):
        self.email = "foo@bar.com"


class Config:

    def switch_protocol_to(self, protocol):
        log.debug(f"Switching protocol to {protocol}")
        add_file("Configuration File", "agent.conf", "foo=bar\nfoo1=bar1\nfoo2=bar2")


class HostConnection:

    def __init__(self):
        self.has_succeeded = True


class Agent:

    def auth(self, tenant, email):
        log.debug(f"Connecting {tenant} with email {email}")
        log.debug("Request json")

    def resolve_host(self, host):
        log.debug(f'Resolving host {host}')
        return HostConnection()

    def config(self):
        return Config()

    def connect(self, network):
        log.info(f"Connecting to network {network}")
        data = """
        {
  "id": 0,
  "category": {
    "id": 0,
    "name": "string"
  },
  "name": "doggie",
  "photoUrls": [
    "string"
  ],
  "tags": [
    {
      "id": 0,
      "name": "string"
    }
  ],
  "status": "available"
}"""
        add_file('request', 'request.json', data, 'application/json')
