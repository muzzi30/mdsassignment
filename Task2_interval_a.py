from bs4 import BeautifulSoup
import urllib.request
from time import sleep
from datetime import datetime
import pandas as pd
import re

def getWeather():
	#access time temperature, wind and pressure from the following website
	weather = []
	url = "http://www.bom.gov.au/places/vic/melbourne/"
	req = urllib.request.urlopen(url)
	page = req.read()
	scraping = BeautifulSoup(page,'lxml')
	#time: 
	#from (<div class="update">Updated at 10:00 EST</div>), extract 10:00
	tmp = scraping.findAll("h3")[0].text
	time = (re.findall('[0-9]+:[0-9]+', tmp))[0]
	weather.append(time)
	#tempreture:
	#from <h3>19.7°C</h3> extract 19.7
	tmp = scraping.findAll("div", attrs={"class":"wrapper"})[0]
	temp = tmp.findAll("li",attrs={"class":"airT"})[0].text
	weather.append(temp.replace('°C',''))
	#humidity and pressure:
	tmp = scraping.findAll("table")[0]
	humi = tmp.findAll("td")[0].text
	humi = humi.replace('%','')
	humi = '0.'+humi
	weather.append(humi)
    
	pres = tmp.findAll("td")[2].text
	pres = pres.replace('hPa','')
	weather.append(pres)
	#ttmp = tmp.findAll("tbody")[0]
	#for itm in ttmp:
		#if itm.text.find("humidity") != -1:
			#humidity:
			#from <div class="value">78%</div> extract 78
	
	return weather

if __name__ == '__main__':
	print("Collecting 10 Weather Data in a Interval of 1 Hour")
	idx = 0
	weatherdata = {'time':[],'tempreture':[],'humidity':[],'pressure':[]}
	while idx < 10:
		print('collecting weather data '+str(idx))
		tmp = getWeather()
		weatherdata['time'].append(tmp[0])
		weatherdata['tempreture'].append(tmp[1])
		weatherdata['humidity'].append(tmp[2])
		weatherdata['pressure'].append(tmp[3])
		idx += 1
		#collect data every 1800 seconds
		sleep(18)
	data = pd.DataFrame(weatherdata)
	data.to_csv(r'c:\temp\weather_interval_d.csv', index=False)
	print('Endo of Test')
