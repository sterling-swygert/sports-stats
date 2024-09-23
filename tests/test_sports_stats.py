#!/usr/bin/env python

"""Tests for `sports_stats` package."""

import pytest

from sports_stats import sports_stats


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    import requests
    return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    from bs4 import BeautifulSoup
    assert 'GitHub' in BeautifulSoup(response.content, features="html.parser").title.string
