import scrapy
from selenium import webdriver
from selenium.webdriver import Chrome
import pandas as pd
from selenium.webdriver.chrome.options import Options

import string 
import time

driver = webdriver.Chrome()
start_url = 'http://www.ebay.in/sch/allcategories/all-categories'  #all categories page
driver.get(start_url)


category = driver.find_elements_by_xpath("//a[@class='ch']")
print len(category)

df = pd.read_csv('auction.csv')

cv = pd.DataFrame()
v = pd.read_csv('a.csv')
l = v['c'].iloc[-1]


for c in xrange(l,len(category)):
    driver.get(start_url)  #contains all categories
    driver.find_elements_by_xpath("//a[@class='ch']")[c].click()  #click the i-th category
    
    
    df.to_csv('auction.csv',index=False)
    cv = cv.append({'c':c},ignore_index=True).astype(int)
    cv.to_csv('a.csv',index=False)
    
    try:
        driver.find_element_by_xpath("//a[text()='Auction']").click()
        driver.find_element_by_xpath('//li[@class="dropdown"]/a').click()
        driver.find_element_by_xpath("//ul[@role='menu']//a/span[text()='Gallery view']").click()
    except:
        print 'w'

    
    if driver.find_element_by_xpath("//span[@class='listingscnt']").text.encode('utf-8') == '0 listings':
        print driver.find_element_by_xpath("//span[@class='listingscnt']").text.encode('utf-8')
        continue
    while True:
        sel = scrapy.Selector(text=driver.page_source)   #1st product page
        t = driver.current_url.encode('utf-8')
        if '_pgn=53' in t: 
            break
            
        for prod in sel.xpath('//ul[@id="GalleryViewInner"]/li/div'):
            item = {}
            title = prod.xpath('.//div[@class="gvtitle"]/h3/a/text()').extract()
            item['title'] = title[0].encode('utf-8') 
            mylist = prod.xpath('.//div[@class="gvprices"]//text()').extract()
            if mylist==[]:
                mylist = prod.xpath('.//div[@class="gvprices1"]//text()').extract()
            price = [i for i in xrange(0,len(mylist)) if any(letter in mylist[i] for letter in 'Rs.')]
            if price!=[]:
                price = (mylist[price[0]] + mylist[price[0]+1]).encode('utf-8')
            item['price'] = price
            item['bids'] = prod.xpath('.//div[@class="gvprices"]//span[@class="lbl gvformat"]/text()').extract()[0].encode('utf-8')
            image = prod.xpath('.//div[@class="multiImgHolder wpr"]//img/@src').extract() + prod.xpath('.//div[@class="multiImgHolder wpr"]//img/@imgurl').extract()

            pic = []
            
            for i in xrange(0,len(image)):
                if '.jpg' in image[i]:
                    pic = image[i]
                    break
 
                     
            item['image_link'] = pic
            text = title[0].encode('utf-8')
            categories = driver.find_element_by_xpath("//ul[@class='breadcrumb bc-cat']").text.encode('utf-8')
            
            item['main_category'] = categories.split('>')[0]
            item['sub-category'] = categories.split('>')[1]
            all=string.maketrans('','')
            nodigs=all.translate(all, string.digits)
            try:
                item['bids'] = item['bids'].translate(all, nodigs) 
            except:
                print 'y'
            try:
                item['price'] = item['price'].translate(all, nodigs)
            except:
                print 'q'
                
#             driver.find_element_by_xpath("//div[@class='gvtitle']/h3/a[text()='%s']" % text).click()

#             cat1 =  driver.find_element_by_xpath("//li[@itemprop='itemListElement']/a").text 
#             cat2 = driver.find_element_by_xpath("//li[@itemprop='itemListElement']/a[@class='scnd']").text  #category
#             item['category'] = (cat1+', '+cat2).encode('utf-8') 
#             next = driver.find_element_by_xpath("//div[@class='mbg']/a")
#             item['seller_name'] = next.text.encode('utf-8') 
#             item['seller_link'] = next.get_attribute("href").encode('utf-8')
#             next.click()
#             item['seller_products'] = driver.find_element_by_xpath("//span[@class='sell_count']/a").text.encode('utf-8') 
            df = df.append(item, ignore_index=True)
#             print item
#             driver.execute_script("window.history.go(-2)")   #Go Back 
#        next = driver.find_element_by_xpath('//td[@class="pagn-next"]/a')  #=> td class = 'pagn-next' 
        
        # if there exist no 'next' 'button' itself
        try: 
            if prod.xpath('//td[@class="pagn-next"]/a/@href').extract()[0].encode('utf-8') == 'javascript:;':
                break     
            else:
                url = prod.xpath('//td[@class="pagn-next"]/a/@href').extract()[0].encode('utf-8')
                driver.get(url)
        except:
            break


          