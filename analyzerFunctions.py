from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji


extract = URLExtract()


# statistical information extraction
def msg_count(selected_user,data):
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]

    # fetch the number of messages
    num_messages = data.shape[0]

    # fetch the total number of words
    words = []
    for message in data['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = data[data['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in data['message']:
        links.extend(extract.find_urls(message))

    #fetching the unsent msg
    num_unsent=data[data['message'] == 'This message was deleted\n'].shape[0]
    # fetching the missed voice call
    num_voice_call = data[data['message'] == 'Missed voice call\n'].shape[0]

    return num_messages,len(words),num_media_messages,len(links),num_unsent,num_voice_call

#finding the most busy user of the group
def most_busy_users(data):
    x = data['user'].value_counts().head()
    data = round((data['user'].value_counts() / data.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,data

#creating the words map(most used word)
def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'This message was deleted\n']
    temp = temp[temp['message'] != 'Missed voice call\n']

    wc = WordCloud(width=400, height=320, min_font_size=10, background_color='white')
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

#find the most common words
def most_common_words(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'This message was deleted\n']
    temp = temp[temp['message'] != 'Missed voice call\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

    #find the emoji and analysis
def emoji_helper(selected_user,data):
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]


    emojis = []
    for message in data['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis)))).rename(
        columns={0:'emoji',1:'counts'})

    return emoji_df

#monthly timeline
def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

#daily timeline
def daily_timeline(selected_user,data):

    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]

    daily_timeline = data.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

#weekly busy day
def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

#monthly busy day
def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()
