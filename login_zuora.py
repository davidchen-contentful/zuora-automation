
from selenium import webdriver
driver = webdriver.Chrome('/Users/davidchen/PycharmProjects/pythonProject/Drivers/chromedriver')

#log into Zuora

def login():

    #navigates to zuora
    driver.get("https://www.zuora.com/apps/CustomerAccount.do?menu=Z-Billing#/page/1/tab/2")

    driver.maximize_window()

    #logs into zuora
    username = driver.find_element_by_id("id_username")
    username.clear()
    username.send_keys("david.chen@contentful.com")

    password = driver.find_element_by_name("password")
    password.clear()
    password.send_keys("KLUX3somp-gaur")

    #clicks login button
    driver.find_element_by_xpath("/html/body/form[2]/div/a").click()
