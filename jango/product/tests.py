from django.test import TestCase
import pandas as pd
import os
from django.conf import settings

# Create your tests here.
filepath = os.path.join('datas\\' + 'test.xlsx')
df = pd.read_excel(filepath,  index_col=0)
print(df.index[:])

a = len(df)

name = {}
for i in range(a):
    temp = df.index[i]

    if str(type(df.index[i])) == "<class 'str'>" and  temp.find('#') > -1:
        aa = temp.strip('#')
        bb = aa.strip()
        sb = bb.split()
        
        name[sb[0]] = sb[2]
        print(sb[0])

    else:
        print(f'----{i}')

print(name)

print(df.index[0].find('#'))
print(type(df.index[0]))

print(type(df.index[:]))