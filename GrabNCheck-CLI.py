import argparse
import os
import requests_html
import re
from pyfiglet import figlet_format   #fonts http://www.figlet.org/examples.html
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tabulate import tabulate

EMAIL_REGEX = r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+'
CHROME_WEBDRIVER_PATH = r'C:\webdrivers\chromedriver' #Modify this to your webdriver path

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class name_in_process:
    def __init__(self):
        pass

    def get_emails(self, url):
        session = requests_html.HTMLSession()
        try:
            r = session.get(url)
            r.html.render()
            page = r.html.text
            emails = re.findall(EMAIL_REGEX, page)
            return emails
        except:
            print(
                bcolors.FAIL + "\nFailed to connect to the website. The website doesn't exit or it uses captcha protection." + bcolors.ENDC)

    def save_emails(self,url,emails):
        if "http://" in url or "https://" in url:
            url = url.replace('http://', '').replace('https://', '') # Removing the http/s from the string to make it look better
        url = "".join(x for x in url if x.isalnum())

        try:
            with open(url + "-emails.txt", "w") as txt_file:
                for line in emails:
                    txt_file.write("".join(line) + "\n")  # Saving emails line by line
            print(bcolors.OKGREEN + "The emails have been saved in your current work directory\n" + bcolors.ENDC)
        except:
            print(bcolors.FAIL + "The emails couldn't be saved\n" + bcolors.ENDC)

    def save_pwds(self,email,passwds):
        try:
            with open(email +"-passwords.txt", "w") as txt_file:
                for line in passwds:
                    txt_file.write("".join(line) + "\n")  # Saving passwords line by line
            print(bcolors.OKGREEN + "The passwords have been saved in your current work directory\n" + bcolors.ENDC)
        except:
            print(bcolors.FAIL + "The passwords couldn't be saved\n" + bcolors.ENDC)

    def check_pwns(self,emails):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        driver = webdriver.Chrome(executable_path=CHROME_WEBDRIVER_PATH,options=options)

        driver.get("https://breachdirectory.tk/")

        driver.implicitly_wait(5)

        for email in emails:
            print(bcolors.WARNING + "Checking pwns for " + email + bcolors.ENDC)
            driver.find_element_by_xpath('//*[@id="home"]/div/form/div/input').send_keys(email)

            driver.implicitly_wait(10)

            driver.find_element_by_xpath('//*[@id="home"]/div/form/div/button').click()

            driver.implicitly_wait(10)
            try:
                pr = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="passwords"]')))
                pwds = pr.text
            except:
                print(bcolors.FAIL + "Failed. Timeout exception" + bcolors.ENDC)

            if "No data available in table" in pwds:
                print("No data available in table: " + email +" hasn't been pwned. \n")
            else:
                pwds = pwds.replace("CENSORED PASSWORD", "CENSORED-PASSWORD").replace("SHA-1 HASH", "SHA-1-HASH")
                pwds = re.split('\n', pwds)
                pwd_table = []

                for row in pwds:
                    pwd_table.append(re.split(" ", row))

                print(tabulate(pwd_table[1:], headers=pwd_table[0]))
                print("")
                self.save_pwds(email,pwds)

            #Clear text input
            driver.find_element_by_xpath('//*[@id="home"]/div/form/div/input').clear()

        driver.close()

    def main(self, args):
        if "http://" not in args.url and "https://" not in args.url :
            args.url = "http://" + args.url

        print(bcolors.WARNING + "Looking for emails...")
        emails = self.get_emails(args.url)

        if not emails:
            print("\n" + bcolors.FAIL + "No emails were found at " + args.url + "\n" + bcolors.ENDC)
            exit()

        print("\n" + bcolors.OKGREEN + "Emails found at " + args.url + ": " + bcolors.ENDC)
        for email in emails:
            print(email)

        print(bcolors.WARNING + "\nSaving emails..." + bcolors.ENDC)
        self.save_emails(args.url,emails)

        print(bcolors.WARNING + "\nChecking if the emails have been pwned...\n" + bcolors.ENDC)
        self.check_pwns(emails)


if __name__ == "__main__":
    print(bcolors.FAIL + "###################################################################" + bcolors.ENDC)
    print(bcolors.FAIL + figlet_format("Grab N' Check", font="ogre") + bcolors.ENDC)
    print(bcolors.FAIL + "###################################################################\n" + bcolors.ENDC)

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', type=str, help='The target URL.', required=True)

    args = parser.parse_args()

    p = name_in_process()
    p.main(args)