import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties
prop = FontProperties(fname='/System/Library/Fonts/Apple Color Emoji.ttc')
plt.rcParams['font.family'] = prop.get_family()


st.sidebar.title('WhatsApp Chat Analyzer')
uploaded_file = st.sidebar.file_uploader("Pilih File  : WhatsApp History Chat (.txt)")

if uploaded_file is not None:
    st.title("==================Welcome==================")
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')
    selected_user = st.sidebar.selectbox("Show analysis WhatsApp", user_list)
    st.title("=============================================")

    if st.sidebar.button("Show Analysis"):
        num_messages, num_words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        # st.title("History WhatApps Chat")
        # st.dataframe(df_user)
        # st.title("=============================================")

        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(num_words)

        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)

        with col4:
            st.header("Link Shared")
            st.title(num_links)

        st.title("=============================================")

        if selected_user == 'Overall':
            st.title("Most Busy User")
            x, new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # wordcloud analysis
        st.title("=============================================")
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title("=============================================")
        st.title("Most frequently words")
        most_common_df = helper.most_common_words(selected_user, df)
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(most_common_df)

        with col2:
            fig, ax = plt.subplots()
            # ax.bar(most_common_df['word'], most_common_df['frekuensi'], color='red')
            ax.barh(most_common_df['word'], most_common_df['frekuensi'], color='red')
            ax.invert_yaxis()
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # emoji analysis
        st.title("=============================================")
        st.title("Most frequently emoji")
        most_emoji_df = helper.emoji_func(selected_user, df)

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(most_emoji_df)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(most_emoji_df['frekuensi'], labels=most_emoji_df['emoji'], autopct="%0.2f")
            plt.rc('axes', unicode_minus=False)
            st.pyplot(fig)

        # montly timeline analysis
        st.title("=============================================")
        st.title("Monthly Timeline")
        montly_timeline_df = helper.monthly_timeline(selected_user, df)
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(montly_timeline_df)

        with col2:
            fig, ax = plt.subplots()
            ax.plot(montly_timeline_df['time'], montly_timeline_df['message'], color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # daily timeline analysis
        st.title("=============================================")
        st.title("Daily Timeline")
        daily_timeline_df = helper.daily_timeline(selected_user, df)
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(daily_timeline_df)

        with col2:
            fig, ax = plt.subplots()
            ax.plot(daily_timeline_df['only_date'], daily_timeline_df['message'], color='blue')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # activity map
        st.title("=============================================")
        st.title("Activity Map")
        activity_map_df = helper.week_activity_map(selected_user, df)
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='maroon')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # activity map
        st.title("=============================================")
        st.title("Weekly Activity - Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)

        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
