import requests
import pandas as pd
from newsapi import NewsApiClient
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords

api_key = "your key"
n = NewsApiClient(api_key)

query_list = ["Cricket", "Football", "Corona"]


def download(q):
    data = n.get_everything(q=q, sources='bbc-news',
                            language='en', page_size=50)
    articles = data['articles']
    df = pd.DataFrame(articles)

    article_link = df[['title', 'url']]

    article_content = []
    for article in list(article_link['url']):
        try:
            res = requests.get(article)
            soup = BeautifulSoup(res.content, "html.parser")
            body = soup.find("div", attrs={'id': "story-body"})
            c = body.find_all("p")[1:]
            c = [str(a) for a in c]
            c = " ".join(c)
            article_content.append(c)
        except:

            article_content.append("Video Content")
    article_cont_df = pd.DataFrame(article_content)
    article_link['Content'] = article_cont_df
    article_link['Content'] = article_link['Content'].apply(preprocessing)
    print(f"Saving .... Data{str(q)}.csv")
    article_link.to_csv(f"Data{str(q)}.csv")


def preprocessing(body):

    clean = re.compile('<.*?>')
    s = re.sub(clean, '', body)
    s = re.sub(r"\W", " ", s).lower()
    words = nltk.word_tokenize(s)
    stop = set(stopwords.words('english'))
    s = [x for x in words if x not in stop]
    s = " ".join(s)
    return s


for q in query_list:
    download(q)
