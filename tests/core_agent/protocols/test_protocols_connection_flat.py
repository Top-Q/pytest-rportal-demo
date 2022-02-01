from __future__ import annotations
import pytest
import logging

from infra.report_utils import add_image

log = logging.getLogger('tests')


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
    add_image('Important image', 'resources/startrooper.png')
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
    add_image('Important image', 'resources/startrooper.png')
    assert not agent.resolve_host('perimeter81.com').has_succeeded
