import requests
from bs4 import BeautifulSoup
import pandas as pd

speakers, durations,topics,views =[],[],[],[]
for i in range(100):
    url = 'https://www.ted.com/talks?page='+str(i)+'&sort=popular'

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    res = requests.get(url,headers=headers)
    bs=BeautifulSoup(res.text,'html.parser')
    talks = bs.find('div',class_='row-sm-4up').find_all(class_='col')

    for talk in talks:
        speaker = talk.find('h4', class_='h12')   # 爬取演讲者姓名
        if speaker != None:
            speaker = speaker.text.strip()
            speakers.append(speaker)
        duration = talk.find('a', class_='ga-link')    # 爬取演讲时长
        if duration != None:
            duration = duration.text.strip()
            durations.append(duration)
        topic = talk.find('h4',class_ = 'h9')    # 爬取演讲题目
        if topic != None:
            topic = topic.text.strip()
            topics.append(topic)
        view = talk.find('span',class_='meta__val')  # 爬取播放量
        if view != None:
            view = view.text.strip()[:-1]   # 单位million
            views.append(view)

# print(len(speakers),speakers)
# print(len(durations),durations)
# print(len(topics),topics)
# print(len(views),views)

list_labels = ['speakers', 'durations', 'topics', 'views']
list_cols = [speakers, durations, topics, views]
zipped = list(zip(list_labels, list_cols))
ted_talk_data = dict(zipped)
df = pd.DataFrame(ted_talk_data)

df.to_csv('ted_talks_data.csv', index = False)
