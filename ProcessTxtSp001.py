import os
import re, sys
import numpy as np
import pandas as pd
from datetime import datetime

#DataPa = re.compile(r'^\d{1,5}\s{2,}\d{1}\s{2,}IG\D{2}\s{1}\(\d{4}\).*$')
DataPa = re.compile(r'\d{1,5}\s{2,}\d{1,5}\s{2,}\d{1}\s{2,}.*$')
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
	#print MyStr
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
	#print MyStr
	#sys.exit("stop")
	return MyStr

def ProcesTxt (str):	
	DataSet = []	
	CycleDate = '12/31/2017'
	OutputNameDate = ''
	OutputName = '935' #use for accumulator num
	
	with open(str) as f:
		for line in f:
			if line.strip():
				if DataPa.match(line[2:].lstrip(' ')):
					DataSet.append(ClList(line[2:]))
				#get totals from file
				if re.match(r'TOTAL ACCUMULATED AMOUNT', line[2:].lstrip(' ')):
					filetotal = ClList(line[2:])
					#print filetotal
						
	#print 'before assign'
	labels = ['RO', 'Cslt', 'AccType', 'Name', 'Income', 'Tax']
	df = pd.DataFrame(DataSet, columns=labels)
	print df.head()
	#sys.exit("stop")
	
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

	if OutputName in DebtList:
		print 'in if'
		df.to_csv('A0000'+OutputName+'_'+OutputNameDate+'.csv', index=False)
	elif OutputName in AlList:
		print 'in AL'
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
		print 'in else'	
		df.to_csv(OutputName+'.csv', index=False)
	return	
	
for file in os.listdir('\pycode\Data'):
    if file.endswith('C935 - Releve 1 Tax Receipts Produced for Valeurs Mobilieres Groupe Investors Inc for 2017.txt'):
		FileList.append(os.path.join('\pycode\Data', file))

#print FileList	
for txts in FileList:
	with open(txts) as f:
		for line in f:
			if line.strip():
				ProcesTxt(txts)
				print 'out'
				break
					