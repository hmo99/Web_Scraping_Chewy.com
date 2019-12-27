from scrapy import Spider, Request
from chewy.items import ChewyItem
import re, time
import math

i = 0

class ChewySpider(Spider):
	name='chewy_spider'  #This name will be used for generating files??
	allowed_urls=['https://www.chewy.com']

	#start with the all the dog food
	start_urls=['https://www.chewy.com/s?rh=c%3A288%2Cc%3A332&page=1']
#
	print ("#"*50,'in the start url',"#"*50)




	def parse(self, response):
		# Find number_pages
		text=response.xpath('//p[@class="results-count"]/text()').extract_first()
		_, items_per_page, total_items=re.findall('\d+', text)
		number_pages = math.ceil(int(total_items) / int(items_per_page))

		# all urls for top food pages
		result_urls=['https://www.chewy.com/s?rh=c%3A288%2Cc%3A332&page='+ str(i) for i in range(1,number_pages+1 )]


		#TEST FIRST PAGE
		for url in result_urls:
			print('#'*100)
			print('\n we are in page {}'.format(url[-2:]))
			print ( '#'*100)
			yield Request(url=url, callback=self.parse_result_page)

	def parse_result_page(self, response):

		
		detail_urls=response.xpath('//article[@class="product-holder js-tracked-product  cw-card cw-card-hover"]/a/@href').extract()                                 
		productCountOfPage=1

		#Test first 2 products on each catalog page
		for url in detail_urls:   
			print('#'*50,'\n', 'we are on the ', productCountOfPage, 'th product', '#'*50,'\n' )
			yield Request(url='https://www.chewy.com/' + url, callback=self.parse_detail_page)
			productCountOfPage=+1

	def parse_detail_page(self, response):
		global i
			#parse product page
		try: 
			#if there is review

			num_of_reviews=int(response.xpath('//div//span[@class="hide-large"]/text()').extract_first())
			percentRec=int((re.findall('\d+', response.xpath('//div[@class="ugc-list__recap__recommend"]/p/span').extract()[0]))[0])

			#when <10 review
			if num_of_reviews<=10:

				print ("####"*50, '\n WHEN <<<<<<<10 REVIEW \n',"####"*50)
				#Top product info
				productName=(response.xpath('//div[@id="product-title"]/h1/text()').extract()[0]).strip()
				brandName=response.xpath('//span[@itemprop="brand"]/text()').extract()[0]
				price=float(response.xpath('//span[@class="ga-eec__price"]/text()').extract()[0].strip().split('$')[1])

				#bottom review info
				reviews=response.xpath('//li[@class="js-content"]')
				for review in reviews: 
					date=review.xpath('.//span/@content').extract()		
					reviewRating=int(review.xpath('.//@alt').extract()[0].split()[0])
					reviewTitle=(review.xpath('.//h3/text()').extract())
					reviewContent=review.xpath('.//span[@class="ugc-list__review__display"]/text()').extract()

					item=ChewyItem()
					item['productName']=productName
					item['brandName']=brandName
					item['price']=price
					item['num_of_reviews']=num_of_reviews
					

		
					item['date']=date
					item['reviewRating']=reviewRating
					item['reviewTitle']=reviewTitle
					item['reviewContent']=reviewContent
					item['percentRec']=percentRec

					print('\n\n\n')
					print('*'*25,    i    ,'*'*25)
					print('\n\n\n')
					time.sleep(0.5)

					yield item
					i = i + 1




			else:
				# print ("####"*50, '\n WHEN >>>>>10 REVIEW \n',"####"*50)
				first_review_page=response.xpath('//footer[@class="ugc-list__footer js-read-all"]/a/@href').extract()[0]
				review_page_num=math.ceil(num_of_reviews/10)
				review_urls=[first_review_page[:-1]+ str(i) for i in range(1,review_page_num+1) ]
				
				#Top product info
				brandName=response.xpath('//span[@itemprop="brand"]/text()').extract()[0]
				productName=(response.xpath('//div[@id="product-title"]/h1/text()').extract()[0]).strip()
				price=float(response.xpath('//span[@class="ga-eec__price"]/text()').extract()[0].strip().split('$')[1])

				# print(type(brandName))
				# print(type(productName))

				#bottom review section, go to review_page and pass top product info
				
				for url1 in review_urls: #test first 1
					new_url='https://www.chewy.com' + url1

				
					yield Request(url= new_url, meta={'brandName': brandName, 'productName':productName, "price":price, "num_of_reviews":num_of_reviews, 'percentRec':percentRec}, callback = self.parse_review_page)
					#yield Request(url = new_url, callback=self.parse_review_page )
					# print('hello!')


		except Exception as e:
			return

			 

	def parse_review_page(self, response):
		#parse the review pages
		global i

		print('IN THE PARSE REVIEW PAGE')
		
		print ("####"*50)
		productName=response.meta['productName']
		brandName=response.meta['brandName']
		price=response.meta['price']
		num_of_reviews=response.meta['num_of_reviews']
		percentRec=response.meta["percentRec"]

		#extract all review tags
		reviews=response.xpath('//li[@class="js-content"]')


		for review in reviews:  #test review
			
			date=review.xpath('.//span/@content').extract()
			reviewRating=int(review.xpath('.//@alt').extract()[0].split()[0])
			reviewTitle=(review.xpath('.//h3/text()').extract())[0].strip()
			reviewContent=review.xpath('.//span[@class="ugc-list__review__display"]/text()').extract()
					

			item=ChewyItem()
			item['productName']=productName
			item['brandName']=brandName
			item['price']=price
			item['num_of_reviews']=num_of_reviews

			item['date']=date
			item['reviewRating']=reviewRating
			item['reviewTitle']=reviewTitle
			item['reviewContent']=reviewContent
			item['percentRec']=percentRec

	
			print('\n\n\n')
			print('*'*25,'  collected total review count:  ',i,'    ','*'*25)
		# 	print('\n\n\n')
		# 	time.sleep(0.5)
			yield item
		i = i + 1




