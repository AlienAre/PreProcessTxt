import os
import re
import sys
import numpy as np
import pandas as pd
from datetime import datetime

#df = pd.read_excel('\pycode')

prnls = []
with open(r'C:\pycode\10163_NL ASF.prn') as f:
	for line in f:
		if line.strip():
			if line[0] == 'D':
				myl = [int(line[1:6]), int(line[16:17]), float(line[6:15])/100]
				prnls.append(myl)
#print  prnls

uploaddf = pd.DataFrame(prnls, columns=['cslt', 'accounttype', 'amount'])

df = pd.read_excel(r'C:\pycode\602.xlsx')
df = df.merge(uploaddf, left_on=['CNSLT NUM', 'CACT TYPE'], right_on=['cslt', 'accounttype'], how='left')
print df.head()
# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter("C:\\pycode\\602.xlsx", engine='openpyxl')
# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='602', index=False)
# Close the Pandas Excel writer and output the Excel file.
writer.save()

#sys.exit("done")
