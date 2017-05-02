import requests
import urllib
from bs4 import BeautifulSoup
from os.path import exists,join,dirname,realpath

name_url = 'https://dominionstrategy.com/all-cards'

img_url = 'http://www.hiwiller.com/dominion/images/'

def filter_name(nm):
    nm = nm.replace("'", "")
    nm = nm.replace(" ","")
    nm = nm.replace("-","")
    nm = nm.replace("_","")
    if(nm.lower().startswith('philosopher')):
        return 'philosophersstone'
    if(nm.lower().startswith('fool')):
        return 'foolsgold'
    if(nm.lower().startswith('king')):
        if(nm.lower().endswith('court')):
            return 'kingscourt'
    if(nm.lower().startswith('worker')):
        return 'workersvillage'
    return nm.lower()

def get_all_names():
    r = urllib.urlopen(name_url).read()
    soup = BeautifulSoup(r)
    tablediv = soup.find("div", {"id": "post-3041"})
    tables = tablediv.findChildren('table')
    imgnames = []
    for table in tables:
        rows = table.findChildren(['th','tr'])
        for row in rows:
            cells = row.findChildren('td')
            val = cells[0].string
            if(val):
                imgnames.append(filter_name(val))
    for im in imgnames:
        print im
    return imgnames

def get_all_imgs():
    nms = get_all_names()
    for nm in nms:
        dir_path = dirname(realpath(__file__))
        if(not exists(join(dir_path,nm+'.png'))):
            if(not exists(join(dir_path,nm+'.jpg'))):
                print img_url
                download_img(nm+'.jpg',img_url)

def download_img(file_name,base_url):
	from urllib2 import Request, urlopen, URLError, HTTPError
	
	#create the url and the request
	url = base_url + file_name
	req = Request(url)
	
	# Open the url
	try:
		f = urlopen(req)
		print "downloading " + url
		
		# Open our local file for writing
		local_file = open(file_name, "w" )
		#Write to our local file
		local_file.write(f.read())
		local_file.close()
		
	#handle errors
	except HTTPError, e:
		print "HTTP Error:",e.code , url
	except URLError, e:
		print "URL Error:",e.reason , url

if __name__ == '__main__':
    get_all_imgs()
