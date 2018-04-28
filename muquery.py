import pandas as pd
import numpy as np

#compare time by minute
def compTime(a,b):
	flag = 0
	time1 = int(a.split(':')[0])*60 + int(a.split(':')[1])
	time2 = int(b.split(':')[0])*60 + int(b.split(':')[1])
	if time1 == time2: return 0
	elif time1 < time2: return 1
	else: return 2

if __name__ == '__main__':
	data = pd.read_csv(r'C:\Users\mypc\Desktop\mds\Data for both\myfuse.csv')
	while True:
		print('Please enter the time of weather (hour:minute): ')
		query = input('')
		time = data['time']
		lowbound = -1
		upbound = -1
		key = -1
		#if the query time is not in the data:
		#	1, return the earliest tempreture is query time is earlier
		#	2, return the latest tempreture is query time is later
		#if the query time is in the range of data, 
		#return the mean of its lower bound and upper bound tempreture
		for idx in range(len(time)):
			if compTime(time[idx], query) == 1: lowbound = idx
			elif compTime(time[idx], query) == 0: key = idx; break
			else: upbound = idx; break
		if key != -1: print(data['temp'][key])
		elif lowbound != -1 and upbound != -1: print(round(np.mean([float(data['temp'][lowbound]), float(data['temp'][upbound])]),2))
		elif lowbound == -1: print(data['temp'][upbound])
		else: print(data['temp'][lowbound])
	print('End of Test!')
