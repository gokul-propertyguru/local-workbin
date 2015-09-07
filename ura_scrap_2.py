from selenium import webdriver
from selenium.webdriver.support.ui import Select
from pyvirtualdisplay import Display
import time
import pandas as pd

year = [1]
month = [1]

def init():
	display = Display(visible=0, size=(800, 600))
	display.start()
	for y in year:
		for m in month:
			createCSV(year=y,month=m)

def createCSV(year,month):
	profile = webdriver.FirefoxProfile()
	profile.set_preference('browser.download.folderList', 2) # custom location
	profile.set_preference('browser.download.manager.showWhenStarting', False)
	profile.set_preference('browser.download.dir', "/var/www/dev_workbin")
	profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
	driver = webdriver.Firefox(profile)
	driver.get("https://www.ura.gov.sg/realEstateIIWeb/price/search.action")
	form = driver.find_element_by_id("SubmitSearchForm")
	select_year = Select(driver.find_element_by_name('yearSelect'))
	select_year.select_by_index(year)
	select_month = Select(driver.find_element_by_name('monthSelect'))
	select_month.select_by_index(year)
	form.submit()
	
def main():
	init()

if __name__=="__main__":
	main()

