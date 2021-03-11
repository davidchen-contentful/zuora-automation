from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import csv
import time

# set download path
options = webdriver.ChromeOptions()
prefs = {'download.default_directory':'/Users/davidchen/PycharmProjects/pythonProject/Zuora/Datasources'}
options.add_experimental_option('prefs',prefs)
driver = webdriver.Chrome(options=options, executable_path='/Users/davidchen/PycharmProjects/pythonProject/Drivers/chromedriver')

# save previous os instance
before = os.listdir('/Users/davidchen/PycharmProjects/pythonProject/Zuora/Datasources')

# download file
driver.get('https://redash.prd.data.contentful.org/api/queries/2217/results.csv?api_key=gSBpcGnMJzjN2g6FX4jCoq3cG3kYMsvxkS56bfGv')
time.sleep(3)

# check for new downloaded file
after  = os.listdir('/Users/davidchen/PycharmProjects/pythonProject/Zuora/Datasources')
change = set(after) - set(before)
file_name = ''
if len(change) == 1:
    file_name = change.pop()
else:
    print("More than one file or no file downloaded")

# Log into Zuora
driver.get("https://www.zuora.com/apps/CustomerAccount.do?menu=Z-Billing#/page/1/tab/2")

driver.maximize_window()
time.sleep(2)

# logs into zuora
username = driver.find_element_by_id("id_username")
username.clear()
username.send_keys("david.chen@contentful.com")

password = driver.find_element_by_name("password")
password.clear()
password.send_keys("KLUX3somp-gaur")

# clicks login button
driver.find_element_by_xpath("/html/body/form[2]/div/a").click()
time.sleep(3)

# csv data
expand = 0
with open('/Users/davidchen/PycharmProjects/pythonProject/Zuora/Datasources/' + file_name, newline='') as inputfile:
    reader = csv.DictReader(inputfile, delimiter = ',')

# BEGIN LOOP

    for row in reader:

        # list creation
        list = []
        list.append(row['id'])
        list.append(row['upper'])

        # go to account URL
        driver.get('https://www.zuora.com/apps/CustomerAccount.do?method=view&id={}'.format(list[0]))
        time.sleep(1)

        # click edit Basic Information
        driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/table/tbody/tr/td[2]/div[4]/div[1]/div/div[1]/div/div[2]/div/div[1]/ul/li/a/span").click()

        #change Enterprise Account field
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/table/tbody/tr/td[2]/div[4]/div[1]/div/div[1]/div/div/div/div[2]/div/div[2]/div/table/tbody/tr/td[2]/form[1]/table/tbody/tr[21]/td/select").send_keys('Yes')
        driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/table/tbody/tr/td[2]/div[4]/div[1]/div/div[1]/div/div/div/div[2]/div/div[2]/div/table/tbody/tr/td[2]/form[1]/table/tbody/tr[21]/td/select").send_keys(Keys.ENTER)

        # click 'Save' (Basic Information)
        driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/table/tbody/tr/td[2]/div[4]/div[1]/div/div[1]/div/div/div/div[2]/div/div[3]/div[1]/span").click()
        time.sleep(2)

        # expand Billing and Payment Info
        if expand == 0:
            driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/table/tbody/tr/td[2]/div[4]/div[1]/div/div[2]/div/div[2]/div/div[1]/a/h2").click()
            time.sleep(1)
            expand += 1

        # click edit Billing and Payment Info
        driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/table/tbody/tr/td[2]/div[4]/div[1]/div/div[2]/div/div[2]/div/div[2]/div[1]/ul/li/a/span").click()
        time.sleep(2)

        # update tax company code
        if list[1] == 'INC':
            driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/table/tbody/tr/td[2]/div[4]/div[1]/div/div[2]/div/div/div/div[2]/div/div[2]/div/form/table/tbody/tr[28]/td/select").send_keys('CONTENTFULINC')
            driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/table/tbody/tr/td[2]/div[4]/div[1]/div/div[2]/div/div/div/div[2]/div/div[2]/div/form/table/tbody/tr[28]/td/select").send_keys(Keys.ENTER)
        elif list[1] == 'GMBH':
            driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/table/tbody/tr/td[2]/div[4]/div[1]/div/div[2]/div/div/div/div[2]/div/div[2]/div/form/table/tbody/tr[28]/td/select").send_keys('CONTENTFULGMBH')
            driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/table/tbody/tr/td[2]/div[4]/div[1]/div/div[2]/div/div/div/div[2]/div/div[2]/div/form/table/tbody/tr[28]/td/select").send_keys(Keys.ENTER)
        else:
            print('There is no entity to select a tax code')

        # click Save (Billing and Payment Info)
        driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/table/tbody/tr/td[2]/div[4]/div[1]/div/div[2]/div/div/div/div[2]/div/div[3]/div[1]/span").click()

        print("Row {} has been updated".format(row))



