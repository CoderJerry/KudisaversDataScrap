import scrapy
import sys

import KudisaversDataScrap.items as Items

import urlparse


class ComputerSpider(scrapy.Spider):
    name = "computers"
    allowed_domains = ["kara.com.ng"]
    start_urls = [
        "http://kara.com.ng/computers-accessories.html"
    ]

    categories = ['Laptops','Desktops','Tablets','Accessories','Peripherals','Storage','Softwares','Bundles']

    dataProfile = {
        'Laptops':  { #Macbooks / Notebooks & Ultrabooks / Accessories
            'kara' : 'http://kara.com.ng/computers-accessories/laptops.html',
            'kamyu' : 'http://www.kaymu.com.ng/computers/laptop/',
            'jumia' : 'http://www.jumia.com.ng/laptops/',
            'mystore' : 'http://www.mystore.com.ng/office-supplies/laptops', #categorize by mapping brand in the name
            'slot' : 'http://www.slot.ng/laptops/', #categorize by mapping brand in the name
            'regalbuyer' : 'http://www.regalbuyer.com/computers/laptops.html' #categorize by mapping brand in the name
        },
        'Desktops' : {
            'kara' : 'http://kara.com.ng/computers-accessories/desktops.html',
            'kamyu' : 'http://www.kaymu.com.ng/computers/desktop/', #Filter by product type - desktop computer
            'mystore' : 'http://www.mystore.com.ng/office-supplies/computers', #Filter by product type - desktop computer
            'regalbuyer' : 'http://regalbuyer.com/computers/desktops.html'
        },
        'Tablets' : {
            'kara' : 'http://kara.com.ng/phones-and-tablets.html', #Filter by product name - pad and tablet  | No accessories
            'kamyu' : 'http://www.kaymu.com.ng/mobile-phones-tablets/',
            #Apple tablets : /apple-tablets/
            #Android tablets : /android-tablets/
            #Windows : /windows-tablets/
            #other : other-tablets/
            # Accessories page : http://www.kaymu.com.ng/mobile-phones-tablets/phones-tablets-accessories/?model=ipad
            'mystore' : 'http://www.mystore.com.ng/product/search?search=tablet', #No ipad
            'slot' : 'http://www.slot.ng/search.php?search_query=tablet',
            #ipad : 'http://www.slot.ng/search.php?search_query=ipad'
            'regalBuyer' : 'http://regalbuyer.com/', #List given in the main page
        }
        #'Accessories' : {
            #'kara' : 'http://kara.com.ng/computers-accessories/network-devices.html', #Network and others
        #}
        }

    logFile = open("computers-log.log", "w")
    sys.stdout = logFile
    reqFile = open("computers-requests.log", "w")
    errors = open("computers-errors.txt", "w")

    def parse(self, blockResponse):
        # log_file = open("message.log","w")
        #sys.stdout = log_file
        sel = blockResponse.selector
        p = Items.ProductItem()

        laptops = sel.xpath('//div[@id="menu-header"]/ul')

