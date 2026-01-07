# Key input : Los Angeles, California, United States
# Temp XPath : /html/body/span/div/span/div/div[2]/div[2]/div/div[1]/table/tbody/tr[6]/td[1]

# pip install selenium webdriver-manager
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def get_keyword():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    return_message = ''
    url = 'https://embed.windy.com/config/forecast'
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            # Wait loading element
            EC.presence_of_element_located((By.XPATH,
                                            '/html/body/div/main/div/section[1]/section/section[1]/div/div['
                                            '2]/div/div[1]/span/input')),
        )

        driver.find_element(By.XPATH,
                            '/html/body/div/main/div/section[1]/section/section[1]/div/div[2]/div/div[1]/span/input'
                            ).send_keys('Los Angeles, California, United States')

        driver.find_element(By.XPATH,
                            '/html/body/div/main/div/section[1]/section/section[1]/div/div[2]/div/div[1]/span/input'
                            ).send_keys(Keys.ARROW_DOWN, Keys.RETURN)

        frame = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(frame)

        WebDriverWait(driver, 10).until(
            # Wait loading element
            EC.presence_of_element_located((By.XPATH,
                                            '/html/body/span/div/span/div/div[2]/div[2]/div/div[1]/table/tbody/tr['
                                            '2]/td[1]')),
        )

        times = driver.find_elements(By.XPATH,
                                     '/html/body/span/div/span/div/div[2]/div[2]/div/div[1]/table/tbody/tr[2]/td')
        temps = driver.find_elements(By.XPATH,
                                     '/html/body/span/div/span/div/div[2]/div[2]/div/div[1]/table/tbody/tr[4]/td')
        windy = driver.find_elements(By.XPATH,
                                      '/html/body/span/div/span/div/div[2]/div[2]/div/div[1]/table/tbody/tr[6]/td')

        for _time, _temp, _windy in zip(times, temps, windy):
            return_message += f"Time : {_time.text}, \tTemperature : {_temp.text}, \tWindy : {_windy.text}\n"
            print(f"Time : {_time.text}, \tTemperature : {_temp.text}, \tWindy : {_windy.text}")

    except Exception as e:
        print(f"Error : {e}")

    driver.quit()
    return return_message

if __name__ == "__main__":
    print(get_keyword())
