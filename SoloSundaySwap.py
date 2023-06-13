import argparse
import time
import configparser
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_config(filename):
    with open(filename, "r") as file:
        config_data = json.load(file)
    return config_data

def load_credentials(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    return config['DEFAULT']['username'], config['DEFAULT']['password'], config['DEFAULT']['chromedriver_path']

def login(driver, username, password):
    driver.find_element(By.NAME, 'username').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.XPATH, '//input[@type="submit"]').click()

def set_pools(driver, config):
    for i in range(3):
        config_key = f"config{i + 1}"
        pool_address = config[config_key]["mining_address"]
        miner_name = config[config_key]["miner_name"]
        miner_password = config[config_key]["password"]

        driver.find_element(By.XPATH, f"//tr[{i+1}]//td[2]//input").clear()
        driver.find_element(By.XPATH, f"//tr[{i+1}]//td[2]//input").send_keys(pool_address)
        driver.find_element(By.XPATH, f"//tr[{i+1}]//td[3]//input").clear()
        driver.find_element(By.XPATH, f"//tr[{i+1}]//td[3]//input").send_keys(miner_name)
        driver.find_element(By.XPATH, f"//tr[{i+1}]//td[4]//input").clear()
        driver.find_element(By.XPATH, f"//tr[{i+1}]//td[4]//input").send_keys(miner_password)


def save_changes(driver):
    save_button = driver.find_element(By.XPATH, "//input[@value='Save']")
    save_button.click()

def verify_and_log(driver):
    driver.refresh()
    time.sleep(5)
    for i in range(1, 4):
        pool_addr = driver.find_element(By.XPATH, f"//tr[{i}]//td[2]//input").get_attribute("value")
        miner_name = driver.find_element(By.XPATH, f"//tr[{i}]//td[3]//input").get_attribute("value")
        miner_pwd = driver.find_element(By.XPATH, f"//tr[{i}]//td[4]//input").get_attribute("value")
        with open("log.txt", "a") as log_file:
            log_file.write(f"Pool {i}: {pool_addr}, {miner_name}, {miner_pwd}\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file", help="Path to the configuration file.")
    args = parser.parse_args()

    # Load the configuration from the provided file
    config = load_config(args.config_file)

    # Load credentials
    username, password, chromedriver_path = load_credentials('credentials.ini')

    # Start a new Chrome browser instance
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service)

    driver.get("http://" + username + ":" + password +"@192.168.250.134/#miner")
    
    # Log in
    #login(driver, username, password)

    # Set pools
    set_pools(driver, config)
    
    # Save changes
    save_changes(driver)
    time.sleep(20)  # Wait for 20 seconds
    
    # Verify and log
    #verify_and_log(driver)

    # Close the browser instance
    driver.quit()

if __name__ == "__main__":
    main()
