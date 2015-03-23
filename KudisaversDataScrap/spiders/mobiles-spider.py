import scrapy
import sys

import KudisaversDataScrap.items as Items

import urlparse
import urllib

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False


class MobilesSpider(scrapy.Spider):
    name = "mobiles"
    allowed_domains = ['kara.com.ng', 'kaymu.com.ng', 'jumia.com.ng', 'regalbuyer.com' ]
    start_urls = [
        "http://www.kaymu.com.ng/"
    ]

    reqFile = open("mobiles-requests.log", "w")

    siteScrappers = {
        'kara' : 'self.karaScrap',
        'kaymu' : 'self.kaymuScrap',
        'jumia' : 'self.jumiaScrap',
        'regalbuyer' : 'self.regalbuyerScrap'
    }

    dataProfile = {
        'Brands':  { #Categorize by brands
            'kara' : 'http://www.kara.com.ng/phones-and-tablets.html', #filter by 'phone' keyword in list
            'kaymu' : 'http://www.kaymu.com.ng/mobile-phones-tablets/mobile-phones/',
            'jumia' : 'http://www.jumia.com.ng/all-brands/',
            'regalbuyer' : 'http://regalbuyer.com/smart-phones-in-nigeria.html' #categorize by mapping brand in the name
        },

        'Accessories' : {

            'Headphones & Headsets' : ['http://www.kaymu.com.ng/mobile-phones-tablets/headphones-headsets-bluetooth/',
                                       'http://www.jumia.com.ng/earphones-headsets/'
            ], #tag by keyword bluetooth
            'Chargers' : ['http://www.kaymu.com.ng/mobile-phones-tablets/chargers/',
                          'http://www.jumia.com.ng/mobile-phone-chargers-adaptors/'
            ],
            'Memory cards' : ['http://www.kaymu.com.ng/mobile-phones-tablets/mobile-tablet-memory-cards/',
                              'http://www.jumia.com.ng/mobile-phone-memory-cards/'
            ],
            'Batteries' : ['http://www.kaymu.com.ng/mobile-phones-tablets/mobile-tablet-batteries/',
                           'http://www.jumia.com.ng/mobile-phone-batteries/'
            ],
            'Cases & Covers' : ['http://www.kaymu.com.ng/mobile-phones-tablets/covers-cases-pouches/',
                                'http://www.jumia.com.ng/mobile-phones-cases-covers/'
            ],
            'Power Banks' : ['http://www.kaymu.com.ng/mobile-phones-tablets/power-banks/',
                             'http://www.jumia.com.ng/mobile-phone-accessories-power-banks/'
            ],
            'Car accessories' : ['http://www.jumia.com.ng/mobile-phones-car-accessories/'
            ],
            'Sim Cards' : ['http://www.jumia.com.ng/sim-cards/'
            ],
            'Stylus' : ['http://www.jumia.com.ng/stylus/'
            ],
            'Screen protectors' : ['http://www.kaymu.com.ng/mobile-phones-tablets/mobile-tablet-screens/',
                                   'http://www.jumia.com.ng/surface-screen-protector/'
            ],

            'Bluetooth Accessories' : ['http://www.kaymu.com.ng/mobile-phones-tablets/mobile-tablet-screens/',
                                   'http://www.jumia.com.ng/surface-screen-protector/'
            ],

        }

    }

    logFile = open("mobiles-log.log", "w")
    sys.stdout = logFile
    reqFile = open("mobiles-requests.log", "w")
    errorFile = open("mobiles-errors.txt", "w")

    def parse(self, response):
        try:
            sites = self.dataProfile['Brands']
            for (site,siteUrl) in sites.iteritems():
                self.reqFile.write(siteUrl + '\n')
                request = scrapy.Request(siteUrl, callback=self.parse_site, meta={'site': site})
                yield request
        except Exception, e:
            v=str(e)
            self.errorFile.write(v + '\n')

    def parse_site(self, brandResponse):
        try:
            sel = brandResponse.selector
            thisSite = brandResponse.meta['site']

            for case in switch(thisSite):
                if case('kara'): #
                    brandLinks =[i for i in sel.xpath('//dl[@id="narrow-by-list2"]/dd/ol/li/a') if str(i.xpath('text()')[0].extract()).split()[-1] in  ['Phones','Iphones', 'phones', 'Mobile','Galaxy','Xperia']]
                    for thisBrand in brandLinks:
                        brandName = str(thisBrand.xpath('text()')[0].extract()).split()[0].encode('ascii', 'ignore')
                        brandUrl = str.strip(str(thisBrand.xpath('@href')[0].extract()))
                        self.reqFile.write(brandUrl + '\n')
                        request = scrapy.Request(brandUrl, callback= self.scrapSiteBrand, meta={'brand' : brandName, 'site' : 'kara' })
                        yield request
                    break
                if case('kaymu'): #kaymu
                    brandLinks = sel.xpath('//ul[@class="cnv-childs cnv-subCat-2"]/li/a')
                    for thisBrand in brandLinks:
                        brandName = str(thisBrand.xpath('span/text()')[0].extract()).split(" ")[0].encode('ascii', 'ignore')
                        brandUrl =  'http://www.kaymu.com.ng' + str.strip(str(thisBrand.xpath('@href')[0].extract()))
                        self.reqFile.write(brandUrl + '\n')
                        request = scrapy.Request(brandUrl, callback= self.scrapSiteBrand, meta={'brand' : brandName, 'site' : 'kaymu' })
                        yield request
                    break
                if case('jumia'): #jumia
                    brandLinks = sel.xpath('//ul[@id="facet_brand-top"]/li/a')
                    for thisBrand in brandLinks:
                        brandName = str.strip(str(thisBrand.xpath('@title')[0].extract().encode('ascii', 'ignore')))
                        brandUrl = str.strip(str(thisBrand.xpath('@href')[0].extract()))
                        self.reqFile.write(brandUrl + '\n')
                        request = scrapy.Request(brandUrl, callback= self.scrapSiteBrand, meta={'brand' : brandName, 'site' : 'jumia' })
                        yield request
                    break
                if case('regalbuyer'): #regalbuyer
                    brandLinks = sel.xpath('//dl[@id="narrow-by-list2"]/dd/ol/li/a')
                    for thisBrand in brandLinks:
                        brandName = str.strip(str(thisBrand.xpath('text()')[0].extract()))
                        brandUrl = str.strip(str(thisBrand.xpath('@href')[0].extract()))
                        self.reqFile.write(brandUrl + '\n')
                        request = scrapy.Request(brandUrl, callback= self.scrapSiteBrand, meta={'brand' : brandName, 'site' : 'regalbuyer' })
                        yield request
                    break
                if case(): pass
        except Exception, e:
            v=str(e)
            self.errorFile.write(v + '\n')



    def scrapSiteBrand(self, siteBrandResponse):
        try:
            sel = siteBrandResponse.selector
            thisPageUrl = siteBrandResponse.url

            section = 'Mobiles'
            cateogry = 'Brands'
            prodType = siteBrandResponse.meta['brand']
            site = siteBrandResponse.meta['site']

            item_info = dict()
            item_info['section'] = section
            item_info['cateogry'] = cateogry
            item_info['prodType'] = prodType

            siteSpecifics = dict()
            siteSpecifics = {
                'regalbuyer' : {'numPages' : "len(sel.xpath('//div[@class=\"pages\"]')[0].xpath('ol/li/a'))", 'param' : '?p='},
                'jumia' : {'numPages' : "int(sel.xpath('//div[@class=\"button-see-more txtCenter\"]/@data-total-pages').extract()[0])" , 'param' : '?page='},
                'kaymu' : {'numPages' : "int(str(sel.xpath('//li[@class=\"ui-listItem\"]/a[contains(@title, \"Last\")]/@href')[0].extract()).split(\"=\")[1])", 'param' : '?page='},
                'kara' : {'numPages' : "len(sel.xpath('//div[@class=\"pages\"][1]/ol/li'))", 'param' : "?p="}
            }

            try:
                numPages = eval(siteSpecifics[site]['numPages'])
            except:
                numPages = 1
            finally:
                for pageNum in range(1, numPages+1):
                    parsePageUrl = urlparse.urlparse(thisPageUrl).geturl() + siteSpecifics[site]['param'] + str(pageNum)
                    self.reqFile.write(parsePageUrl + '\n')
                    request = scrapy.Request(parsePageUrl, callback=eval(self.siteScrappers[site]), dont_filter=True, meta={'item_info': item_info })
                    yield request
        except Exception, e:
            v=str(e)
            self.errorFile.write(v + '\n')

    def karaScrap(self, karaPageResponse):
        try:
            sel = karaPageResponse.selector
            item_info = karaPageResponse.meta['item_info']
            products = sel.xpath('//ul[@class="products-grid category-products-grid"]/li[@class="item last"]')
            for product in products:
                prodUrl = str(product.xpath('div/a/@href')[0].extract())
                request = scrapy.Request(prodUrl, callback=self.karaProdScrap, meta={'item_info': item_info })
                yield request
        except Exception, e:
            v=str(e)
            self.errorFile.write(v + '\n')


    def karaProdScrap(self, karaProdResponse):
        try:
            sel = karaProdResponse.selector
            item_info = karaProdResponse.meta['item_info']
            item_mobile = Items.ProductItem()
            item_mobile['site'] = 'kara'
            item_mobile['section'] = item_info['section']
            item_mobile['cateogry'] = item_info['cateogry']
            item_mobile['prodType'] = item_info['prodType']
            item_mobile['brand'] = item_info['prodType']
            item_mobile['prodUrl'] = karaProdResponse.url

            item_mobile['prodName'] = " ".join(str.strip(str(sel.xpath('//div[@class="product-name"]/h2/text()')[0].extract().encode('ascii','ignore'))).split())
            item_mobile['availability'] = 'In Stock'
            item_mobile['imageLink'] = str(sel.xpath('//p[@class="product-image"]/a/img/@src')[0].extract())

            try:
                item_mobile['price'] = float(str.strip(str(sel.xpath('//span[@class="regular-price"]/span/text()')[0].extract().encode('ascii','ignore'))).replace(",",""))
                discount = ''
            except:
                item_mobile['price'] = float(str.strip(str(sel.xpath('//p[@class="special-price"]/span/text()')[1].extract().encode('ascii','ignore'))).replace(",",""))
                oldPrice = float(str.strip(str(sel.xpath('//p[@class="special-price"]/span/text()')[1].extract().encode('ascii','ignore'))).replace(",",""))
                discount = str(float((item_mobile['price']/oldPrice - 1)*100)) + '%'
            finally:
                item_mobile['discount'] = discount
            try:
                prodProperties = "#".join([str(i) for i in sel.xpath('//div[@class="std"]/ul/li/span/text()').extract()])
            except:
                prodProperties = ''
            finally:
                item_mobile['prodProperties'] = prodProperties

            yield item_mobile

        except Exception, e:
            v=str(e)
            self.errorFile.write(v + '\n')


    def kaymuScrap(self, kaymuPageResponse):
        try:
            sel = kaymuPageResponse.selector
            item_info = kaymuPageResponse.meta['item_info']
            products = sel.xpath('//div[@id="productsCatalog"]/div')
            for product in products:
                prodUrl = 'http://www.kaymu.com.ng' + str(product.xpath('div/a/@href')[0].extract())
                request = scrapy.Request(prodUrl, callback=self.kaymuProdScrap,
                                                              meta={'item_info': item_info })
                yield request
        except Exception, e:
            v=str(e)
            self.errorFile.write(v + '\n')

    def kaymuProdScrap(self, kaymuProdResponse):
        try:
            sel = kaymuProdResponse.selector
            item_info = kaymuProdResponse.meta['item_info']
            item_mobile = Items.ProductItem()
            item_mobile['site'] = 'kaymu'
            item_mobile['section'] = item_info['section']
            item_mobile['cateogry'] = item_info['cateogry']
            item_mobile['prodType'] = item_info['prodType']
            item_mobile['brand'] = item_info['prodType']
            item_mobile['prodUrl'] = kaymuProdResponse.url

            item_mobile['prodName'] = " ".join(str.strip(str(sel.xpath('//span[@class="prd-title"]/text()')[0].extract().encode('ascii','ignore'))).split())
            item_mobile['price'] = float(str.strip(str(sel.xpath('//span[@id="price_box"]/text()')[0].extract().encode('ascii','ignore'))).replace(",",""))
            item_mobile['availability'] = 'In Stock'
            item_mobile['imageLink'] = str(sel.xpath('//div[@id="prdImage"]/span/span/img/@src')[0].extract())

            try:
                discount =  str.strip(str(sel.xpath('//div[@class="itm-flag itm-saleFlagPercent"]/span/text()')[0].extract()))
            except:
                discount = ''
            finally:
                item_mobile['discount'] = discount
            try:
                prodProperties = "#".join([str(i).strip() for i in sel.xpath('//table[@class="attributeTable"]/tr/td/text()').extract()]).replace(":#",":")
            except:
                prodProperties = ''
            finally:
                item_mobile['prodProperties'] = prodProperties

            if(item_mobile['brand'] == "Other"):
                brand =  (prodProperties.split("#")[[v.split(":")[0]   for v in prodProperties.split("#")].index("Brand")]).split(":")[1]
                if(brand=="Other"):
                    brand = item_mobile['prodName'].split(" ")[0]
                item_mobile['brand'] = brand
                item_mobile['prodType'] = brand

            yield item_mobile

        except Exception, e:
            v=str(e)
            self.errorFile.write(v + '\n')



    def jumiaScrap(self, jumiaPageResponse):
        try:
            sel = jumiaPageResponse.selector
            item_info = jumiaPageResponse.meta['item_info']
            products = sel.xpath('//ul[@id="productsCatalog"]/li')
            for product in products:
                prodUrl =str(product.xpath('div/a/@href')[0].extract())
                request = scrapy.Request(prodUrl, callback=self.jumiaProdScrap,
                                                              meta={'item_info': item_info })
                yield request
        except Exception, e:
            v=str(e)
            self.errorFile.write(v + '\n')

    def jumiaProdScrap(self, jumiaProdResponse):
        try:
            sel = jumiaProdResponse.selector
            item_info = jumiaProdResponse.meta['item_info']
            item_mobile = Items.ProductItem()
            item_mobile['site'] = 'jumia'
            item_mobile['section'] = item_info['section']
            item_mobile['cateogry'] = item_info['cateogry']
            item_mobile['prodType'] = item_info['prodType']
            item_mobile['brand'] = item_info['prodType']
            item_mobile['prodUrl'] = jumiaProdResponse.url

            item_mobile['prodName'] = " ".join(str.strip(str(sel.xpath('//span[@class=" prd-title ltr-content"]/text()')[0].extract().encode('ascii','ignore'))).split())
            item_mobile['price'] = str.strip(str(sel.xpath('//span[@id="price_box"]/span[2]/text()')[0].extract()))
            item_mobile['availability'] = 'In Stock'
            item_mobile['imageLink'] = str(sel.xpath('//img[@id="prdImage"]/@src')[0].extract())

            try:
                discount =  str.strip(str(sel.xpath('//span[@id="product_saving_percentage"]/text()')[0].extract()))
            except:
                discount = ''
            finally:
                item_mobile['discount'] = discount
            try:
                prodProperties = ("#".join(sel.xpath('//div[@class="usp-shortdescr usp-list-spacing usp-font-text"]/ul/li/text()').extract()))
            except:
                prodProperties = ''
            finally:
                item_mobile['prodProperties'] = prodProperties

            yield item_mobile

        except Exception, e:
            v=str(e)
            self.errorFile.write(v + '\n')


    def regalbuyerScrap(self, regalbuyerPageResponse):
        try:
            sel = regalbuyerPageResponse.selector
            item_info = regalbuyerPageResponse.meta['item_info']
            products = sel.xpath('//div[@class="category-products"]/ul/li')
            for product in products:
                prodUrl = str(product.xpath('a/@href')[0].extract())
                request = scrapy.Request(prodUrl, callback=self.regalbuyerProdScrap,
                                                              meta={'item_info': item_info })
                yield request
        except Exception, e:
            v=str(e)
            self.errorFile.write(v + '\n')

    def regalbuyerProdScrap(self, regalbuyerProdResponse):
        try:
            sel = regalbuyerProdResponse.selector

            item_info = regalbuyerProdResponse.meta['item_info']
            item_mobile = Items.ProductItem()
            item_mobile['site'] = 'regalbuyer'
            item_mobile['section'] = item_info['section']
            item_mobile['cateogry'] = item_info['cateogry']
            item_mobile['prodType'] = item_info['prodType']
            item_mobile['brand'] = item_info['prodType']
            item_mobile['prodUrl'] = regalbuyerProdResponse.url
            item_mobile['prodName'] = " ".join(str(sel.xpath('//div[@class="product-name"]/h1/text()').extract()[0].encode('ascii','ignore')).split())
            item_mobile['price'] = sel.xpath('//span[@class="price"]/text()')[0].extract().encode('ascii', 'ignore')
            item_mobile['availability'] = str(sel.xpath('//div[@class="product-shop"]/p/span/text()')[0].extract())
            item_mobile['imageLink'] = str(sel.xpath('//p[@class="product-image"]/a/@href')[0].extract())

            yield item_mobile

        except Exception, e:
            v=str(e)
            self.errorFile.write(v + '\n')