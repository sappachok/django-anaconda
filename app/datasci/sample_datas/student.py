import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline
df = pd.read_csv('datasci/datasets/student.txt',sep=',',low_memory=False)
df.head()

#df.shape
#df.isnull().sum()

a = ['2555','2556','2557']
df = df[~df['YEAR'].isin(a)]
df['YEAR'].value_counts()

import seaborn as sns
sns.set_style('whitegrid')
#print(df)
x = df
#plt.figure(figsize=(16, 6))
sns.countplot(x='YEAR', data=x)

#ax = sns.lineplot(x="YEAR", y="GPA", data=df)

b = df[['YEAR','GPA']]
b.groupby(['YEAR']).mean()

x.groupby('YEAR')

sc = df[['SCHOOL_NAME']]
sc.dropna()
# sc.head()

df['SCHOOL_NAME'].value_counts().head(10)

df_grouped = df.groupby('SCHOOL_NAME')['STUDENT_CODE'].count()

SchoolTopCount = df_grouped.loc[df_grouped >= 200]
SchoolTopIndex = list(SchoolTopCount.index)

topsch = df[df['SCHOOL_NAME'].isin(SchoolTopIndex)]
# topsch.head()

schoolId = []
i=1
for scid in SchoolTopIndex:
    schoolId.append(scid)
    i += 1


# schoolId

ye = [2560,2561,2562]
data = {'year':ye}
df_data = []
df_data = pd.DataFrame(data)
tmp = []
for sc in SchoolTopIndex:
    tmp = df[df['SCHOOL_NAME']==sc]
    tmp_year = []
    for y in ye:
        tmp_year.append(len(tmp[tmp['YEAR']==y]))
        #print("%d %s %d",(y,sc,len(tmp[tmp['YEAR']==y])))
    df_data['col_'+str(SchoolTopIndex.index(sc))] = tmp_year

# df_data

df_data = df_data.melt('year', var_name='cols',  value_name='vals')
# df_data.head()

plt.figure(figsize=(16, 6))
g = sns.lineplot(x="year", y="vals", hue='cols', data=df_data)

for ind, value in enumerate(SchoolTopIndex):
    print(ind, value)
    
#data_pot = df[df]
#plt.figure(figsize=(16, 6))
#sns.countplot(x='SCHOOL_NAME', data=df)