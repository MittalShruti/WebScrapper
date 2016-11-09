import scrapy
from selenium import webdriver

class product_spiderItem(scrapy.Item):
    title = scrapy.Field()
    price=scrapy.Field()
    image_link=scrapy.Field()
    pass

driver = webdriver.Chrome()
driver.get('http://www.ebay.in/sch/i.html?_sacat=0&_from=R40&_nkw=python&rt=nc&_dmd=2')
products = product_spiderItem()
products['title']='Title'
products['price']='Price'
products['image_link']='Link to Image'
products = [products]
while True: 
    sel = scrapy.Selector(text=driver.page_source)
    for prod in sel.xpath('//ul[@id="GalleryViewInner"]/li/div'):  
        item = product_spiderItem()
        item['title'] = prod.xpath('.//div[@class="gvtitle"]/h3/a/text()').extract()
        mylist = prod.xpath('.//div[@class="gvprices"]//text()').extract()     
        h = [i for i in xrange(0,len(mylist)) if any(letter in mylist[i] for letter in 'Rs.')]
        price = mylist[h[0]] + mylist[h[0]+1]
        item['price']=price
        image = prod.xpath('.//div[@class="multiImgHolder wpr"]//img/@src').extract() + prod.xpath('.//div[@class="multiImgHolder wpr"]//img/@imgurl').extract()
        item['image_link'] = [img for img in image if all(letter in img for letter in 'jpg')]
        products.append([item])
    print i
    next = driver.find_element_by_xpath('//td[@class="pagn-next"]/a')  #=> td class = 'pagn-next' 
    next.click()

    if prod.xpath('//td[@class="pagn-next"]/a/@href').extract()[0].encode('utf-8') == 'javascript:;':
        break 

driver.quit()

import pickle

with open("all_products", 'wb') as f:
    pickle.dump(products, f)    

print products

