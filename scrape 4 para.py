import requests
from bs4 import BeautifulSoup  
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def scrape_page():

    data = []
    
    for i in range(3):   
        url = 'https://www.ted.com/talks?language=en&page='+str(i)+'&sort=newest'
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
        res = requests.get(url,headers=headers)
        bs=BeautifulSoup(res.text,'html.parser')
        talks = bs.find('div',class_='row-sm-4up').find_all(class_='col')

    for talk in talks:
        speakers, durations,topics = None, None, None
        
        speaker = talk.find('h4', class_='h12')   # 爬取演讲者姓名
        if speaker != None:
            speakers = speaker.get_text().strip()
 
            
        duration = talk.find('a', class_='ga-link')    # 爬取演讲时长
        if duration != None:
            durations = duration.get_text().strip()
            
        topic = talk.find('h4',class_ = 'h9')    # 爬取演讲题目
        if topic != None:
            topics = topic.get_text().strip()

        data.append((speakers,durations,topics))
        
    df = pd.DataFrame(data=data,columns=['speakers','durations','topics'])

    url_speaker_li = []
    url_topic_li = []
    url_ = []
    for i  in speakers:
        url_speaker = i.lower().replace(' ','_')+'_'
        url_speaker_li.append(url_speaker)

    for i in topics:
        url_topic = i.lower().replace(' ','_')
        url_topic_li.append(url_topic)

    for i in range(len(url_topic_li)):
        url_0 = 'https://www.ted.com/talks/' + url_speaker_li[i] + url_topic_li[i] + '?language=en'
        url_.append(url_0)    # 每个视频的sub网址

    views = []

    for i in url_:
        res_ = requests.get(i,headers=headers)
        if res_.status_code == 200:
            bs_ = BeautifulSoup(res_.text,'html.parser')
            view = bs_.find('script',class_='data-spec')
            if view != None:
                view = view.text.strip()
                views.append(view)
        else:
            views.append('')

    print(views)
    print(len(views))
              
    return df 

# def data_preprocessing(data):
    
    

def write_csv(data):

    df = data.to_csv('ted_talks.csv')
    
    return df
    
def get_chunk_csv(path, chunk_size=1001):
    
    data = pd.read_csv(path, chunksize=chunk_size, index_col=0)   
    chunk_data = pd.DataFrame(data.get_chunk(chunk_size))   
    df = chunk_data.to_csv('ted_talks_1000_chunks.csv')
  
    return df

if __name__ == "__main__":
    
#    data = data_preprocessing(scrape_page())
    data=scrape_page()
#    write_csv(data)
#    get_chunk_csv('ted_talks.csv')

    

