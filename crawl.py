#!/usr/bin/python
import eventlet
from eventlet.green.urllib import request
from selenium import webdriver
driver = webdriver.PhantomJS("phantomjs-2.1.1-windows/phantomjs-2.1.1-windows/bin/phantomjs")

header = ["097", "098", "0168", "0164", "0165", "0166", "0167", "0169", "091", "094", "0123", "0125", "0127", "0129", "090", "093", "0121", "0122", "0124", "0126", "0128", "092", "0188"]

current_header_index = 0

url = "http://sodt.mobi/"

current_stop = 0
current_start = 0

max_stop = 282475250


# Open a file
fo = open("test.txt", "wb")

def fetch(url):
    #return request.urlopen(url).read()
    print("fetching", url)
    driver.get(url)

    try:
        mobile_number = driver.find_element_by_xpath("/html/body/main/div/div/div[1]/div[1]/div[1]/h1").text
    except Exception as e:
    	name = "None"

    try:
    	name = driver.find_element_by_xpath("/html/body/main/div/div/div[1]/div[2]/div/h5").text.replace("person_pin ", "")
    except Exception as e:
    	name = "None"
    
    try:
    	location = (driver.find_element_by_xpath("/html/body/main/div/div/div[1]/div[2]/div/h6").text).replace("location_on ", "")
    except Exception as e:
    	location = "None"

    return name + "|" + mobile_number + "|" + location

pool = eventlet.GreenPool()

while current_header_index < len(header):

	while current_stop < max_stop:
		urls = set()

		current_stop = current_stop + 2000

		if current_stop > max_stop:
			current_stop = current_stop - abs(max_stop - current_stop)

		for i in range(current_start, current_stop):
			urls.add(url+header[current_header_index]+"-"+str(i).zfill(7))

		current_start = current_stop

		for body in pool.imap(fetch, urls):
			fo.write((body+"\r\n").encode(encoding='UTF-8'))

		pool.waitall()

	print("Finished " + header[current_header_index])

	current_stop = 0
	current_start = 0
	
	current_header_index = current_header_index + 1


# Close opend file
fo.close()