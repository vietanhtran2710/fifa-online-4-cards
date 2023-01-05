import argparse
from os import system

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

parser = argparse.ArgumentParser(
                    prog = 'Get Single Player Data URL from a season',
                    description = 'This program retrieve all player\'s information link from one season and save to a links.txt file',
                    epilog = '')
parser.add_argument('--season', metavar='S', type=str, nargs='?',
                    help='an integer represent season value')
parser.add_argument('--maxovr', metavar='M', type=str, nargs='?', 
                    help='Maximum OVR stat of the players')
parser.add_argument('--name', metavar='N', type=str, nargs='?',
                    help='Name of the season')
args = parser.parse_args()

links_set = set()
URL_PREFIX = "https://fo4s.com/?class%5B%5D=" + args.season +"&sort=ovr-desc&ovr_max="

max_ovr = args.maxovr
while True:
    wait_for_element = 10  # wait timeout in seconds
    chrome = webdriver.Chrome()
    chrome.get(URL_PREFIX + max_ovr)

    try:
        WebDriverWait(chrome, wait_for_element).until(
            EC.presence_of_element_located((By.CLASS_NAME, "player-name")))
        source = chrome.page_source
        soup = BeautifulSoup(source, "html.parser")
        a_tags = soup.find_all("a", {"class": "player-name"})
        for item in a_tags:
            links_set.add(item["href"])
        if len(list(a_tags)) < 100:
            break
        last_row = list(soup.find_all("tr"))[-1]
        max_ovr = list(last_row.children)[4].text
        chrome.close()
    except TimeoutException as e:
        break

system("mkdir " + args.name)
data = []
for item in links_set:
    data.append(item + "\n")
with open("./" + args.name + "/links.txt", "w") as f:
    f.writelines(data)