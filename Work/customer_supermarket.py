import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
from pandas_profiling import ProfileReport
import datetime as dt
import matplotlib.pyplot as plt
import dtale
import warnings
warnings.filterwarnings("ignore")
#supermarket=pd.read_csv('E:/Work/customer_supermarket.csv',on_bad_lines='skip',sep='\t')
supermarket=pd.read_csv('E:/Work/customer_supermarket.csv',on_bad_lines='skip',sep='\t',index_col=0)
#data= supermarket[pd.notnull(supermarket['CustomerID'])]
#dtale.show(data)
#dtale.show(data).open_browser()
#print(data)
print(supermarket['CustomerID'].value_counts())
#supermarket['CustomerCountry'].value_counts()[:10].plot(kind='bar')
print(supermarket.shape)
print(supermarket.dtypes)
#Check Weather Any column having null or not
print(supermarket.isnull().any())
codes=supermarket[supermarket["BasketID"].str.contains('^[a-zA-Z]+',regex=True)]["BasketID"].unique()
print(pd.Series(codes).apply(lambda x:x[0]).unique())

print('Conains C in BasketID: {0}'.format(supermarket[supermarket["BasketID"].str.contains('C')].shape[0]))
print('Conains A in BasketID: {0}'.format(supermarket[supermarket["BasketID"].str.contains('A')].shape[0]))
#Select Top 10 Values
print(supermarket.head(10))
#Description of Data frame
print(supermarket.describe())
#Column Names
print(supermarket.columns)
specialCodes=supermarket[supermarket["ProdID"].str.contains('^[a-zA-Z]+',regex=True)]["ProdID"].unique()
for code in specialCodes:
  print('{0} having Description: {1}'.format(code,supermarket[supermarket["ProdID"]==code]["ProdDescr"].unique()[0]))
#Get Null Coumnt
print(supermarket.isnull().sum())
print(supermarket['BasketDate'].nunique())
data= supermarket[pd.notnull(supermarket['CustomerID'])]
#supermarket['Sale'] = supermarket['Sale'].str.split(',')                                                               
#supermarket.explode('Sale')
print(data)
print(supermarket["CustomerID"].unique().sum())
Total_beforeDrop=supermarket.shape[0]
supermarket.drop_duplicates(ignore_index=True,inplace=True)
Total_AfterDrop=supermarket.shape[0]
remainTotal=Total_beforeDrop-Total_AfterDrop
CancelledRecords=remainTotal/Total_beforeDrop*100
print('Cancelled Records: {0} %'.format(CancelledRecords))
nullCustomer=supermarket["CustomerID"].isnull().sum()
totalSample=supermarket.shape

#remove null values
supermarket = supermarket.dropna()
#supermarket=data[['CustomerCountry','CustomerID']].drop_duplicates()
#Check Null values after remove.
print(supermarket.isnull().sum())
#Convert Customerid column as Int
supermarket["CustomerID"]=supermarket["CustomerID"].astype('int')
supermarket['BasketDate'] = pd.to_datetime(supermarket['BasketDate'])
supermarket['Sale'] = supermarket['Sale'].str.replace(',','.')
supermarket['Sale'] =pd.to_numeric(supermarket['Sale'])
supermarket['Max_Year_Date'] = supermarket['BasketDate'].max() 
supermarket['Year'] = supermarket['BasketDate'].dt.year
print(supermarket.info())
print(supermarket.describe())
supermarket =supermarket[(supermarket['Qta']>0)]
print(supermarket.describe())
print(supermarket.dtypes)
print(supermarket)
print(supermarket.tail(10))
NOW = pd.to_datetime('now')
supermarket.reset_index(inplace=True)
supermarket['Date_Interval'] = supermarket['Max_Year_Date'] - supermarket['BasketDate']
print(supermarket)
# We use group and aggregation to calculate R,F and M
rfm_gb = supermarket.groupby(['Year', 'CustomerID'], as_index = False).agg({'Date_Interval': 'min', 'Date_Interval': 'count', 'Sale': 'mean'})
#rfm_gb.columns = ['Year', 'CustomerID', 'r', 'f', 'm']
print(rfm_gb)
recancy=supermarket.groupby('CustomerID').agg({'BasketDate': lambda x: (NOW - x.max()).days})
print(recancy)
frequency=supermarket.drop_duplicates(subset='BasketID').groupby(['CustomerID'])[["BasketID"]].count()
print(frequency)
supermarket['Total']=supermarket['Sale']* supermarket['Qta']
money=supermarket.groupby('CustomerID')[["Total"]].sum()
print(money)
print(supermarket)
RFM=pd.concat([recancy,frequency,money],axis=1)
recancy.columns=["Recancy"]
frequency.columns=["Frequency"]
money.columns=['Monetary']
print(RFM)

from sklearn.preprocessing import StandardScaler
Scaler=StandardScaler()
scaled=Scaler.fit_transform(RFM)

from sklearn.cluster import KMeans
inertia=[]
for i in np.arange(1,11):
  kmeans=KMeans(n_clusters=int(i))
  kmeans.fit(scaled)
  inertia.append(kmeans.inertia_)
expensive_Purchases = supermarket.groupby("CustomerCountry")[["Sale"]].max().sort_values("Sale", ascending=False)
print(expensive_Purchases)
pd.set_option('display.max_rows', None)
#print(pd.Series({c: supermarket[c].unique() for c in supermarket}))

#Average Customer Sale
print(supermarket.groupby('CustomerCountry')['Sale'].mean())

sns.heatmap(supermarket.isnull(),cbar=False)

fig,(ax1,ax2)=plt.subplots(1,2)
supermarket.boxplot(column=['Sale'],ax=ax1)
supermarket.boxplot(column=['Qta'],ax=ax2)
fig.subplots_adjust(wspace=0.5)
plt.savefig('/boxplots_before.png')

print(pd.DataFrame({'Transection':supermarket.BasketDate.nunique(),
              'Customers':supermarket.CustomerID.nunique(),
              'Product':supermarket.ProdID.nunique(),
              },index=['QTY']))

print(supermarket.groupby(['CustomerID'])['Qta'].max())

