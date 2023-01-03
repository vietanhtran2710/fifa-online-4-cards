from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from lxml import etree

import json

def get_element_value(source, xpath):
    soup = BeautifulSoup(source, "html.parser")
    dom = etree.HTML(str(soup))
    print(dom.xpath(xpath)[0])
    return dom.xpath(xpath)[0].text

links = []
players_data = []
with open("links.txt", "r") as f:
    links = f.readlines()
for link in links:
    player_data = {}
    firefox = webdriver.Firefox()
    firefox.get(link)
    player_data["season"] = "WC22"
    player_data["name"] = get_element_value(firefox.page_source, '//*[@id="player-info"]/div[1]/div[1]/span')
    player_data["main_position"] = get_element_value(firefox.page_source, '//*[@id="player-info"]/div[1]/div[2]/span[1]')
    player_data["country"] = get_element_value(firefox.page_source, '//*[@id="player-info"]/div[1]/div[3]/a/span')
    player_data["salary"] = get_element_value(firefox.page_source, '//*[@id="player-info"]/div[1]/div[4]/div[1]/div/div')

    soup = BeautifulSoup(firefox.page_source, "html.parser")
    img = soup.find("img", {"class": "img-fluid i-avatar"})
    img_src = img["src"]
    img_name = img_src.split("/")[-1].split("?")[0]
    with open("./images/" + img_name, "wb") as f:
        f.write(requests.get(img_src).content)
    player_data["image_name"] = img_name

    player_data["stat"] = {}
    for level in range(1, 11):
        firefox.find_element(By.XPATH, "//*[@id=\"player-info\"]/div[2]/div/div[2]/div[3]/button").click()
        firefox.find_element(By.XPATH, "//*[@id=\"player-info\"]/div[2]/div/div[2]/div[3]/ul/li[" + str(level) + "]/a").click()
        player_data["stat"][level] = get_element_value(firefox.page_source, '//*[@id="player-info"]/div[1]/div[2]/span[2]')
    players_data.append(player_data)
    firefox.close()

with open("wc22.json", "w") as final:
   json.dump(players_data, final, indent=2)