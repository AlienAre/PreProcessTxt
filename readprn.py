import os
import re
import sys
import numpy as np
import pandas as pd
from datetime import datetime

#df = pd.read_excel('\pycode')

uploaddf = []
with open(r'C:\pycode\10163_NL ASF.prn') as f:
	for line in f:
		if line.strip():
			myl = [line[1:6], float(line[6:15])/100, line[16:17]]
			uploaddf.append(myl)
print  uploaddf
#sys.exit("done")
