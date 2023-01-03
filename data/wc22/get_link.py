import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

links_set = set()
URL_PREFIX = "https://fo4s.com/?class%5B%5D=1575&sort=ovr-desc&ovr_max="

max_ovr = "108"
while True:
    wait_for_element = 10  # wait timeout in seconds
    firefox = webdriver.Firefox()
    firefox.get(URL_PREFIX + max_ovr)

    try:
        WebDriverWait(firefox, wait_for_element).until(
            EC.presence_of_element_located((By.CLASS_NAME, "player-name")))
        source = firefox.page_source
        soup = BeautifulSoup(source, "html.parser")
        a_tags = soup.find_all("a", {"class": "player-name"})
        for item in a_tags:
            links_set.add(item["href"])
        if len(list(a_tags)) < 100:
            break
        last_row = list(soup.find_all("tr"))[-1]
        max_ovr = list(last_row.children)[4].text
        firefox.close()
    except TimeoutException as e:
        break

data = []
for item in links_set:
    data.append(item + "\n")
with open("links.txt", "w") as f:
    f.writelines(data)