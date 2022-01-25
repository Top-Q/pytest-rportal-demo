from __future__ import annotations
import pytest
import logging

log = logging.getLogger('tests')

class ApiMember:

    def __init__(self):
        self.email = "foo@bar.com"

@pytest.fixture
def admin() -> ApiMember:
    return ApiMember()


class ApiNetwork:
    def __init__(self):
        self.network = "someNetwork"

    def __str__(self):
        return self.network

@pytest.fixture
def network() -> ApiNetwork:
    log.info("Given network is set")
    log.debug("Doing all kind of things")
    return ApiNetwork()


class Config:

    def switch_protocol_to(self, protocol):
        log.debug(f"Switching protocol to {protocol}")
        log.debug(
            "Configuration File",
            attachment={
                "name": "agent.conf",
                "data": "foo=bar\nfoo1=bar1\nfoo2=bar2",
                "mime": "application/octet-stream",
            },
        )

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
        log.debug(
            "Request",
            attachment={
                "name": "request.json",
                "data": """
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
}""",
                "mime": "application/json",
            },
        )


@pytest.fixture
def agent() -> Agent:
    return Agent()


@pytest.mark.component("web")
@pytest.mark.os("linux")
def test_admin_connects_via(admin, network, agent):
    """
    Given agent is authenticated
    And the server is configured
    When the agent connects to the network
    Then the connection to host perimeter81.com is successful
    """
    log.info("And agent is authenticated")
    agent.auth("tenant", admin.email)

    log.info("And the server is configured")
    agent.config().switch_protocol_to("http")

    log.info("When the agent connects to the network")
    agent.connect(network)

    log.info("Then the connection to host perimeter81.com is successful")
    assert agent.resolve_host('perimeter81.com').has_succeeded


@pytest.mark.component("web")
@pytest.mark.os("windows")
def test_admin_failed_to_connect_via(admin, network, agent):
    """
    Given agent is authenticated
    And the server is configured
    When the agent connects to the network
    Then the connection to host perimeter81.com is successful
    """
    log.info("Given agent is authenticated")
    agent.auth("tenant", admin.email)

    log.info("And the server is configured")
    agent.config().switch_protocol_to("http")

    log.info("When the agent connects to the network")
    agent.connect(network)

    log.info("Then the connection to host perimeter81.com is successful")
    assert not agent.resolve_host('perimeter81.com').has_succeeded
