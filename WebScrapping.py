import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
pd.set_option('display.max_rows',100)
pd.set_option('display.max_columns',30)
case_list = []
for param in range(1,5):
 url = "https://www.naukri.com/financial-analyst-jobs-in-mumbai-" + str(param)
 page = requests.get(url)
 #print(page.text)
 driver = webdriver.Chrome("D:/chromedriver-win64/chromedriver-win64/chromedriver.exe")
 driver.get(url)
 time.sleep(3)
 soup = BeautifulSoup(driver.page_source,'html5lib')
 #print(soup.prettify())
 driver.close()
 #df = pd.DataFrame(columns=['Title','Company','Ratings','Reviews','URL'])
 #print(df)
 results = soup.find(class_='styles_jlc__main__VdwtF')
 #print(results)
 if results is not None:
  job_elems = results.find_all(class_='srp-jobtuple-wrapper')

  for job_elem in job_elems:
         
         #Job Id
         
         JobId= job_elem.get('data-job-id')

         # URL to apply for the job     
         URL = job_elem.find('a',class_='title').get('href')
     #     print(URL.strip())
 
         # Post Title
         Title = job_elem.find('a',class_='title').get('title')
 
         # Company Name
         Company = job_elem.find('a',class_='comp-name').get('title')

         # Job Description
         Job_Description = job_elem.find('span',class_='job-desc').text
 
         # Ratings
         Rating_span = job_elem.find('span',Title='main-2')
         
         if Rating_span is None:
             Ratings=''
         else:
             Ratings = Rating_span.text
 
         # Reviews Counts
         Review_span = job_elem.find('a',class_='review ver-line')
         
         if Review_span is None:
             Reviews=''
         else:
             Reviews = Review_span.text
         
         #Job Walkin
         Job_Walkin_Span = job_elem.find('span',class_='walkDateWdth')

         if Job_Walkin_Span is None:
             Job_Walkin=''
         else:
             Job_Walkin= Job_Walkin_Span.text

         # Years of experience Required
         Exp_span = job_elem.find('span',class_='expwdth')
         if Exp_span is None:
             Experience=''
         else:
             Experience = Exp_span.text
 
         # Salary offered for the job
         Sal = job_elem.find('span',class_='ni-job-tuple-icon-srp-rupee')
         Sal_span = Sal.find('span')
         if Sal_span is None:
             Salary=''
         else:
             Salary = Sal_span.text
 
         # Location for the job post
         Loc = job_elem.find('span',class_='ni-job-tuple-icon-srp-location')
         Loc_exp = Loc.find('span')
         if Loc_exp is None:
             Location=''
         else:
             Location = Loc_exp.text
 
         # Number of days since job posted
         #Hist = job_elem.find("div",["type br2 fleft grey","type br2 fleft green"])
         Post_Hist = job_elem.find('span',class_='job-post-day')
         if Post_Hist is None:
             Post_History=''
         else:
             Post_History = Post_Hist.text
         
     #   Appending data to the DataFrame 
         case = {'JobId':JobId,'Title':Title,'Company':Company,'Ratings':Ratings,'Reviews':Reviews,'URL':URL,'Experience':Experience,'Salary':Salary,'Location':Location,'Job_Post_History':Post_History,'Job_Walkin':Job_Walkin,'Job_Description':Job_Description}
         case_list.append(case)
#df=pd.concat(case_list,ignore_index=0)
df=pd.DataFrame(case_list)
df.columns =['JobId','Title','Company','Ratings','Reviews','URL','Experience','Salary','Location','Job_Post_History','Job_Walkin','Job_Description']
print(df)
print(df.Job_Description)
print(df.groupby(by="Title")['Location'].sum())
#let us check the dataframe structure and its column type
print(df.info())
#Take-away: there are 10 columns and all these are object type
#let us find number of rows and column in given dataset
print(df.shape)
#Take-away: as per the shape, dataset has 1205 rows and 10 columns

#Exploratory Data Analysis
#we will perform exploratory data analysis on given dataset to understand below points

 #Find Unwanted Columns or Features which has only one value or unique values and which will not play important role in analysis
 #Handle the missing values if there is any
 #Explore, what are categorical features we have in given dataset
 #Understand the features distribution
 #Find the Top 15 Industries and Functional Areas for which maximum number of oportunies are available
 #Find the Top 15 Locations where job opportunities are very high
 #Find the Top 15 Role and Role category to which maximum number of recruiters are looking
 #Find the Top 15 Job exp required in Years for which maximum number of oportunies are available
 #Find the Top Job experiences levels for which maximum number of oportunies are available
 #Find the Salary Ranges for which maximum number of oportunies are available
 #Find the Top 20 Key Skills for which maximum number of oportunies are available

#1. Find Unwanted Columns
  #Take-away: JobId and URL columns seem to be not usefull.
#2. Find Missing Values
features_na = [features for features in df.columns if df[features].isnull().sum() > 0]
for feature in features_na:
    print(feature, np.round(df[feature].isnull().mean(), 4),  ' % missing values and actual count is '+str(df[feature].isnull().sum()))
# check what will be new shape after droping missing values

df.dropna(inplace=False).shape

#3. Find Features with One Value

for column in df.columns:
    print(column,df[column].nunique())

#4. Explore the Categorical Features

categorical_features=[feature for feature in df.columns if ((df[feature].dtypes=='O') & (feature not in ['JobId','URL']))]
print(categorical_features)

for feature in categorical_features:
    print('The feature is {} and number of categories are {}'.format(feature,len(df[feature].unique())))

print(df.groupby('Company',sort=True)['Company'].count()[0:15])


print(df.groupby('Title',sort=True)['Title'].count()[0:15])
from re import search

def get_comman_job_industry(x):
    x = x.replace(",", " /")
    if (search('it-software', x.lower())):
        return 'Software Services'
    elif (search('call ', x.lower())):
        return 'Call Centre'
    elif (search('banking', x.lower()) or search('insurance', x.lower()) or search('finance', x.lower())):
        return 'Financial Services'
    elif (search('recruitment', x.lower())): 
        return 'Recruitment'
    elif (search('pharma', x.lower())): 
        return 'Pharma'
    elif (search('isp', x.lower())): 
        return 'Telcom / ISP'
    elif (search('ecommerce', x.lower())): 
        return 'Ecommerce'
    elif (search('fmcg', x.lower())): 
        return 'FMCG'
    elif (search('ngo', x.lower())): 
        return 'NGO'
    elif (search('medical', x.lower())): 
        return 'Medical'
    elif (search('aviation', x.lower())): 
        return 'Aviation'
    elif (search('fresher ', x.lower())): 
        return 'Fresher'
    elif (search('education', x.lower())): 
        return 'Education'
    elif (search('construction', x.lower())): 
        return 'Construction'
    elif (search('consulting', x.lower())): 
        return 'Consulting'
    elif (search('automobile', x.lower())): 
        return 'Automobile'
    elif (search('travel', x.lower())): 
        return 'Travels'
    elif (search('advertising', x.lower()) or search('broadcasting', x.lower())): 
        return 'Advertising'
    elif (search('transportation', x.lower())): 
        return 'Transportation'
    elif (search('agriculture', x.lower())): 
        return 'Agriculture'
    elif (search('agriculture', x.lower())): 
        return 'Agriculture'
    elif (search('industrial', x.lower())): 
        return 'Industrial Products'
    elif (search('media', x.lower())): 
        return 'Entertainment'
    elif (search('teksystems', x.lower()) or search('allegis', x.lower()) or search('aston', x.lower())
         or search('solugenix', x.lower()) or search('laurus', x.lower()) ):
        return 'Other'
    else:
        return x.strip()
    
#df['New_Industry']=df['Industry'].apply(get_comman_job_industry)
#print(df.groupby('New_Industry',sort=True)['New_Industry'].count().sort_values(ascending=False)[0:15])

plt.figure(figsize=(18,6), facecolor='white')
df.groupby('Company',sort=True)['Company'].count().sort_values(ascending=False)[0:15].plot.bar(color='green')
plt.xlabel('Company')
plt.ylabel('Count')
plt.title('Distribution of Top 15 Company')
plt.show()

print(df.groupby('Location',sort=True)['Location'].count())
plt.figure(figsize=(18,6), facecolor='white')
df.groupby('Location',sort=True)['Location'].count().sort_values(ascending=False)[0:15].plot.bar(color='red')
plt.xlabel('Location')
plt.ylabel('Count')
plt.title('Distribution of Top 15 Location')
plt.show()

#Location column has multiple locatios separated by comm (,). let us separate all these location into individual rows, so that it will easy to analyse its count based on job opportunities
def get_location(df):
    df_new=pd.DataFrame()
    for index, row in df.iterrows():
        for loc in row['Location'].split(','):
            loc_df = pd.DataFrame([loc])
            df_new = pd.concat([df_new,loc_df],ignore_index=True)
    return df_new  
Location_df = get_location(df)
Location_df.columns = ['Location']

print(Location_df.groupby('Location',sort=True)['Location'].count().sort_values(ascending=False)[0:30])
plt.figure(figsize=(18,6), facecolor='white')
Location_df.groupby('Location',sort=True)['Location'].count().sort_values(ascending=False)[0:15].plot.bar(color="red")
plt.xlabel('Location')
plt.ylabel('Count')
plt.title('Distribution of Top 15 Locations')
plt.show()

print(df.groupby('Experience',sort=True)['Experience'].count()[0:30])
import re
def get_exp_level(x):
    if re.findall('-',x):
        lst =x.replace('Yrs','').strip().split('-')
        #print (x)
        lvl =(int(lst[0].strip())+int(lst[1].strip()))/2
        if (lvl >= 0 and lvl <= 2):
            return ('Freshers')
        elif (lvl >= 2 and lvl <= 5):
            return ('Intermediate')
        elif (lvl >= 5 and lvl <= 8):
            return ('Lead')
        elif (lvl >= 8 and lvl <= 12):
            return ('Manager')
        elif (lvl >= 12 and lvl <= 16):
            return ('Senior Manager')
        elif (lvl >= 16 and lvl <= 20):
            return ('Executive')
        elif (lvl >= 20):
            return ('Senior Executive')
        else:
            return('Others')
    else:
        return('Others')

df['New_Exp_Level']=df['Experience'].apply(get_exp_level)
print(df['New_Exp_Level'])
print(df.groupby('New_Exp_Level',sort=True)['New_Exp_Level'].count().sort_values(ascending=False)[0:30])

plt.figure(figsize=(18,6), facecolor='white')
df.groupby('New_Exp_Level',sort=True)['New_Exp_Level'].count().sort_values(ascending=False)[0:15].plot.bar(color="purple")
plt.xlabel('Job Exp Required in Years')
plt.ylabel('Count')
plt.title('Distribution of Top 15 Job Experience Year Range Required')
plt.show()
#df.to_csv('D:/Naukri.csv')
#Take-away: As we can see, most job posting required intermediate level experience professionals that is about 2-5 years exp holders followed by Lead Exp (5-8 Years) and then Freshers (0-2 Years).

# Salary
print(df.groupby('Salary',sort=True)['Salary'].count()[0:30])

#It is very uncleaned data, let us try to clean this and add generic salary label as per exp level and analyse
#0-2 : Freshers : 0-3L
#2-5 : Intermediate : 3-8L
#5-8 : Lead : 8 -15L
#8-12 : Manager : 15 - 22L
#12-16 : Senior Manager : 22 - 30L
#16-20 : Executive : 30 - 38L
#20-above : Senior Executive : 38L - above

import re
def get_salary(x):
    if re.findall('-',x):
        lst =x.replace('PA.','').replace(',','').replace('INR','').strip().split('-')        
        try:
            sal1 = int(lst[0].strip())
            sal2 = int(lst[1].strip())
            #print (sal1)
            if (sal1 <= 300000):
                return '0-3L PA'
            elif (sal1 >= 300000 & sal2 <= 800000 ):
                return '3-8L PA'
            elif (sal1 >= 800000 & sal2 <= 1500000 ):
                return '8 -15L PA'
            elif (sal1 >= 1500000 & sal2 <= 2200000 ):
                return '15 - 22L PA'
            elif (sal1 >= 2200000 & sal2 <= 3000000 ):
                return '22 - 30L PA'
            elif (sal1 >= 3000000 & sal2 <= 3800000 ):
                return '30 - 38L PA'
            if (sal1 >= 3800000):
                return '38L - Above PA'
        except:
            return('Others')
    else:
        return('Others')
    
df['New_Job_Salary']=df['Salary'].apply(get_salary)
print(df.groupby('New_Job_Salary',sort=True)['New_Job_Salary'].count().sort_values(ascending=False)[0:30])
#Take-away: it seems for most of the job openings, no job salary is mentioned.

