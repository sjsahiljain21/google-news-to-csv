import pandas as pd
import feedparser
from newspaper import Article

def article_info(keywords):
    if len((keywords).split()) == 1:
        NewsFeed = feedparser.parse('https://news.google.com/rss/search?q={}%20when%3A1d&hl=en-US&gl=US&ceid=US:en'.format(keywords))
        entry = NewsFeed.entries
        test = pd.json_normalize(entry)

        urls = []
        # source_domain = []
        # publication = []
        # date_publish = []
        # category = []
        headline = []
        article = []
        # summary = []
        authors = []
        # keywords = []

        for i in test.link:
            try:
                news = Article(i)
                news.download()
                news.parse()
            except:
                continue
            urls.append(i)
        #     source_domain.append(news.source_domain)
        #     publication.append(news.publication)
        #     date_publish.append(news.publish_date)
        #     category.append(news.category)
            headline.append(news.title)
            article.append(news.text)
        #     summary.append(news.summary)
            authors.append(news.authors)
        #     keywords.append(news.keywords)

        news_df_1 = pd.DataFrame({'link':urls, 'headline': headline, 'body': article, 'authors': authors})

        news_df_merged_1 = pd.merge(news_df_1, test[['link', 'source.href', 'source.title', 'published']], how = 'left', on = 'link')

        news_df_merged_1.columns = ['urls', 'headline', 'body', 'authors', 'domains', 'publications', 'publishedAt']

        return news_df_merged_1    

    else:

        keywords_updated = keywords.split()
        keywords_updated = "%20".join(keywords_updated) 
        NewsFeed = feedparser.parse('https://news.google.com/rss/search?q={}%20when%3A1d&hl=en-US&gl=US&ceid=US:en'.format(keywords_updated))
        entry = NewsFeed.entries
        test = pd.json_normalize(entry)

        urls = []
        # source_domain = []
        # publication = []
        # date_publish = []
        # category = []
        headline = []
        article = []
        # summary = []
        authors = []
        # keywords = []

        for i in test.link:
            try:
                news = Article(i)
                news.download()
                news.parse()
            except:
                continue
            urls.append(i)
        #     source_domain.append(news.source_domain)
        #     publication.append(news.publication)
        #     date_publish.append(news.publish_date)
        #     category.append(news.category)
            headline.append(news.title)
            article.append(news.text)
        #     summary.append(news.summary)
            authors.append(news.authors)
        #     keywords.append(news.keywords)

        news_df_1 = pd.DataFrame({'link':urls, 'headline': headline, 'body': article, 'authors': authors})

        news_df_merged_1 = pd.merge(news_df_1, test[['link', 'source.href', 'source.title', 'published']], how = 'left', on = 'link')

        news_df_merged_1.columns = ['urls', 'headline', 'body', 'authors', 'domains', 'publications', 'publishedAt']

        return news_df_merged_1