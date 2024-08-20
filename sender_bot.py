from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time, pandas as pd , math
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

# Setup Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-notifications")
chrome_options.binary_location = "/usr/bin/google-chrome"
profile_list = ["1", "2", "3"]
file_path = '/home/zohair/Surviral_scrapers/members_listcopy.csv'
def get_usernames_from_csv():
    global all_usernames, divided_usernames
    all_usernames = []
    df = pd.read_csv(file_path)
    if 'members' in df.columns:
        all_usernames = [q for q in df['members'] if not str(q).isdigit()]
        print(all_usernames)
        print(len(all_usernames))
    else:
        print("Column 'members' does not exist in the CSV file.")
        return
    num_profiles = len(profile_list)
    usernames_per_profile = math.ceil(len(all_usernames) / num_profiles)
    divided_usernames = []
    start = 0
    for _ in range(num_profiles):
        end = start + usernames_per_profile
        divided_usernames.append(all_usernames[start:end])
        start = end
    for idx, subset in enumerate(divided_usernames):
        print(f"Profile {profile_list[idx]} will get {len(subset)} usernames.")

def messenger_bot():
    global failed_items
    for i, profile_id in enumerate(profile_list):
        chrome_options.add_argument("user-data-dir=/home/zohair/.config/google-chrome")
        chrome_options.add_argument(f"profile-directory=Profile {profile_id}")  # Replace with your profile name
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        driver.get('https://web.telegram.org')
        time.sleep(10)

        # Get the usernames assigned to this profile
        usernames_for_profile = divided_usernames[i]
        
        for username in usernames_for_profile:
            try:
                text_box = WebDriverWait(driver, 50).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="column-left"]/div/div/div[1]/div[2]/input'))
                )
                text_box.clear()
                text_box.send_keys(username)
                time.sleep(3)
                driver.implicitly_wait(50)
                resultss = driver.find_element(By.CSS_SELECTOR, 'a[class="row no-wrap row-with-padding row-clickable hover-effect rp chatlist-chat chatlist-chat-abitbigger"]')
                actions = ActionChains(driver)
                actions.move_to_element(resultss).click().perform()
                time.sleep(3)
                driver.implicitly_wait(10)
                input_message = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div/div[4]/div/div[1]/div/div[8]/div[1]/div[1]')
                input_message.clear()
                input_message.send_keys("This is a test message ")
                time.sleep(2)
                input_message.clear()
                time.sleep(2)
                print("message sent to  :" , username)
                # usernames_for_profile.remove(username)
                # print(usernames_for_profile)
            except Exception as e:
                failed_items=[]
                failed_items.append(username)
                print(f"Failed for URL:              {username}  {e}")
        
        
        driver.quit()
    print(failed_items)

if __name__ == "__main__":
    get_usernames_from_csv()
    messenger_bot()
