from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd


# Uses a chrome driver to open prize picks
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://app.prizepicks.com/")

# Waits and closes the initial popup
wait = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[3]/div/div/div[3]/button")))
driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div/div[3]/button").click()
time.sleep(1)


nbaPlayers = []

# Goes to the NBA tab (Change NBA to the Sport you want to scrape)
driver.find_element(By.XPATH, "//div[@class='name'][normalize-space()='NBA']").click()
time.sleep(2)
stat_container = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".stat-container")))


# Fetches a list of all prop stat categories, example: Points
categories = driver.find_element(By.CSS_SELECTOR, ".stat-container").text.split("\n")

# Collecting categories
for category in categories:
    driver.find_element(By.XPATH, f"//div[text()='{category}']").click()

    projectionsPP = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".projection")))

    for projections in projectionsPP:
        names = projections.find_element(By.CLASS_NAME, "name").text
        pos = projections.find_element(By.CLASS_NAME, "team-position").text.split(' - ')[-1]
        pts = projections.find_element(By.CLASS_NAME, "presale-score").get_attribute("innerText")
        proptype = projections.find_element(By.CLASS_NAME, "text").get_attribute("innerText")

        players = {
            "Name": names,
            "Position": pos,
            "Stat": pts,
            "Prop": proptype.replace("<wbr>", "")
        }
        nbaPlayers.append(players)

ppProps = pd.DataFrame(nbaPlayers)

ppProps.to_csv('nba_props.csv', index=False)

