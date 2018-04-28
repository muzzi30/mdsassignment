from bs4 import BeautifulSoup
import urllib.request
from time import sleep
from datetime import datetime
import pandas as pd
import re
import math

def getWeather():
	#time temperature, humidity and pressure from the following website
	weather = []
	url = "https://weather.com/weather/today/l/ASXX0075:1:AS"
	req = urllib.request.urlopen(url)
	page = req.read()
	scraping = BeautifulSoup(page,'lxml')
	#time:
	#<strong>Melbourne at Wednesday 9:50am EST</strong> --> 9:50am and convert it into 24 hours' format
	tmp = scraping.findAll("p",attrs={"class":"today_nowcard-timestamp"})[0].text
	time = (re.findall('[0-9]+:[0-9]+', tmp))[0]
	#hour = int(time.split(':')[0])
	#if tmp.find('pm') != -1: 
		#time = time.replace(str(hour)+':',str(hour+12)+':')
	weather.append(time)
    #tempreture:
	#from <h3>19.7°C</h3> extract 19.7
	tmp = scraping.findAll("div",attrs={"class":"today_nowcard-temp"})[0]
	temp = tmp.findAll("span")[0].text
	saj = int(temp.replace('°',''))
	saj = ((saj - 32)*5)/9
	sajc = round(saj, 1)
	weather.append(sajc)
    
    #humidity and pressure:
	tmp = scraping.findAll("tbody")[0]
	ttmp = tmp.findAll("tr")[1]
	#for itm in ttmp:
	#	if itm.text.find("Humidity") != -1:
			#humidity:
			#from <div class="value">78%</div> extract 78
	humi = ttmp.findAll("span")[0].text
	humi = humi.replace('%','')
	humi = '0.'+humi
	weather.append(humi)
    
#if itm.text.find("Pressure") != -1:
			#pressure:
			#from <div class="value">1016.9hPa</div> extract 1016.9
	ttmp = tmp.findAll("tr")[3]
	pres = ttmp.findAll("span")[0].text
	mbpre = float (pres.replace('in',''))
	mbpre1 = mbpre * 33.8639
	mbpre2 = round(mbpre1, 1)
	weather.append(mbpre2)

	return weather

if __name__ == '__main__':
	print("Collecting 10 Weather Data in a Interval of 1 Hour")
	idx = 0
	weatherdata = {'time':[], 'temp':[], 'rh':[], 'pressure':[]}
	while idx < 10:
		print('collecting weather data '+str(idx))
		tmp = getWeather()
		weatherdata['time'].append(tmp[0])
		weatherdata['temp'].append(tmp[1])
		weatherdata['rh'].append(tmp[2])
		weatherdata['pressure'].append(tmp[3])
		idx += 1
		#collect data every 1800 seconds
		sleep(1800)
	data = pd.DataFrame(weatherdata)
	data.to_csv(r'c:\Users\mypc\Desktop\mds\weather_interval_test.csv',index=False)
	print('Endo of Test')
	
	
	