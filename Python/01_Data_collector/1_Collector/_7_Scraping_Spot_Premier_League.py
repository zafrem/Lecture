# pip install selenium webdriver-manager
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_keyword():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    url = 'https://www.premierleague.com/'
    return_message = ''

    driver.get(url)

    try:
        time.sleep(10)
        elements = driver.find_elements(By.XPATH,
                                        '/html/body/main/div/section/div[1]/div[3]/div[1]/div/time')
        if 0 == len(elements):
            elements = driver.find_elements(By.XPATH,
                                        '/html/body/main/div[5]/div/nav/div[2]/div[1]/div/time')
        if 0 == len(elements):
            elements = driver.find_elements(By.XPATH,
                                        '/html/body/main/div[4]/div/nav/div[2]/div[1]/div/time')

        for idx, title in enumerate(elements, 1):
            print(idx, title.text)
            scores = driver.find_elements(By.XPATH,
                                         f'/html/body/main/div/section/div[1]/div[3]/div[1]/div[{str(idx)}]/a/span')
            if 0 == len(scores):
                scores = driver.find_elements(By.XPATH,
                                              f'/html/body/main/div[5]/div/nav/div[2]/div[1]/div[{str(idx)}]/a/span')
            upcoming = driver.find_elements(By.XPATH,
                                         f'/html/body/main/div/section/div[1]/div[3]/div[1]/div[{str(idx)}]/a/time')
            if 0 == len(upcoming):
                upcoming = driver.find_elements(By.XPATH,
                                         f'/html/body/main/div[5]/div/nav/div[2]/div[1]/div[{str(idx)}]/a/time')
            times = scores + upcoming
            team1s = driver.find_elements(By.XPATH,
                                         f'/html/body/main/div/section/div[1]/div[3]/div[1]/div[{str(idx)}]/a/div[1]')
            if 0 == len(team1s):
                team1s = driver.find_elements(By.XPATH,
                                              f'/html/body/main/div[5]/div/nav/div[2]/div[1]/div[{str(idx)}]/a/div[1]')
            team2s = driver.find_elements(By.XPATH,
                                          f'/html/body/main/div/section/div[1]/div[3]/div[1]/div[{str(idx)}]/a/div[2]')
            if 0 == len(team2s):
                team2s = driver.find_elements(By.XPATH,
                                              f'/html/body/main/div[5]/div/nav/div[2]/div[1]/div[{str(idx)}]/a/div[2]')
            print(len(times), len(team1s), len(team2s))
            for _time, _team1, _team2 in zip(times, team1s, team2s):
                _temp = _time.text.replace('\n', '')
                print(f"""{title.text} \t {_temp} : {_team1.text} vs {_team2.text}""")
                return_message += f"""{title.text} \t {_temp} : {_team1.text} vs {_team2.text}\n"""

    except Exception as e:
        print(f"Error : {e}")

    driver.quit()

    return return_message


if __name__ == "__main__":
    print(get_keyword())
