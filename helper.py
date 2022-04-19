import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from collections import Counter

extractor = URLExtract()

stopwords_from_sastawi = StopWordRemoverFactory().get_stop_words()
more_stopword = ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.',
                 'yg', 'mas', 'bang', '-']
stopword = stopwords_from_sastawi + more_stopword


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
    num_words = len(words)

    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    num_links = len(links)

    return num_messages, num_words, num_media_messages, num_links


def most_busy_user(df):
    x = df['user'].value_counts().head(10)
    df = round((df['user'].value_counts()/df.shape[0])*100).reset_index().rename(columns={'index':'name', 'user':'percent'})
    return x, df


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != "group_notification"]
    temp = temp[temp['message'] != "<Media omitted>\n"]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc


def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != "group_notification"]
    temp = temp[temp['message'] != "<Media omitted>\n"]

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stopword:
                words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20), columns={'word', 'frekuensi'})

    return most_common_df
