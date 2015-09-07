
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
import time
import pandas as pd

'''def main():
    driver = webdriver.Firefox()
    driver.get("http://www.python.org")
    print(dir(driver))
    assert "Python" in driver.title
    elem = driver.find_element_by_name("q")
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    driver.close()
    
    display = Display(visible=0, size=(800, 600))
    display.start()
    driver = webdriver.Firefox()
    driver.get("https://www.ura.gov.sg/realEstateIIWeb/price/search.action")
    elem = driver.find_element_by_css_selector("#BtnViewAll")
    elem.click()'''
    #driver.close()
    
def init():

	display = Display(visible=0, size=(800, 600))
	display.start()
	year_list = get_year_list()
	for y in year_list:
		print(y)
        months = get_month_list(y)
    	print(months)
    	time.sleep(3)
    	#break
        '''for m in months:
            createCSV(year=y,month=m)'''
            
def get_year_list():
	driver = webdriver.Firefox()
	driver.get("https://www.ura.gov.sg/realEstateIIWeb/price/search.action")
	select_year = driver.find_element_by_css_selector("#yearSelect")
	year_list = [int(x.get_attribute("value")) for x in select_year.find_elements_by_tag_name("option")]
	driver.close()
	return year_list
    
def get_month_list(year):
    driver = webdriver.Firefox()
    driver.get("https://www.ura.gov.sg/realEstateIIWeb/price/search.action")
    select_year = driver.find_element_by_css_selector("#yearSelect")
    year_list = [x for x in select_year.find_elements_by_tag_name("option")]
    for y in year_list:
        if int(y.get_attribute("value"))==year:
            y.click()
            select_month = driver.find_element_by_css_selector("#monthSelect")
            months_list = [int(y.get_attribute("value")) for y in select_month.find_elements_by_tag_name("option")]
    driver.close()    
    return months_list

def main():
    init()

if __name__=="__main__":
    main()