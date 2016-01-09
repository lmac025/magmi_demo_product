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

IMG_URL = ''
#format: title,price,categories,thumb,small,image,media_gallery,short_desc,long_desc
#format 2: title,price,categories,image,short_desc,long_desc
cnt = 0
for url in urls:
	
	if cnt!=0 and url[0] and url[1]:

		url = url.split('|')
		
		title = url[0]
		new_price = url[1]
		old_price = ''
		categories = url[2]
		thumb = IMG_URL+url[3]
		small = IMG_URL+url[3]
		image = IMG_URL+url[3]
		media_gallery = IMG_URL+url[3]
		short_desc = url[4]
		long_desc = url[5]
		
		sku = title.replace(' ','').lower()
		new_start = '2015-1-01'
		new_end = '2020-01-01'
		special_start = '2015-1-01'
		special_end = '2020-01-01'

		row = [sku,'Default','simple','admin',title,long_desc,short_desc,old_price,new_price,99999,1,1,1,1,'Catalog, Seach','Product Info Column',0,categories, thumb, small, image, media_gallery,special_start,special_end,new_start,new_end]
		wr.writerow(row)
		
	cnt += 1

