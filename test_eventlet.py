import eventlet
from eventlet.green import urllib2
from lxml import etree
from lxml.etree import tostring
from lxml.html.soupparser import fromstring

url = "http://sodt.mobi/"

header_test = ["097", "098", "0168", "0164", "0165", "0166", "0167", "0169", "091", "094", "0123", "0125", "0127", "0129", "090", "093", "0121", "0122", "0124", "0126", "0128", "092", "0188"]
current_stop = 0
current_start = 0
current_header_index = 0

max_stop = 282475250
#max_stop = 21

def fetch(url):
	print("fetching", url)
	return urllib2.urlopen(url, timeout=60).read()

fo = open("test.txt", "wb")

while current_header_index < len(header_test):

	while current_stop < max_stop:
		urls = set()

		current_stop = current_stop + 100

		if current_stop > max_stop:
			current_stop = current_stop - abs(max_stop - current_stop)


		for i in range(current_start, current_stop):
			urls.add(url+header_test[current_header_index]+"-"+str(i).zfill(7)+".html")

		current_start = current_stop

		pool = eventlet.GreenPool(50)
		for body in pool.imap(fetch, urls):
			try: 
			    root = fromstring(body)
			    tree = etree.ElementTree(root)
			    name = tree.xpath("/html/body/main/div/div/div[1]/div[2]/div/h5/text()")
			    location = tree.xpath("/html/body/main/div/div/div[1]/div[2]/div/h6/text()")
			    mobile_number = tree.xpath("/html/body/main/div/div/div[1]/div[1]/div[1]/h1")
			    if len(name) > 0 and len(mobile_number) >0:
			    	if len(location) > 0:
			    		total = name[0] + "|" + location[0] + "|" + mobile_number[0].text	
			    	else:
			    		total = name[0] + "|" + "None" + "|" + mobile_number[0].text

			    	fo.write((total+"\r\n").encode(encoding='UTF-8'))

			    	print((total+"\r\n").encode(encoding='UTF-8'))
			except Exception:
				print("Error")
		pool.waitall()
	print("Finished " + header_test[current_header_index])

	current_stop = 0
	current_start = 0
	
	current_header_index = current_header_index + 1	    	

fo.close()

