from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time, pandas as pd , math , csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

# Setup Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-notifications")
chrome_options.binary_location = "/usr/bin/google-chrome"
chrome_options.add_argument("user-data-dir=/home/zohair/Documents/google_profiles/Profile")
chrome_options.add_argument(f"profile-directory=Profile 1")  # Replace with your profile name
global link_list , cleaned_usernames
link_list=[]
cleaned_usernames=[]
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
def reach():
    driver.get("https://web.telegram.org/k/#@eB_maroc")
    driver.set_window_size(300,1050)
    time.sleep(5)
    members_list_xpath = "div[class='user-title']"
    driver.implicitly_wait(120)
    members = driver.find_element(By.CSS_SELECTOR, members_list_xpath)
    actions = ActionChains(driver)
    actions.move_to_element(members).click().perform()
    driver.implicitly_wait(50)
    time.sleep(5)
    mem=driver.find_element(By.XPATH , '//*[@id="column-right"]/div/div/div[2]/div/div[2]/div[4]/div[1]/div/nav/div[3]/div')
    actions.move_to_element(mem).click().perform()
    for i in range(1,246):
        try:
            # Press PAGE_DOWN to scroll down the page
            mem2=driver.find_element(By.XPATH, f"/html[1]/body[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[2]/div[4]/div[2]/div[3]/div[1]/ul[1]/a[{i}]")
            actions = ActionChains(driver)
            actions.move_to_element(mem2).click().perform()
            time.sleep(1)
            current_url = driver.current_url
            print(current_url)
            if current_url not in link_list and "@" in current_url :
                        link_list.append(current_url)
            driver.back()
            driver.implicitly_wait(20)
        except Exception as e:
            print(f"Error: {e}")
            pass
            

    i+=1
    print(link_list)
    global cleaned_usernames
    cleaned_usernames = [url.replace("https://web.telegram.org/k/#@", "") for url in link_list]

def csv_file():
    final_file='members_list55.csv'
    with open(final_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["members"])  # Write the header
        for member in cleaned_usernames:
            writer.writerow([member])

    print("Data has been written to " , final_file)
if __name__ == "__main__":
    reach()
    csv_file()