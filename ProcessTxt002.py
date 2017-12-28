import os
import re
import pandas as pd
from datetime import datetime

#DataPa = re.compile(r'^\d{1,5}\s{2,}\d{1}\s{2,}IG\D{2}\s{1}\(\d{4}\).*$')
DataPa = re.compile(r'^\d{1,5}\s{2,}\d{1}\s{2,}\D{4}.*$')
TypePa = re.compile(r'ACCUMULATOR TYPE.*\d+')
CycDatePa = re.compile(r'.*THRU\s+20\d{2}\s+\D{3}\s+\d{1,2}')
Negative = re.compile(r'-')

DebtList = ['1', '2', '7', '1193']
AlList = ['335', '602', '696', '1133', '1177', '1181', '1317', '1334', '1336', '1338', '1340']

FileList = [] 


def ClList (str):
	#strip left blanks and end '\n', '\r'
	MyStr = filter(None, re.split(r'\s{2,}', str.lstrip(' ').rstrip('\n').rstrip('\r')))

	for idx in range(len(MyStr)):
		#remove front and trailing blank for each element and remove ',' for numbers
		MyStr[idx] = MyStr[idx].lstrip(' ').rstrip(' ').replace(',', '')
		#update '-' to front
		if '-' in MyStr[idx]:
			MyStr[idx] = '-' + MyStr[idx].replace('-', '')
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
				if TypePa.match(line.lstrip(' ')) and len(OutputName) == 0:
					#print 'process type'
					OutputName = re.search(r'\d+', line).group()
					#break
				#get normal data lines	
				if DataPa.match(line.lstrip(' ')):
					DataSet.append(ClList(line))
	#print 'before assign'
	labels = ['CNSLT NUM', 'CACT TYPE', 'CURRENT DEALERSHIP', 'IGFS ACCUMULATED AMOUNT', 'IGSI ACCUMULATED AMOUNT', 'TOTAL ACCUMULATED AMOUNT']
	df = pd.DataFrame(DataSet, columns=labels)
	#print 'after assign'
	if not df.empty:
		df['IGFS ACCUMULATED AMOUNT'] = df['IGFS ACCUMULATED AMOUNT'].str.replace(',' , '')
		df['IGSI ACCUMULATED AMOUNT'] = df['IGSI ACCUMULATED AMOUNT'].str.replace(',' , '')
		df['TOTAL ACCUMULATED AMOUNT'] = df['TOTAL ACCUMULATED AMOUNT'].str.replace(',' , '')
		
		pd.to_numeric(df['CNSLT NUM'], downcast='integer')
		pd.to_numeric(df['CACT TYPE'], downcast='integer')
		pd.to_numeric(df['IGFS ACCUMULATED AMOUNT'], downcast='float')
		pd.to_numeric(df['IGSI ACCUMULATED AMOUNT'], downcast='float')
		pd.to_numeric(df['TOTAL ACCUMULATED AMOUNT'], downcast='float')
	
	df['CYCLE END DATE'] = CycleDate
		
	#if OutputName == '1' or OutputName == '2':
	print OutputName
	#print DebtList
	if OutputName in DebtList:
		print 'in if'
		df.to_csv('A0000'+OutputName+'_'+OutputNameDate+'.csv', index=False)
	elif OutputName in AlList:
		print 'this is 335'
		
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
				if TypePa.match(line.lstrip(' ')):
					#print 'Process'
					ProcesTxt(txts)
					break
					