from bs4 import BeautifulSoup
import requests 
import csv
import pandas

# year = '15'
skip_list = ['0','2000','4000']

category = 'gr-qc'

start_year = 10
end_year = 15 

for year_number in range(start_year,end_year):
	year = str(year_number)
	print(year)

	output_filename = 'Arviv_GRQC_Title_' + year +'.csv'
	csv_file = open(output_filename,'w')
	csv_writer = csv.writer(csv_file)
	csv_writer.writerow(['Title'])




	for value in skip_list:
		skip = value
		

		'''Requesting the required webpage'''
		source=requests.get('https://arxiv.org/list/'+ category +'/'+ year +'?skip='+ skip +'&show=2000').text

		'''souping the html'''
		soup=BeautifulSoup(source,'lxml')

		body=soup.find('div',id='dlpage')



		'''poinitng at the dl tag which contains the list of all the papers'''
		content=body.find('dl')
		# print(content.prettify)

		# title = content.find('div',class_='list-title mathjax')
		# print(title.text)
		# article_title =title.text.split(':')
		# csv_writer.writerow([article_title[0]])


		'''extracting the titles from each row within the dl tag where the title is 
		given the class, list-title mathjax''' 	
		for title in content.find_all('div',class_='list-title mathjax'):
			article_title =title.text.split(':') ######### TO GET THE TITLE TEXT	
			csv_writer.writerow([article_title[1]])

	csv_file.close()
	print("The CSV file is ready ")
