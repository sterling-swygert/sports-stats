
"""Tests for `sports_stats` package."""
import pytest
import pickle
import bs4
from bs4 import BeautifulSoup
from requests import HTTPError

from sports_stats.stat_scraping import football_scraping


@pytest.fixture
def scraper():
    return football_scraping.FootballReferenceScraper()


@pytest.fixture
def player_result_set(scraper):
    return scraper.get_players_from_letter('A')


@pytest.fixture
def josh_allen_tag():
    with open('tests/resources/JoshAllenTag.pkl', 'rb') as f:
        str_soup = pickle.load(f)
        return BeautifulSoup(str_soup, 'lxml').find('p')


@pytest.fixture
def josh_allen_soup(scraper):
    with open('tests/resources/JoshAllenSoup.pkl', 'rb') as f:
        str_soup = pickle.load(f)
        return BeautifulSoup(str_soup, 'lxml')


def test_get_player_soup_pos(scraper):
    soup = scraper.get_player_soup('/players/A/AlleJo02.htm')
    assert type(soup) == bs4.BeautifulSoup


def test_get_player_soup_raises(scraper):
    with pytest.raises(HTTPError):
        scraper.get_player_soup('/players/A/BlleJo02.htm')


def test_get_player_bio(scraper, josh_allen_soup):
    bio = scraper.get_player_bio(josh_allen_soup, 'AlleJo02')
    assert bio['name'] == 'Josh Allen'
    assert bio['position'] == 'QB'
    assert bio['height'] == '6-5'
    assert bio['weight'] == '237lb'
    assert bio['team'] == 'Buffalo Bills'
    assert bio['birthday'] == '1996-05-21'
    assert bio['college'] == 'Wyoming'
    assert bio['hometown'] == 'Firebaugh'
    assert bio['home_state'] == 'CA'
    assert bio['draft_pick'] == '7'


def test_get_player_record(scraper, josh_allen_tag):
    player_data = scraper.get_player_record(josh_allen_tag)
    assert player_data['name'] == 'Josh Allen'
    assert player_data['href'] == '/players/A/AlleJo02.htm'
    assert player_data['player_id'] == 'AlleJo02'
    assert player_data['starting_year'] == '2018'
    assert player_data['final_year'] == '2023'
    assert player_data['positions'] == ['QB']


def test_get_players(player_result_set):
    assert type(player_result_set) == bs4.element.ResultSet
    assert type(player_result_set[0]) == bs4.element.Tag






