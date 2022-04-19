import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import plotly.graph_objects as go


st.sidebar.title('WhatsApp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    st.title("Data from WhatsApp Group Chat")
    st.title("=============================================")

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
        fig, ax = plt.subplots()
        ax.barh(most_common_df['word'], most_common_df['frekuensi'], color='red')
        ax.invert_yaxis()
        plt.xticks(rotation='vertical')


        # fig = go.Figure(go.Bar(
        #     y=most_common_df['word'],
        #     x=most_common_df['frekuensi'],
        #     orientation='h'))

        st.pyplot(fig)
        st.title("=============================================")







