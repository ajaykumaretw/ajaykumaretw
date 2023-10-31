import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
pd.set_option('display.max_rows',100)
pd.set_option('display.max_columns',30)
url = "https://www.naukri.com/financial-analyst-jobs-in-mumbai?k=financial%20analyst&l=mumbai"
page = requests.get(url)
print(page.text)
driver = webdriver.Chrome("E:/chromedriver-win32/chromedriver-win32/chromedriver.exe")
driver.get(url)
time.sleep(3)
soup = BeautifulSoup(driver.page_source,'html5lib')
print(soup.prettify())
driver.close()
#df = pd.DataFrame(columns=['Title','Company','Ratings','Reviews','URL'])
#print(df)
results = soup.find(class_='styles_jlc__main__VdwtF')
print(results)
case_list = []
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

        # Ratings
        rating_span = job_elem.find('span',class_='main-2')
        if rating_span is None:
            continue
        else:
            Ratings = rating_span.text

        # Reviews Counts
        Review_span = job_elem.find('a',class_='review ver-line')
        if Review_span is None:
            continue
        else:
            Reviews = Review_span.text

        # Years of experience Required
        Exp_span = job_elem.find('span',class_='main-2')
        
        if Exp_span is None:
            continue
        else:
            Experience = Exp_span.text

        # Salary offered for the job
        Sal = job_elem.find('span',class_='ni-job-tuple-icon-srp-rupee')
        Sal_span = Sal.find('span')
        if Sal_span is None:
            continue
        else:
            Salary = Sal_span.text

        # Location for the job post
        Loc = job_elem.find('span',class_='ni-job-tuple-icon-srp-location')
        Loc_exp = Loc.find('span')
        if Loc_exp is None:
            continue
        else:
            Location = Loc_exp.text

        # Number of days since job posted
        #Hist = job_elem.find("div",["type br2 fleft grey","type br2 fleft green"])
        Post_Hist = job_elem.find('span',class_='job-post-day')
        if Post_Hist is None:
            continue
        else:
            Post_History = Post_Hist.text
    #   Appending data to the DataFrame 
        case = {'JobId':JobId,'Title':Title,'Company':Company,'Ratings':Ratings,'Reviews':Reviews,'URL':URL,'Experience':Experience,'Salary':Salary,'Location':Location,'Job_Post_History':Post_History}
        case_list.append(case)
#df=pd.concat(case_list,ignore_index=0)
df=pd.DataFrame(case_list)
df.columns =['JobId','Title','Company','Ratings','Reviews','URL','Experience','Salary','Location','Job_Post_History']
print(df)
df.to_csv('D:/Naukri.csv')
