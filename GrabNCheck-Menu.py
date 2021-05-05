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

    def bye(self):
        print(bcolors.FAIL + "\n=================================" + bcolors.ENDC)
        print(bcolors.FAIL + "            Bye bye              " + bcolors.ENDC)
        print(bcolors.FAIL + "=================================\n" + bcolors.ENDC)
        exit()

    def get_emails(self, url):
        session = requests_html.HTMLSession()
        try:
            r = session.get(url)
            r.html.render()
            page = r.html.text
            emails = re.findall(EMAIL_REGEX, page)
            return emails
        except:
            print(bcolors.FAIL + "\nFailed to connect to the website. The website doesn't exit or it uses captcha protection." + bcolors.ENDC)


    def save_emails(self,url,emails):
        if "http://" in url or "https://" in url:
            url = url.replace('http://', '').replace('https://', '') #Removing the http/s from the string to make it look better
        url = "".join(x for x in url if x.isalnum())
        try:
            with open(url + "-emails.txt", "w") as txt_file:
                for line in emails:
                    txt_file.write("".join(line) + "\n")  # Saving emails line by line
            print(bcolors.OKGREEN + "\nThe emails have been saved in your current work directory\n" + bcolors.ENDC)
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

            pr = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="passwords"]')))
            pwds = pr.text

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

    def main(self):
        # Menú
        while True:
            print(bcolors.OKCYAN + "What do you want to do?:" + bcolors.ENDC)
            print(bcolors.WARNING + "[1] - Get every email from a website" + bcolors.ENDC)
            print(bcolors.WARNING + "[2] - Exit" + bcolors.ENDC)

            while True:
                print("\n" + bcolors.OKCYAN + "Enter option: " + bcolors.ENDC)
                option = input()
                if option in ('1', '2'):
                    break
                print("Invalid input.")

            if option == '1':
                print("\n" + bcolors.OKCYAN + "Enter a website (Must have http/https format): " + bcolors.ENDC)
                url = input()
                emails = self.get_emails(url)

                if not emails:
                    print("\n" + bcolors.FAIL + "No emails were found at " + url + "\n" + bcolors.ENDC)
                    continue

                print("\n" + bcolors.OKGREEN + "Emails found: " + bcolors.ENDC)
                for email in emails:
                    print(email)

                while True:
                    print("\n" + bcolors.OKCYAN + "What do you want to do?:" + bcolors.ENDC)
                    print(bcolors.WARNING + "[1] - Save emails (txt file)" + bcolors.ENDC)
                    print(bcolors.WARNING + "[2] - Check if emails are pwned" + bcolors.ENDC)
                    print(bcolors.WARNING + "[3] - Go back" + bcolors.ENDC)
                    print(bcolors.WARNING + "[4] - Exit" + bcolors.ENDC)

                    while True:
                        print("\n" + bcolors.OKCYAN + "Enter option: " + bcolors.ENDC)
                        option2 = input()
                        if option2 in ('1', '2', '3', '4'):
                            break
                        print("Invalid input.")

                    if option2 == '1': #Saving emails
                        self.save_emails(url,emails)
                        continue

                    if option2 == '2': #Check for pwns
                        self.check_pwns(emails)
                        continue

                    if option2 == '3':
                        break

                    if option2 == '4':
                        self.bye()

                    break

            if option == '2':
                self.bye()



if __name__ == "__main__":
    print(bcolors.FAIL + "###################################################################" + bcolors.ENDC)
    print(bcolors.FAIL + figlet_format("Grab N' Check", font="ogre") + bcolors.ENDC)
    print(bcolors.FAIL + "###################################################################\n" + bcolors.ENDC)
    p = name_in_process()
    p.main()