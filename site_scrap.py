import sys
from lxml import html
import requests
import bs4
import re
import csv, math
from decimal import *

PROJECT = ''
IMG_ROOT = ''
HEADER = ['sku','atrribute_set', 'type', 'store', 'name', 'description','short_description', 'price', 'special_price', 'qty', 'is_in_stock', 'manage_stock', 'use_config_manage_stock','status', 'visibility','options_container', 'weight', 'categories', 'thumbnail', 'small_image', 'image', 'media_gallery','special_from_date','special_to_date','news_from_date','news_to_date']

def strip_tags(elem):
    raw = re.sub("<.*?>", "", str(elem))
    return raw

urls = []

with open(PROJECT+'.txt', 'rU') as f:
    for line in f:
        urls.append(line)

csv_file = open(PROJECT+'.csv', 'wb')
wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
wr.writerow(HEADER)

for url in urls:

	page = requests.get(url)
	soup = bs4.BeautifulSoup(page.text,'html.parser')

	title = soup.select('h1.PageAdvertDetails-heading')
	
	not_found = False
	try:
		title = strip_tags(title[0])
	except:
		print 'product not found: {0}'.format(url)
		not_found = True
		#sys.exit()
		
	if not_found == False:
		try:
			new_price = soup.select('span.Price-sale span')
			new_price = strip_tags(new_price[0])
			new_price = new_price.replace('$','').replace(',','')
		except:
			new_price = ''

		try:
			old_price = soup.select('span.Price-was')
			old_price = strip_tags(old_price[0])
			old_price = old_price.replace('$','').replace(',','')
		except:
			old_price = ''
		
		images = soup.select('div.slide img.RatioBox-child')
		imgs = []
		for img in images:
			imgs.append(IMG_ROOT+img['src'])

		thumb = imgs[0]
		small = imgs[0]
		image = imgs[0]
		media_gallery = ','.join(imgs)

		try:
			desc = soup.findAll('div', {'itemprop' : 'description'})
			short_desc = strip_tags(desc[0])
		except:
			short_desc = ''
			
		try:
			specs = soup.findAll('div', {'itemprop' : 'specifications'})
			long_desc = strip_tags(specs[0])
		except:
			long_desc = ''
			
		cats = soup.select('div.Breadcrumbs-item a span')
		new_cats = []
		for cat in cats:
			cat = strip_tags(cat)
			new_cats.append(cat)

		categories = '/'.join(new_cats)

		sku = title.replace(' ','').lower()

		new_start = '2015-1-01'
		new_end = '2020-01-01'
		special_start = '2015-1-01'
		special_end = '2020-01-01'

		row = [sku,'Default','simple','admin',title,long_desc,short_desc,old_price,new_price,99999,1,1,1,1,'Catalog, Seach','Product Info Column',0,categories, thumb, small, image, media_gallery,special_start,special_end,new_start,new_end]
		wr.writerow(row)

