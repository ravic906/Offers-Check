import requests
from bs4 import BeautifulSoup
from telethon import TelegramClient
from datetime import datetime

api_id= 29000080
api_hash='51397438c07ba4da64d9f8521dfdb7b2'
k=0
old_text = None
print('Scraping started at:',datetime.now())
with TelegramClient('newestone', api_id, api_hash,timeout=3600) as client:    
    while 1:
    	if int(datetime.now().strftime('%M'))%10==0:
	        html_doc = requests.get('https://www.desidime.com/new').text
	        bs = BeautifulSoup(html_doc,'html.parser')
	        x=bs.findAll('div',"deal-url",limit=5)            
	        i=x[0]
	        if ('kettle' in i.text.lower() or 'diaper' in i.text.lower() or 'toothpaste' in i.text.lower()) and i.text!=old_text:
	            old_text=i.text
	            k=k+1
	            link=i.find('a').get('href')
	            print('Scraping a deal for you!')
	            client.loop.run_until_complete(client.send_message('ravic906',i.text+'\n'+link))
	            print('Found '+ str(k)+ ' deal(s)!')
