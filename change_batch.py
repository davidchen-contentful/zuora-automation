from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import csv
import time
from login_zuora import *

#set download path
options = webdriver.ChromeOptions()
prefs = {'download.default_directory':'/Users/davidchen/PycharmProjects/pythonProject/Zuora/Datasources'}
options.add_experimental_option('prefs',prefs)
driver = webdriver.Chrome(options=options, executable_path='/Users/davidchen/PycharmProjects/pythonProject/Drivers/chromedriver')

#save previous os instance
before = os.listdir('/Users/davidchen/PycharmProjects/pythonProject/Zuora/Datasources')

#download file
driver.get('https://redash.prd.data.contentful.org/api/queries/2682/results.csv?api_key=e0a6K5WZ7CHwNA5AE8jLHVuAPe7n96eWDnnBFyD9')
time.sleep(3)

#check for new downloaded file
after  = os.listdir('/Users/davidchen/PycharmProjects/pythonProject/Zuora/Datasources')
change = set(after) - set(before)
file_name = ''
if len(change) == 1:
    file_name = change.pop()
else:
    print("More than one file or no file downloaded")

#Log into Zuora
driver.get("https://www.zuora.com/apps/CustomerAccount.do?menu=Z-Billing#/page/1/tab/2")

driver.maximize_window()
time.sleep(2)

#logs into zuora
username = driver.find_element_by_id("id_username")
username.clear()
username.send_keys("david.chen@contentful.com")

password = driver.find_element_by_name("password")
password.clear()
password.send_keys("KLUX3somp-gaur")

#clicks login button
driver.find_element_by_xpath("/html/body/form[2]/div/a").click()
time.sleep(3)

#csv data
expand = 0
with open('/Users/davidchen/PycharmProjects/pythonProject/Zuora/Datasources/' + file_name, newline='') as inputfile:
    reader = csv.reader(inputfile)
    next(reader, None)

#BEGIN LOOP

    for row in reader:

        #loop list creation for row data
        list = []
        list.append(row[0])

        #go to account URL
        driver.get('https://www.zuora.com/apps/CustomerAccount.do?method=view&id={}'.format(list[0]))
        time.sleep(1)

        #expand Billing and Payment Info
        if expand == 0:
            driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/table/tbody/tr/td[2]/div[4]/div[1]/div/div[2]/div/div[2]/div/div[1]/a/h2").click()
            expand += 1

        #click edit Billing and Payment Info
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/table/tbody/tr/td[2]/div[4]/div[1]/div/div[2]/div/div[2]/div/div[2]/div[1]/ul/li/a/span").click()

        #change Billing Batch
        time.sleep(3)
        driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/table/tbody/tr/td[2]/div[4]/div[1]/div/div[2]/div/div/div/div[2]/div/div[2]/div/form/table/tbody/tr[10]/td/select").send_keys("Batch9 (Committed Clients Email Invoicing)")
        driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/table/tbody/tr/td[2]/div[4]/div[1]/div/div[2]/div/div/div/div[2]/div/div[2]/div/form/table/tbody/tr[10]/td/select").send_keys(Keys.ENTER)

        #click Save
        driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/table/tbody/tr/td[2]/div[4]/div[1]/div/div[2]/div/div/div/div[2]/div/div[3]/div[1]/span").click()

        print("Row {} has been updated".format(row))