import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from transactions import class_a, class_b, class_c
from db_writer import DataDumper
import pyotp


class Reporter():


    def __init__(self, b2_email, b2_pwd, db_host='b2-db', db_user='user', db_pwd='password', 
        db_port=3306, db_name="b2", timestamp='true', totp_key='false'):

        self.totp_key = str(totp_key)
        self.email = b2_email
        self.password = b2_pwd
        self.login_url = "https://secure.backblaze.com/user_signin.htm"
        self.transaction_results = []
        table_name='transactions'

        if timestamp.lower() == 'true':
            self.date = datetime.today().strftime("%Y-%m-%d %H-%M-%S")
        elif timestamp.lower() == 'false':
            self.date = datetime.today().strftime("%Y-%m-%d")
        else:
            print("INVALID TIMESTAMP OPTION")
            exit(1)

        self.db = DataDumper(db_host, db_user, db_pwd, db_port, db_name, table_name)
        self.driver_setup()
        self.authenticate()
        self.display_transactions()
        self.parse_transactions()
        self.save_transactions()

    def driver_setup(self):

        options=Options()
        options.headless=True
        options.set_preference("dom.webdriver.enabled", False)
        options.set_preference("useAutomationExtension", False)
        self.driver = webdriver.Remote(command_executor='http://firefox:4444',options=options)
        self.driver.implicitly_wait(15)
        self.driver.get(self.login_url)


    def authenticate(self):

        email_elem = self.driver.find_element(By.NAME, "email-field")
        email_elem.send_keys(self.email)
        email_elem.send_keys(Keys.RETURN)

        pwd_elem = self.driver.find_element(By.NAME, "password-field")
        pwd_elem.send_keys(self.password)
        pwd_elem.send_keys(Keys.RETURN)

        if self.totp_key.lower() != 'false':
            totp = pyotp.TOTP(self.totp_key).now()
            code_elem = self.driver.find_element(By.NAME, "code-field")
            code_elem.send_keys(totp)
            code_elem.send_keys(Keys.RETURN)

    def display_transactions(self):

        report_link = self.driver.find_element(By.LINK_TEXT, 'Reports')
        report_link.click()

        #toggle transaction buttons to expose table
        transaction_toggles = {  #CSS_selectors
            'A': 'span.transaction-detail-A:nth-child(3) > img:nth-child(1)',
            'B': 'span.transaction-detail-B:nth-child(3) > img:nth-child(1)',
            'C': 'span.transaction-detail-C:nth-child(3) > img:nth-child(1)'
        }

        def transaction_toggler(css_selector):
            tog = self.driver.find_element(By.CSS_SELECTOR, css_selector)
            tog.click()

        for transaction in transaction_toggles:
            transaction_toggler(transaction_toggles[transaction])

    def parse_transactions(self):

        transaction_tables = {  #CSS_selectors
            'A': 'div.transaction-detail-A',
            'B': 'div.transaction-detail-B',
            'C': 'div.transaction-detail-C'
        }


        def parse_table(css_selector):

            table = self.driver.find_element(By.CSS_SELECTOR, css_selector)
            table_text = table.text.split('\n')
            table_tidy = [line.strip() for line in table_text]

            def sqlformat(value):
                return '"'+value+'"'

            transaction_type = ''
            for i, val in enumerate(table_tidy):
                if val in class_a:
                    transaction_type = "A"
                elif val in class_b:
                    transaction_type = "B"
                elif val in class_c:
                    transaction_type = "C"
                else:
                    continue
                self.transaction_results.append([
                    sqlformat(val), 
                    sqlformat(table_tidy[i + 1].replace(',', '')), 
                    sqlformat(transaction_type), 
                    sqlformat(self.date)
                ])

        for table in transaction_tables:
             parse_table(transaction_tables[table])

    def save_transactions(self):
        for transaction in self.transaction_results:
            self.db.update_db(transaction)

        self.db.disconnect_db()
        self.driver.quit()
