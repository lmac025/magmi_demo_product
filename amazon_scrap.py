import csv, math
from decimal import *
from amazon.api import AmazonAPI
from lxml import etree

PROJECT = 'suchgadget'
HEADER = ['sku','atrribute_set', 'type', 'store', 'name', 'description','short_description', 'price', 'special_price', 'qty', 'is_in_stock', 'manage_stock', 'use_config_manage_stock','status', 'visibility','options_container', 'weight', 'categories', 'thumbnail', 'small_image', 'image', 'media_gallery','special_from_date','special_to_date','news_from_date','news_to_date']
EXTRA = ['Size:drop_down:1','Color:drop_down:1']

AMZ_IDS = []
AMZ_ID_CATS = {}
CATEGORIES = []
SPECIALS = []
NEW = []

with open(PROJECT+'.txt', 'rU') as f:
	current_cat = None
	for line in f:
	
		line = line.replace('\n', '').replace('\r', '')
		
		if line[0] == '_':
			current_cat = line[1:]
			if current_cat not in ['Specials','New']:
				CATEGORIES.append(line[1:])		
			
		if current_cat and line[0] != '_':
			if current_cat == 'Specials':
				SPECIALS.append(line)		
			elif current_cat == 'New':
				NEW.append(line)		
			else:
				AMZ_ID_CATS[line] = current_cat
				AMZ_IDS.append(line)		
	
print 'categories: {0}'.format(len(CATEGORIES))	
print CATEGORIES
print 'products: {0}'.format(len(AMZ_IDS))	
print AMZ_IDS
		
csv_file = open(PROJECT+'.csv', 'wb')
wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
# add header fields
wr.writerow(HEADER)
		
amazon = AmazonAPI('', '', True)
#products = amazon.search(Keywords='kindle', SearchIndex='All')
products = []

div =  math.trunc(len(AMZ_IDS)/10)

ii = 0
for i in range(0, div+1):
	
	AMZ_IDS_STR = ','.join(AMZ_IDS[ii:ii+10])
	
	print AMZ_IDS_STR 
	
	try:
		new_products = amazon.lookup(ItemId=AMZ_IDS_STR)
		print new_products
	except:
		print '------------'
		print ii,ii+10
		print AMZ_IDS[ii:ii+10]
	
	ii += 10
	try:
		products.extend(new_products)
	except:
		products.append(new_products)
		
for i, product in enumerate(products):
	
	long_desc = product.editorial_review.encode('ascii', 'ignore').replace('\n', ' ').replace('\r', '')
	short_desc = ''
	for feature in product.features:
		short_desc += feature
	short_desc = short_desc.encode('ascii', 'ignore').replace('\n', ' ').replace('\r', '')
	
	images = ''
	
	print product.title
			
	try:
		categories = AMZ_ID_CATS[product.asin]
	except:
		categories = ''
		
	new_price = ''	
		
	new_start = ''
	new_end = ''
	if product.asin in SPECIALS:
		new_start = '2015-1-01'
		new_end = '2020-01-01'
	
	special_start = ''
	special_end = ''
	if product.asin in NEW:
		special_start = '2015-1-01'
		special_end = '2020-01-01'
		
		try:
			new_price = float(product.list_price[0])*0.8
		except:
			new_price = ''
			
	thumb = ''
	if product.tiny_image_url:
		thumb = product.tiny_image_url
	small = ''
	if product.small_image_url:
		if not thumb:
			thumb = product.small_image_url
		small = product.small_image_url
		
	image = ''
	if product.large_image_url:
		thumb = product.large_image_url
		small = product.large_image_url
		image = product.large_image_url
		
	media_gallery = '{0};{1};{2}'.format(thumb, small, image)
	
	sku = ''
	if product.sku:
		sku = product.sku
	else:
		sku = product.asin
	
	row = [sku,'Default','simple','admin',product.title.encode('ascii', 'ignore'),long_desc,short_desc,product.list_price[0],new_price,99999,1,1,1,1,'Catalog, Seach','Product Info Column',0,categories, thumb, small, image, media_gallery,special_start,special_end,new_start,new_end]
	wr.writerow(row) 
	