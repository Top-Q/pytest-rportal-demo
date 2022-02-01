import logging

import pytest

from infra.component import Agent, ApiMember

log = logging.getLogger('conftest')


@pytest.fixture
def admin() -> ApiMember:
    return ApiMember()


class ApiNetwork:
    def __init__(self):
        self.network = "someNetwork"

    def __str__(self):
        return self.network


@pytest.fixture
def agent() -> Agent:
    return Agent()


@pytest.fixture
def network(step) -> ApiNetwork:
    return ApiNetwork()
