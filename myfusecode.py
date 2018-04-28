import re
import numpy as np
import pandas as pd

#this function is used to tell if two features are aligned
#for example: key1 = 'humidity', key2 = 'wind',
#return False because this combination is not in the align rule
#and they should be two separate columns in the fusedata
#if key1 = 'humidity', key2 = 'rh'
#return True to indicate that 'humidity' and 'rh' are the same feature
#and their value should be merged together as one column in fusedata
def isaligned(key1, key2):
	#alignment rule
	rule = [['temp', 'tempreture'], ['humidity','rh']]
	if key1 == key2: return True
	for item in rule:
		if key1 in item and key2 in item: return True
	return False

#return True if the input feature is in the feature sets of the input dataset
#for example: dataset has a feature set ['humidity','temp','time']
#if input feature = 'humidity', return True
#if input feature = 'pressure', return False
def featInData(feat, dataset):
	#whether the input feature or 
	#it has aligned feature in the input dataset
	for itm in dataset:
		if isaligned(feat, itm): return True, itm
	return False, ''

#fuse two weather dataset into one
#the confidence of correctness of website 1 and website2
def weatherfuse(data1, data2, confidence1, confidence2):
	fusedata = {}
	#add all features in data1 into fusedata
	for feat1 in data1:
		fusedata[feat1] = []

	#add the features that not in data1 and
	#have no aligned feature in data1
	for feat2 in data2:
		if not featInData(feat2, data1):
			fusedata[feat2] = []
	
	#fuse data1 and data2 using (data1*conf1+data2*conf2)/(conf1+conf2) if their time stamps are the same
	#if not add data1 or data2 to fusedata separately with their relative time stamp
	#example: data1=[1:1, 2:2, 3:3] with confidence 0.8, data2=[1:2, 2:4, 5:5] with confidence 0.6,
	#fusedata = [1:(1*0.8+2*0.6)/(0.8+0.6), 2:(2*0.8+4*0.6)/(0.8+0.6), 3:3, 5:5]
	#		  = [1:1.43, 2:2.86, 3:3, 5:5]
	i = 0
	j = 0
	#this loop is used to fuse data1 and data2 in a time sequence,
	#for example: data1['time'] = [10:00,10:30], data2['time'] = [10:30,12:00]
	#in the first loop, i < len(data1)(2) -> time1 = 10*60+0
	#                   j < len(data2)(2) -> time2 = 10*60+30
	#time1 < time2, so add data1[0] into fusedata and i = 1
	#in the second loop, i < len(data1)(2) -> time1 = 10*60+30
	#                    j < len(data2)(2) -> time2 = 10*60+30
	#time1 = time2, so fuse data1[1] with data2[0] considering confidence, and i = 2, j = 1
	#in the third loop, i = len(data1)(2) -> time1 = 10000000
	#                   j < len(data2)(2) -> time2 = 12*60+0
	#time1 > time2, so add data2[1] into fusedata and j = 2
	#now i = 2 and j =2 the loop condition (i != len(data1) or j != len(data2)) breaks and the loop stops
	#the fusedata is [data1[0], fuse(data1[1],data2[0]), data2[1]]
	while i != len(data1) or j != len(data2):
		time1 = 10000000
		time2 = 10000000
		if i < len(data1):
			time1 = int(data1['time'][i].split(':')[0])*60 + int(data1['time'][i].split(':')[1])
		if j < len(data2):
			time2 = int(data2['time'][j].split(':')[0])*60 + int(data2['time'][j].split(':')[1])
		onedata = []
		#data1 and data2 have the same time stamp, fuse them with (data1*conf1+data2*conf2)/(conf1+conf2)
		if time1 == time2:
			for feat in fusedata:
				#no need to fuse time because they are the same
				if feat == 'time': fusedata[feat].append(data1[feat][i]); continue
				#if this feature or its aligned feature in data2
				flag, alignfeat = featInData(feat, data2)
				#if this feature also in data1
				#if this feature exist in both data1 and data2, fuse them
				if feat in data1 and flag: fusedata[feat].append(
					round((float(data1[feat][i])*confidence1 + float(data2[alignfeat][j])*confidence2) / (confidence1 + confidence2),2))
				#this feature only in data1, just add it, nothing to fuse
				elif feat in data1: fusedata[feat].append(data1[feat][i])
				#this feature only in data2, just add it, nothing to fuse
				else: fusedata[feat].append(data2[feat][j])
			i += 1
			j += 1
		#add data1 whose time is smaller as data2 has no such time stamp
		elif time1 < time2:
			for feat in fusedata:
				if feat in data1: fusedata[feat].append(data1[feat][i])
				else: fusedata[feat].append(np.nan)
			i += 1
		#add data2 whose time is smaller as data1 has no such time stamp
		else:
			for feat in fusedata:
				#find the aligned feature in fusedata
				flag, alignfeat = featInData(feat, data2)
				if flag: fusedata[feat].append(data2[alignfeat][j])
				else: fusedata[feat].append(np.nan)
			j += 1

	return fusedata

if __name__ == '__main__':
	data1 = pd.read_csv(r'C:\Users\mypc\Desktop\mds\Data for both\t_2intervaltesta.csv')
	data2 = pd.read_csv(r'C:\Users\mypc\Desktop\mds\Data for both\t_2intervaltestb.csv')
	#because I use website 1 a lot, thus I have confident to it.
	#though I seldom use data2, but it is said that oldersweather 
	#is one of the best weather app, so I trust it only a bit less.
	fusedata = weatherfuse(data1, data2, 0.8, 0.6)
	tmp = pd.DataFrame(fusedata)
	tmp.to_csv(r'C:\Users\mypc\Desktop\mds\Data for both\myfuse.csv', index=False)
	print('End of Test!')