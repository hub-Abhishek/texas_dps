from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from datetime import datetime
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd


class dps_appointement:
    def __init__(self, iterator='', idno='', fname='', lname='', dob='', ssn='', phone='', mail='', zip_code=''):
        self.iterator = iterator
        self.idno = idno
        self.fname = fname
        self.lname = lname
        self.dob = dob
        self.ssn = ssn
        self.phone = phone
        self.mail = mail
        self.zip_code = zip_code
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def get_elements_by_class(self, name):
        return self.driver.find_elements_by_class_name(name)

    def get_all_elements_by_css(self, element):
        return element.find_elements_by_css_selector('*')

    def check(self, dates):
        within_7 = (dates - pd.to_datetime(datetime.today())).days < 7
        if within_7:
            self.driver.find_element_by_xpath(f'//*[@id="app"]/section/div/main/div/section/div[2]/div/div[2]/div/table/tbody/tr[{len(dates)-1}]/td[4]').click()
        return within_7

    def initialize(self):
        self.driver.get(url='https://public.txdpsscheduler.com/')
        return None

    def login(self):
        self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div[2]/button[1]').click()

        diction_login = {'Texas Card Number (DL, ID, EIC)': self.idno, 'First Name': self.fname,
                         'Last Name': self.lname, 'Date of Birth (mm/dd/yyyy)': self.dob, 'Last four of SSN': self.ssn}

        elements_on_page = self.get_elements_by_class("v-text-field__slot")

        for element in elements_on_page:
            sub_elements = self.get_all_elements_by_css(element)
            if sub_elements[0].text in diction_login.keys():
                sub_elements[1].send_keys(diction_login[sub_elements[0].text])

        for z in self.get_elements_by_class('v-btn__content'):
            if z.text == 'LOG ON':
                z.click()
        return None

    def get_new_appointment(self):

        for element in self.get_elements_by_class('v-btn__content'):
            if element.text == 'NEW APPOINTMENT':
                element.click()
                break

        # type of appointment
        self.driver.find_element_by_xpath(
            '//*[@id="app"]/section/div/main/div/section/div[2]/div/main/div/div/div[1]/div[1]/button').click()

        diction_details = {'Home Phone': self.phone, 'Cell Phone': self.phone, 'Email': self.mail,
                           'Verify Email': self.mail, 'Zip Code': self.zip_code}

        for element in self.driver.find_elements_by_class_name('v-text-field__slot'):
            if element.text in diction_details.keys():
                element.find_elements_by_css_selector('*')[1].clear()
                element.find_elements_by_css_selector('*')[1].send_keys(diction_details[element.text])

        # Get notification by phone
        self.driver.find_element_by_xpath(
            '//*[@id="app"]/section/div/main/div/section/div[2]/div/form/div/div[1]/div/div[7]/div/div[1]/div/div[1]/div').click()

        # Next page
        self.driver.find_element_by_xpath(
            '//*[@id="app"]/section/div/main/div/section/div[2]/div/form/div/div[2]/div[2]/div/div[2]/button').click()

        sleep(5)

        dates = pd.to_datetime(self.driver.find_element_by_xpath(
            '//*[@id="app"]/section/div/main/div/section/div[2]/div/div[1]/div/table/tbody/tr/td[3]').text)
        status = self.check(dates)

        if status:
            print(f'got date {dates} at {self.zip_code}')
            return status, dates
        else:
            print(f'getting date {dates} at {self.zip_code}, not booked')
            return False, False

        # for row in self.driver.find_element_by_xpath(
        #     '//*[@id="app"]/section/div/main/div/section/div[2]/div/div[2]/div/table'
        #     ).find_elements(By.TAG_NAME, "tr"):
        #     for col_num, col in enumerate(row.find_elements(By.TAG_NAME, "td")):
        #         if col_num == 2:
        #             dates.append(col.text)
        #         status = self.check(dates)
        #
        #         if status:
        #             return status

    def book_appointment(self):
        # click date
        self.driver.find_element_by_xpath(
            '//*[@id="app"]/section/div/main/div/section/div[2]/div/div[3]/table/tbody/tr/td[2]/div/div[1]').click()

        # click time
        self.driver.find_element_by_xpath(
            '//*[@id="app"]/section/div/main/div/section/div[2]/div/div[2]/table/tbody/tr/td[2]/div/div[1]/div').click()

        # click next
        self.driver.find_element_by_xpath(
            '//*[@id="app"]/section/div/main/div/section/div[2]/div/div[4]/div/div[2]/button/span').click()

        # click confirm
        # self.driver.find_element_by_xpath(
        #     '//*[@id="app"]/section/div/main/div/section/div[2]/div/div[4]/div/div[2]/button/span').text