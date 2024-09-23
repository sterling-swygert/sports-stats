import logging
from urllib.parse import urljoin
import requests
from io import StringIO
import json
import logging
import time
from bs4 import BeautifulSoup
from bs4.element import Tag, ResultSet
import pandas as pd
import re
from typing import Dict, List, Tuple, Any

from pandas import DataFrame
from requests import HTTPError

from sports_stats.utils import util

HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US)'}

HOST = "https://pro-football-reference.com"

DIV_ID = "div_players"

BIO_KEYS = [
    "player_Id", "name", "position", "height", "weight", "team", "birthday", "college", "hometown", "home_state",
    "draft_pick", "draft_year"
]


class FootballReferenceScraper(object):
    def __init__(self):
        self.host = HOST
        self.headers = HEADERS
        self.div_id = DIV_ID
        self.bio_keys = BIO_KEYS

    def get_players_from_letter(self, letter: str) -> ResultSet:
        time.sleep(10)
        logging.info(f"Getting player links for letter {letter}...")
        url = self.host + "/players/" + letter
        page = requests.get(url, headers=self.headers)
        logging.info(f"Status code {page.status_code}")
        soup = BeautifulSoup(page.content, 'html.parser')
        player_result_list = soup.find("div", id=self.div_id).find_all("p")
        return player_result_list

    @staticmethod
    def get_player_record(player_tag: Tag) -> Dict:
        name = player_tag.find("a").text
        href = player_tag.find("a")["href"]
        positions = player_tag.text.replace(name, "").split(" ")[1].replace("(", "").replace(")", "").split("-")
        starting_year = player_tag.text.split(" ")[-1].split("-")[0].replace("(", "")
        final_year = player_tag.text.split(" ")[-1].split("-")[-1].replace(")", "")
        active = len(player_tag.find_all("b")) > 0
        base_data = dict()
        base_data['name'] = name
        base_data['href'] = href
        base_data['player_id'] = href.split('/')[-1].split('.')[0]
        base_data['starting_year'] = starting_year
        base_data['final_year'] = final_year
        base_data['active'] = active
        base_data['positions'] = positions
        return base_data

    def get_player_soup(self, href: str) -> BeautifulSoup:
        time.sleep(10)
        url = '/'.join([self.host, href])
        page = requests.get(url, headers=self.headers)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            return soup
        else:
            raise HTTPError(page.text, page.status_code)

    def get_player_bio(self, soup: BeautifulSoup, player_id: str) -> Dict:
        bio = {key: None for key in self.bio_keys}
        bio["player_id"] = player_id
        bio_soup = soup.find("div", attrs={"id": "meta"})
        bio['name'] = bio_soup.find('h1').text.strip()
        ps = bio_soup.find_all("p")
        for i, p in enumerate(ps):
            if "position:" in p.text.lower():
                bio["position"] = p.text.split(":")[1].split('\n')[0].strip()
            elif len(p.find_all("span")) > 1 and "-" in p.find_all("span")[0].text and "lb" in p.find_all("span")[1].text:
                bio["height"] = p.find_all("span")[0].text.strip()
                bio["weight"] = p.find_all("span")[1].text.strip()
            elif len(p.find_all("strong")) > 0 and p.find_all("strong")[0].text == "Team":
                bio["team"] = p.text.strip('Team: ')
            elif len(p.find_all("strong")) > 0 and p.find_all("strong")[0].text == "Born:":
                bio["birthday"] = p.find("span").attrs["data-birth"]
            elif len(p.find_all("strong")) > 0 and p.find_all("strong")[0].text == "College":
                a_s = p.find_all('a')
                for a in a_s:
                    a_href = a.get('href')
                    if a_href and a_href.startswith('/schools/'):
                        bio["college"] = a.text.strip()
            elif len(p.find_all("strong")) > 0 and p.find_all("strong")[0].text == "High School":
                bio["hometown"] = p.find_all("a")[0].text
                bio["home_state"] = p.find_all("a")[1].text
            elif len(p.find_all("strong")) > 0 and p.find_all("strong")[0].text == "Draft":
                try:
                    bio["draft_pick"] = re.sub(
                        "[a-z]*", "", re.sub(" overall", "", p.text.split(")")[0].split("(")[1])
                    )
                except IndexError:
                    bio["draft_pick"] = None
                bio["draft_year"] = p.find_all("a")[-1].text.split(" ")[0]
        return bio

    @staticmethod
    def get_player_tables(self, soup: BeautifulSoup, player_id: str, position: str) -> List[Dict[str, DataFrame]]:
        tables = soup.find_all("table")
        dfs = []
        for table in tables:
            table_df = pd.read_html(StringIO(str(table)))[0]
            table_df = util.clean_table(table_df)
            table_df["player_Id"] = player_id
            table_id = table["id"]
            if table_id == "stats":
                table_id = position + "-" + table_id
            dfs.append({"table_id": table_id, "table": table_df})
        return dfs
