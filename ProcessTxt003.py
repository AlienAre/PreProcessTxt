import os
import re
import numpy as np
import pandas as pd
from datetime import datetime

#DataPa = re.compile(r'^\d{1,5}\s{2,}\d{1}\s{2,}IG\D{2}\s{1}\(\d{4}\).*$')
DataPa = re.compile(r'\d{1,5}\s{2,}\d{1}\s{2,}\D{4}.*$')
TypePa = re.compile(r'ACCUMULATOR TYPE.*\d+')
CycDatePa = re.compile(r'.*THRU\s+20\d{2}\s+\D{3}\s+\d{1,2}')
Negative = re.compile(r'-')

DebtList = ['1', '2', '7', '1193']
IRSList = ['33', '35', '794']
AlList = ['335', '602', '696', '1133', '1177', '1181', '1317', '1334', '1336', '1338', '1340']

FileList = [] 

def Try_Float(num):
    try:
        floatnum = float(num)
    except ValueError:
        return num
    else:
        return floatnum

def ClList (str):
	#strip left blanks and end '\n', '\r'
	MyStr = filter(None, re.split(r'\s{2,}', str.lstrip(' ').rstrip('\n').rstrip('\r')))

	for idx in range(len(MyStr)):
		#remove front and trailing blank for each element and remove ',' seperator for numbers
		MyStr[idx] = MyStr[idx].lstrip(' ').rstrip(' ').replace(',', '')
		#update '-' to front to show correct negitive amount
		if '-' in MyStr[idx]:
			try:
				float(MyStr[idx].replace('-', ''))
			except ValueError:
				MyStr[idx]
			else:
				MyStr[idx] = float('-' + MyStr[idx].replace('-', ''))
		MyStr[idx] = Try_Float(MyStr[idx])			
	#MyStr = [Try_Float(x) for x in MyStr]		
	return MyStr

def ProcesTxt (str):	
	DataSet = []	
	CycleDate = ''
	OutputNameDate = ''
	OutputName = '' #use for accumulator num
	
	with open(str) as f:
		for line in f:
			if line.strip():
				#print 'in strip'
				# get cycle end date
				if CycDatePa.match(line.lstrip(' ')) and len(CycleDate) == 0:
					#get start date and end date to a list, set CycleDate to end date
					#CycleDate = re.search('20\d{2}\s+\D{3}\s+\d{1,2}', line).group()
					CycleDate = re.findall('20\d{2}\s+\D{3}\s+\d{1,2}', line)[1]
					print CycleDate
					tempd = datetime.strptime(CycleDate, '%Y %b %d')
					CycleDate = tempd.strftime('%m/%d/%Y')
					OutputNameDate = tempd.strftime('%Y%m%d')
					#break
				# get ACCUMULATOR TYPE 
				if TypePa.match(line[2:].lstrip(' ')) and len(OutputName) == 0:
					OutputName = re.search(r'\d+', line[2:]).group()			
					#break
				#get normal data lines	
				if DataPa.match(line[2:].lstrip(' ')):
					DataSet.append(ClList(line[2:]))
				#get totals from file
				if re.match(r'TOTAL ACCUMULATED AMOUNT', line[2:].lstrip(' ')):
					filetotal = ClList(line[2:])
					#print filetotal
						
	#print 'before assign'
	labels = ['CNSLT NUM', 'CACT TYPE', 'CURRENT DEALERSHIP', 'IGFS ACCUMULATED AMOUNT', 'IGSI ACCUMULATED AMOUNT', 'TOTAL ACCUMULATED AMOUNT']
	df = pd.DataFrame(DataSet, columns=labels)
	
	if OutputName == '33':
		df['Description'] = 'Mtge Referral'
		df['ACcode'] = 33
		
	if OutputName == '35':
		df['Description'] = 'Mtge Ins'
		df['ACcode'] = 35
		
	if OutputName == '794':
		df['Description'] = 'Bank AOF'
		df['ACcode'] = 794		
		
	df['CYCLE END DATE'] = CycleDate
	
	print 'now handle ' + OutputName
	#print df.dtypes
	if np.isclose(df['IGSI ACCUMULATED AMOUNT'].sum(), float(filetotal[2])):
		print 'IGFI ACCUMULATED AMOUNT matches' 
	if np.isclose(df['TOTAL ACCUMULATED AMOUNT'].sum(), filetotal[3]):
		print 'TOTAL ACCUMULATED AMOUNT matches' 	

	if OutputName in DebtList:
		#print 'in if'
		df.to_csv('A0000'+OutputName+'_'+OutputNameDate+'.csv', index=False)
	elif OutputName in AlList:
		
		df.to_csv(OutputName+'.csv', index=False)
		df2 = pd.read_csv(OutputName+'.csv')
		
		# Create a Pandas Excel writer using XlsxWriter as the engine.
		writer = pd.ExcelWriter(OutputName+'.xlsx', engine='xlsxwriter')
		
		# Convert the dataframe to an XlsxWriter Excel object.
		df2.to_excel(writer, sheet_name=OutputName, index=False)

		# Close the Pandas Excel writer and output the Excel file.
		writer.save()
		
		os.remove(OutputName+'.csv')
			
	else:	
		df.to_csv(OutputName+'.csv', index=False)
	return	
	
for file in os.listdir('\pycode'):
    if file.endswith('.txt'):
		FileList.append(os.path.join('\pycode', file))

#print FileList	
for txts in FileList:
	with open(txts) as f:
		for line in f:
			if line.strip():
				#print 'in strip'
				if TypePa.match(line[2:].lstrip(' ')):
					#print 'Process'
					ProcesTxt(txts)
					break
					