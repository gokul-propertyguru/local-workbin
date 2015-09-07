from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display
import requests
import io
import sys
import os
import shutil
import csv
import pandas as pd


def main():
    display = Display(visible=0, size=(800, 600))
    display.start()
    path = os.getcwd()+os.sep+"realis_temp"
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2) # custom location
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', path)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
    driver = webdriver.Firefox(profile)
    driver.get("https://spring.ura.gov.sg/lad/ore/login/index.cfm")
    driver.implicitly_wait(5)
    username = driver.find_element_by_name("Username")
    password = driver.find_element_by_name("password")
    username.send_keys("allproperty")
    password.send_keys("lf456789")

    submit = driver.find_element_by_name("Submit")
    submit.click()

    driver.implicitly_wait(3)
    driver.get("https://spring.ura.gov.sg//lad/ore/property_market/project/project_resi_search_projdetail.cfm")
    select_year = driver.find_element_by_name("year")
    year_list = [x.get_attribute("value") for x in select_year.find_elements_by_tag_name("option")]
    year = Select(driver.find_element_by_name("year"))
    quarter = Select(driver.find_element_by_name("quarter"))
    for y in year_list:
        year = Select(driver.find_element_by_name("year"))
        select_types = driver.find_element_by_name("all_pytype")
        [x.click() for x in select_types.find_elements_by_tag_name("option")]
        [x.click() for x in driver.find_element_by_name("selected_pytype").find_elements_by_tag_name("option")]
        driver.find_element_by_name("add").click()
        year.select_by_visible_text('2012')
        for q in [1,2,3,4]:
            driver.find_element_by_xpath("//input[@type='submit']").click()
            driver.find_element_by_xpath("//input[@type='submit']").click()
            anchors = driver.find_elements_by_tag_name("a")
            for a in anchors:
                if a.get_attribute("onclick") is not None:
                    a.click()
                    break
            break
        break
    driver.get("https://spring.ura.gov.sg//lad/ore/property_market/project/project_resi_search_projdetail.cfm")

if __name__=="__main__":
    main()