# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 16:33:39 2020

@author: KIIT
"""

#imports
import bs4 as bs
import urllib.request as req
import re
import pandas as pd

#requesting url for search query-Iphone in Amazon
src = req.urlopen('https://www.amazon.in/s?k=iphone&ref=nb_sb_noss').read()
soup = bs.BeautifulSoup(src, 'lxml')

#finding individual links for all the products in the page
containers = soup.find_all('a', {'class': 'a-link-normal s-no-outline'})

links = []
for x in containers:
    links.append('https://www.amazon.in' + str(x).split('"')[3])
    
Name = []
Ratings = []
Price = []
specs = []
Image = []

for x in links:
    #requesting urls for individual products
    srcc = req.urlopen(x).read()
    soupp = bs.BeautifulSoup(srcc, 'lxml')
    #scraping product specifications
    prod_specs = []
    lsts = soupp.find_all('span', {'class': 'a-list-item'})
    for li in lsts[23:36]:
        prod_specs.append(re.sub('\n', '', li.text.strip()))
    specs.append(prod_specs)
    #scraping product ratings
    rate = soupp.find('span', {'class': 'a-icon-alt'})
    Ratings.append(rate.text)
    #scraping product name
    prod_name = soupp.find('h1', {'class': 'a-size-large a-spacing-none'})
    Name.append(re.sub('\xa0', ' ', prod_name.text.strip()))
    #scraping product price
    prod_price = soupp.find('span', {'class': 'a-size-medium a-color-price priceBlockBuyingPriceString'})
    Price.append(re.sub('\xa0','',prod_price.text))
    
#scraping product image thumbnail
img = soup.find_all('img', {'class': 's-image'})
for x in img:
    Image.append(re.sub('src=', '', str(x).split(' ')[15]))
    
#converting the scraped lists into a dataframe
df = pd.DataFrame(list(zip(Name, Image, Ratings, Price, specs)),
                  columns = ['Name', 'Image', 'Ratings', 'Price', 'Specs'])

#converting the dataframe into a JSON file
df.to_json('AmazonDataset-Iphone.json')