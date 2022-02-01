from __future__ import annotations
import pytest
import logging

from infra.report_utils import add_image

log = logging.getLogger('tests')


@pytest.mark.component("agent")
@pytest.mark.os("linux")
def test_admin_connects_via(step, admin, network, agent):
    """
    Given agent is authenticated
    And the server is configured
    When the agent connects to the network
    Then the connection to host perimeter81.com is successful
    """
    with step("Given agent is authenticated"):
        agent.auth("tenant", admin.email)

    with step("And the server is configured"):
        agent.config().switch_protocol_to("http")

    with step("When the agent connects to the network"):
        agent.connect(network)

    with step("Then the connection to host perimeter81.com is successful"):
        add_image('Important image', 'resources/startrooper.png')
        assert agent.resolve_host('perimeter81.com').has_succeeded


@pytest.mark.component("agent")
@pytest.mark.os("windows")
def test_admin_failed_to_connect_via(step, admin, network, agent):
    """
    Given agent is authenticated
    And the server is configured
    When the agent connects to the network
    Then the connection to host perimeter81.com is successful
    """
    with step("Given agent is authenticated"):
        agent.auth("tenant", admin.email)

    with step("And the server is configured"):
        agent.config().switch_protocol_to("http")

    with step("When the agent connects to the network"):
        agent.connect(network)

    with step("Then the connection to host perimeter81.com is successful"):
        add_image('Important image', 'resources/startrooper.png')
        assert not agent.resolve_host('perimeter81.com').has_succeeded
