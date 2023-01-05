from bs4 import BeautifulSoup
import requests
import argparse
from os import system

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
    return dom.xpath(xpath)[0].text

parser = argparse.ArgumentParser(
                    prog = 'Get All Single Player Data from a links file',
                    description = 'This program retrieve all player\'s information from a links.txt file',
                    epilog = '')
parser.add_argument('--name', metavar='N', type=str, nargs='?',
                    help='Name of the season')
args = parser.parse_args()

system("mkdir " + args.name + "/images")
links = []
players_data = []
with open("./" + args.name + "/links.txt", "r") as f:
    links = f.readlines()
for index, link in enumerate(links):
    player_data = {}
    chrome = webdriver.Chrome()
    chrome.get(link)
    player_data["season"] = "WC22"
    player_data["name"] = get_element_value(chrome.page_source, '//*[@id="player-info"]/div[1]/div[1]/span')
    player_data["main_position"] = get_element_value(chrome.page_source, '//*[@id="player-info"]/div[1]/div[2]/span[1]')
    player_data["country"] = get_element_value(chrome.page_source, '//*[@id="player-info"]/div[1]/div[3]/a/span')
    player_data["salary"] = get_element_value(chrome.page_source, '//*[@id="player-info"]/div[1]/div[4]/div[1]/div/div')

    soup = BeautifulSoup(chrome.page_source, "html.parser")
    img = soup.find("img", {"class": "img-fluid i-avatar"})
    img_src = img["src"]
    img_name = img_src.split("/")[-1].split("?")[0]
    with open("./" + args.name + "/images/" + img_name, "wb") as f:
        f.write(requests.get(img_src).content)
    player_data["image_name"] = img_name

    player_data["id"] = img_name.split(".")[0]

    player_data["stat"] = {}
    for level in range(1, 11):
        chrome.find_element(By.XPATH, "//*[@id=\"player-info\"]/div[2]/div/div[2]/div[3]/button").click()
        chrome.find_element(By.XPATH, "//*[@id=\"player-info\"]/div[2]/div/div[2]/div[3]/ul/li[" + str(level) + "]/a").click()
        player_data["stat"][level] = get_element_value(chrome.page_source, '//*[@id="player-info"]/div[1]/div[2]/span[2]')
    players_data.append(player_data)
    chrome.close()
    print(index, "/", len(links))

with open("./" + args.name + "/" + args.name +".json", "w", encoding='utf-8') as final:
   json.dump(players_data, final, indent=2, ensure_ascii=False)