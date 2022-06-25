import streamlit as st
import preproessor,analyzerFunctions
import matplotlib.pyplot as plt
import seaborn as sns

#set title of the app
st.sidebar.title("WhatsApp Chat Analyzer:")

#set file uploader
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    data=preproessor.preprocessing(data)

    #dataShow=data[["user","message","year","month","day","day_name","hour","minute"]]
    #st.text("Messages and messages information:")
    #st.dataframe(dataShow)
    # Create a selectbox for the unique users and display
    user_list = data['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("select a user:", user_list)

    #create the button

    if st.sidebar.button("Show Analysis"):

        col1,col2,col3,col4= st.columns(4)
        col5,col6,col7,col8= st.columns(4)

        #statistical information extraction
        num_msg,num_word,num_media_msg,links,unsent,missed_call=analyzerFunctions.msg_count(selected_user,data)

        with col1:
            st.text("TotalMessages sent:")
            st.title(num_msg)

        with col2:
            st.text("TotalWords sent:")
            st.title(num_word)
        with col3:
            st.text("TotalMedia shared:")
            st.title(num_media_msg)
        with col4:
            st.text("TotalLinks shared:")
            st.title(links)
        with col5:
            st.text("TotalUnsent msg:")
            st.title(unsent)
        with col6:
            st.text("TotalMissed Call:")
            st.title(missed_call)

        # monthly timeline

        col1,col2=st.columns(2)

        st.title("Monthly Timeline:")
        timeline = analyzerFunctions.monthly_timeline(selected_user, data)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='red')
        plt.xticks(rotation='vertical', fontsize=7)
        plt.yticks(fontsize=7)
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline:")
        daily_timeline = analyzerFunctions.daily_timeline(selected_user, data)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical', fontsize=7)
        plt.yticks(fontsize=7)
        st.pyplot(fig)

        # activity map
        st.title('Activity Map:')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day:")
            busy_day = analyzerFunctions.week_activity_map(selected_user, data)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical', fontsize=15)
            plt.yticks(fontsize=15)
            st.pyplot(fig)

        with col2:
            st.header("Most busy month:")
            busy_month = analyzerFunctions.month_activity_map(selected_user, data)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical', fontsize=15)
            plt.yticks(fontsize=15)
            st.pyplot(fig)

        #finding the most busy user of the group
        if selected_user =='Overall':
            st.title('Most Busy Users')
            x, new_df = analyzerFunctions.most_busy_users(data)
            fig, ax = plt.subplots()

            col12, col21 = st.columns(2)

            with col12:
                st.text("Msg contribution of top users:")
                ax.bar(x.index, x.values, color="red")
                plt.xticks(rotation='vertical',fontsize=15)
                plt.yticks(fontsize=15)
                plt.xlabel("User names",fontsize=20)
                plt.ylabel("Number of msg sent",fontsize=20)
                st.pyplot(fig)
            with col21:
                st.text("Top msg sending percentages of each user:")
                st.dataframe(new_df)


        # WordCloud
        st.title("Wordcloud(Most frequent words used in chat):")
        st.text("Larger word_size means mostly used word in chat and smaller means least used word")
        df_wc = analyzerFunctions.create_wordcloud(selected_user, data)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = analyzerFunctions.most_common_words(selected_user, data)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1],color="gold")
        plt.xticks(rotation='vertical')
        plt.xlabel("Number of appearance")
        plt.ylabel("Words")
        st.title('Most frequent 20 words used in chat:')
        st.pyplot(fig)


        # emoji analysis
        emoji_df = analyzerFunctions.emoji_helper(selected_user, data)
        st.title("Emoji Analysis:")

        col1, col2 = st.columns(2)

        with col1:
            st.text("Number of emoji contain in the chat:")
            st.dataframe(emoji_df)
        with col2:
            st.text("5 Top % of emoji contain in chat:")
            fig, ax = plt.subplots()
            ax.pie(emoji_df["counts"].head(), labels=emoji_df["emoji"].head(), autopct="%0.2f")
            st.pyplot(fig)

        
