import os
import re
import pandas as pd

#DataPa = re.compile(r'^\d{1,5}\s{2,}\d{1}\s{2,}IG\D{2}\s{1}\(\d{4}\).*$')
DataPa = re.compile(r'^\d{1,5}\s{2,}\d{1}\s{2,}\D{4}.*$')
TypePa = re.compile(r'ACCUMULATOR TYPE.*\d+')
Negative = re.compile(r'-')

#OutputName = '' #use for accumulator num
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
	# get ACCUMULATOR TYPE 
	with open(str) as f:
		for line in f:
			if line.strip():
				#print 'in strip'
				if TypePa.match(line.lstrip(' ')):
					OutputName = re.search(r'\d+', line).group()
					break
	
	with open(str) as f:
		for line in f:
			if line.strip():
				#print 'in strip'
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
					