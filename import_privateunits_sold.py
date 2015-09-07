# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 17:40:37 2015

@author: Gokul Krishnaa
"""

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from pyvirtualdisplay import Display
import requests
import sys
import os

from pygurujobs.job import job
from pygurujobs.jobbase import JobBase
from pygurucore.tables import GuruTable

log = []

@job
class ImportPrivateUnitsSold(JobBase):
	name='import_privateunits_sold'
	description='Import private units sold from URA portal'

	def exec_(self):
		display = Display(visible=0, size=(800, 600))
		display.start()
		year_list = self.get_year_list()
		csv_folder=os.getcwd()+os.sep+"temp"
		for y in year_list:
			month_list = self.get_month_list(y)
			for m in month_list:
				create_units_sold_CSV(year=str(y),month=m,csv_folder=csv_folder)
		parse_csv()

	def get_year_list(self):
		driver = webdriver.Firefox()
		driver.get("https://www.ura.gov.sg/realEstateIIWeb/price/search.action")
		select_year = driver.find_element_by_css_selector("#yearSelect")
		year_list = [int(x.get_attribute("value")) for x in select_year.find_elements_by_tag_name("option")]
		driver.close()
		return year_list

	def get_month_list(self,year):
		baseURL = "https://www.ura.gov.sg/realEstateIIWeb/price/loadMonths.action?yearSelect="
		data = requests.get(baseURL+str(year))
		month = dict(data.json())
		return month.keys()

	def create_units_sold_CSV(self,year,month,csv_folder):
		profile = webdriver.FirefoxProfile()
		profile.set_preference('browser.download.folderList', 2) # custom location
		profile.set_preference('browser.download.manager.showWhenStarting', False)
		profile.set_preference('browser.download.dir', csv_folder)
		profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
		driver = webdriver.Firefox(profile)
		try:
			driver.get("https://www.ura.gov.sg/realEstateIIWeb/price/search.action")
			driver.implicitly_wait(5)
			select_year = Select(driver.find_element_by_name('yearSelect'))
			onchange_null  = "document.getElementById('yearSelect').onchange='';document.getElementById('monthSelect').onchange='';"
			clear_month = "$('#monthSelect').empty();"
			append_month = "$('#monthSelect').append(\"<option selected='selected' value="+str(month)+">"+str(month)+"</option>\");"  
			driver.execute_script(clear_month)
			driver.execute_script(onchange_null)
			driver.execute_script(append_month)
			select_year.select_by_visible_text(year)
			driver.execute_script("submitViewAll()") # The form submit function on the page is disabled. An ajax call is made to submitViewAll function
			driver.implicitly_wait(5)
			driver.get("https://www.ura.gov.sg/realEstateIIWeb/price/submitExcelResults.action")
			print(year,month)
			driver.close()
		except:
			print("Logging missed values")
			print(year,month)
			print(sys.exc_info())
			log.append([year,month])
			driver.implicitly_wait(10)

	def parse_csv(self,csv_folder):
		fileNameList = os.walk(csv_folder)
		for fileName in fileNameList:
			files = fileName[2]
			for f in files:
				if f[-3:]=="csv":
					reader = csv.reader(open(csv_folder+os.sep+f))
					reader = list(reader)
					title = ''.join(str(reader[0]).split()[-2:])[:-2]
					title = title+".csv"
					columns = reader[2]
					df = pd.DataFrame(reader[3:-13],columns=columns)
					self.insert_data_frame(df,title)
					df.to_csv(csv_folder+os.sep+title,index=False)
					os.remove(csv_folder+os.sep+f)

 
#https://www.ura.gov.sg/realEstateIIWeb/price/loadMonths.action?yearSelect=2008