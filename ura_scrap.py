# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 17:40:37 2015

@author: Gokul Krishnaa
"""
import site
site.addsitedir("/var/www/data-prototyping/")

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from pyvirtualdisplay import Display
import requests
import sys
import os
from pygurujobs.job import JOBNAMES,auto_import
from pygurucore.tables import GuruTable
import shutil
import csv
import pandas as pd
import datetime as dt

log = []

def get_year_list():
	driver = webdriver.Firefox()
	driver.get("https://www.ura.gov.sg/realEstateIIWeb/price/search.action")
	select_year = driver.find_element_by_css_selector("#yearSelect")
	year_list = [int(x.get_attribute("value")) for x in select_year.find_elements_by_tag_name("option")]
	driver.close()
	return year_list
 
def get_month_list(year):
    baseURL = "https://www.ura.gov.sg/realEstateIIWeb/price/loadMonths.action?yearSelect="
    data = requests.get(baseURL+str(year))
    month = dict(data.json())
    return month.keys()

def create_csv(year,month):
	path = os.getcwd()+os.sep+"temp"
	profile = webdriver.FirefoxProfile()
	profile.set_preference('browser.download.folderList', 2) # custom location
	profile.set_preference('browser.download.manager.showWhenStarting', False)
	profile.set_preference('browser.download.dir', path)
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
		driver.execute_script("submitViewAll()")
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

def parse_csv():
	path = os.getcwd()+os.sep+"temp"
	df_agg = pd.DataFrame()
	if not os.path.isdir(path):
		print("URA data not yet extracted to temp directory.")
		return -1
	fileNameList = os.walk(path)
	for fileName in fileNameList:
		files = fileName[2]
	for f in files:
		if f[-3:]=="csv":
			file_handler = open(path+os.sep+f)
			reader = csv.reader(file_handler)
			reader = list(reader)
			title = ''.join(str(reader[0]).split()[-2:])[:-2]
			title = title+".csv"
			columns = reader[2]
			try:
				df = pd.DataFrame(reader[3:-13],columns=columns)
			except AssertionError:
				print(title)
				print(sys.exc_info())
				continue
			df["year"]=int(title.split(".")[0][-4:])
			df["month"]=title.split(".")[0][:-4]
			df = pd.DataFrame(reader[3:-13],columns=columns)
			file_handler.close()
			df.to_csv(path+os.sep+title,index=False)
			df_agg = df_agg.append(df)
			os.remove(path+os.sep+f)
	write_db(df_agg)

def write_db(dataset):
    if dataset.empty:
        print("No data to insert into database")
    else:
        dataset.to_csv("Agg_Data.csv",index=False)
        for i in range(len(dataset)):
            insert_row(dataset.iloc[i])

def insert_row(row):
    dest_table=GuruTable(table_name='ura_private_units_sold')
    #print(row)
    dest_table.insert().values(
        year=row["year"],
        month=row["month"],
        developer=row["Developer"],
        property_type=row["Property Type"],
        locality=row["Locality"],
        street_name=row["Street Name"],
        project_name=row["Project Name"],
        total_units_projects=row["Total Number of Units in Project"],
        cumulative_units_launched=row["Cumulative Units Launched to-date"],
        cumulative_units_sold=row["Cumulative Units Sold to-date"],
        total_unsold_units=row["Total Number of Unsold Units"],
        cumulative_units_launched_unsold=row["Cumulative Units Launched but Unsold"],
        units_launched_month=row["Units Launched in the Month"],
        units_sold_month=row["Units Sold in the Month"],
        median_price_psf_month=row["Median Price ($psf) # in the Month"],
        lowest_price_psf_month=row["Lowest Price ($psf) # in the Month"],
        highest_price_psf_month=row["Highest Price ($psf) # in the Month"],
        modified_date=dt.datetime.now()
    ).execute()

    
def init():
	display = Display(visible=0, size=(800, 600))
	display.start()
	year_list = get_year_list()
	path = os.getcwd()+os.sep+"temp"
	if os.path.isdir(path):
		print("Removing temp folder.")
		shutil.rmtree(path)
	for y in year_list[-1:]:##remove -1
		month_list = get_month_list(y)
		for m in month_list:
			create_csv(year=str(y),month=m)
	parse_csv()

 
def main():
	init()
 
if __name__=="__main__":
	main()

#https://www.ura.gov.sg/realEstateIIWeb/price/loadMonths.action?yearSelect=2008