import requests 
import time
from datetime import datetime

BITCOIN_API_URL = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/INSERT_YOUR_KEY_HERE'
BITCOIN_PRICE_THRESHHOLD = 3500

def get_latest_bitcoin_price():
	response = requests.get(BITCOIN_API_URL)
	print(datetime.now() , response)
	response.raise_for_status()
	response_json = response.json()
	price = float(response_json[0]['price_usd'])
	print(price)
	return price

def post_ifttt_webhook(event , value):
	data = {'value1':value}
	ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
	res = requests.post(ifttt_event_url,json=data)
	res.raise_for_status()

def main():
	while True:
		try:
			bitcoin_price_history = []
			price = get_latest_bitcoin_price()
			date = datetime.now()
			bitcoin_price_history.append({'date':date,'price':price})
			if price<BITCOIN_PRICE_THRESHHOLD:
				post_ifttt_webhook('bitcoin_price_emergency',price)

			if len(bitcoin_price_history) == 1:
				post_ifttt_webhook('bitcoin_price_update',format_bitcoin_history(bitcoin_price_history))
			bitcoin_price_history = []
			time.sleep(300)

		except requests.exceptions.HTTPError as errh:
			print ("Http Error:",errh)
		except requests.exceptions.ConnectionError as errc:
			print ("Error Connecting:",errc)
		except requests.exceptions.Timeout as errt:
			print ("Timeout Error:",errt)
		except requests.exceptions.RequestException as err:
			print ("OOps: Something Else",err)

def format_bitcoin_history(bitcoin_price_history):
	rows = []
	for bitcoin_price in bitcoin_price_history:
		date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M:%S')
		price = bitcoin_price['price']
		row = '{} : $<b>{}<b>'.format(date,price)
		rows.append(row)

	return '<br>'.join(rows)


if __name__ == '__main__':
	main()
