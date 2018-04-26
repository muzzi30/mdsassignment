from bs4 import BeautifulSoup
import urllib.request
from time import sleep
from datetime import datetime
import pandas as pd
import re

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
	print("Collecting 10 Weather Data by Tempreture Change of more than 1°C")
	idx = 0
	weatherdata = {'time':[],'tempreture':[],'humidity':[],'pressure':[]}
	while idx < 10:
		tmp = getWeather()
		oldtempreture = -100
		currtempreture = float(tmp[1])
		if idx != 0:
			oldtempreture = float(weatherdata['tempreture'][idx-1])
		currtempreture = float(tmp[1])
		#collect data if tempreture change is lareger than 1
		if abs(currtempreture - oldtempreture) < 1: sleep(60); continue
		print('collecting weather data '+str(idx))
		print('	weather changes from '+str(oldtempreture)+' to '+str(currtempreture))
		weatherdata['time'].append(tmp[0])
		weatherdata['tempreture'].append(tmp[1])
		weatherdata['humidity'].append(tmp[2])
		weatherdata['pressure'].append(tmp[3])
		idx += 1
		sleep(60)
	data = pd.DataFrame(weatherdata)
	data.to_csv(r'C:\Users\mypc\Desktop\mds\weather_change_test.csv', index=False)
	print('Endo of Test')
