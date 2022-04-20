import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary
from collections import Counter
import emoji
import re


extractor = URLExtract()

stopwords_from_sastawi = StopWordRemoverFactory().get_stop_words()
more_stopword = ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.',
                 'yg', 'mas', 'bang', '-', 'terima', 'kasih', 'aja', 'ga', 'rekan', 'https', 'terimakasih', 'bang',
                 'nggak', 'gak', 'bapak', 'ibu', 'selamat', 'us', 'go', 'id',
                 'was', 'deleted', 'yuk', 'kalo', 'message', 'makasih', 'this', 'udah', 'klo', 'iya', 'biar', 'gaes',
                 'makace', 'besok', 'semoga', 'nih', 'udh', 'pake', 'mba', 'eh', 'om', ]
stopword = stopwords_from_sastawi + more_stopword
stopworder = StopWordRemover(ArrayDictionary(stopword))

def stopwords_clean(singledata_seriez):
    singledata_seriez = str(singledata_seriez)
    singledata_seriez = stopworder.remove(singledata_seriez)
    return singledata_seriez

# def remove_stopwords(message):
#     y = []
#     for word in message.lower().split():
#         if word not in stopword:
#             y.append(word)
#     return " ".join(y)


def clean_dataframe(dataframe):
    dataframe = re.sub(r'\b\d+\b', ' ', dataframe)
    dataframe = re.sub('[.@,*_/(/)//=:]', ' ', dataframe)
    # dataframe = re.sub('[@,*]', ' ', dataframe)
    # dataframe = re.sub('<[^<]+?>', '', dataframe)
    # dataframe = re.sub('-\s+', '', dataframe)
    # dataframe = re.sub('[\(\)-]', '', dataframe)
    # dataframe = re.sub('[.]', ' ', dataframe)
    return dataframe

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
    df = df[df['user'] != 'group_notification']
    x = df['user'].value_counts().head(10)
    df = round((df['user'].value_counts()/df.shape[0])*100).reset_index().rename(columns={'index':'name', 'user':'percent'})
    return x, df


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != "group_notification"]
    temp = temp[temp['message'] != "<Media omitted>\n"]
    temp['message'] = temp['message'].str.lower().apply(clean_dataframe).apply(stopwords_clean)
    # temp['message'] = temp['message'].apply(remove_stopwords)
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white', stopwords=stopword)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc


def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != "group_notification"]
    temp = temp[temp['message'] != "<Media omitted>\n"]
    temp['message'] = temp['message'].str.lower()
    temp['message'] = temp['message'].apply(clean_dataframe)

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    words = []
    for message in temp['message']:
        for word in message.split():
            if (word not in stopword) and (word not in emojis):
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    most_common_df.rename(columns={0: 'word', 1: 'frekuensi'}, inplace=True)

    return most_common_df


def emoji_func(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    most_emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    most_emoji_df  = most_emoji_df.rename(columns={0: 'emoji', 1: 'frekuensi'})

    return most_emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['month_num'] = df['date'].dt.month
    montly_timeline_df = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(montly_timeline_df.shape[0]):
        time.append(montly_timeline_df['month'][i] + "-" + str(montly_timeline_df['year'][1]))

    montly_timeline_df['time'] = time

    return montly_timeline_df


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['only_date'] = df['date'].dt.date
    daily_timeline_df = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline_df


def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap =  df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap
