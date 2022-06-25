import re
import pandas as pd
import numpy as np

#preprocessing the data
def preprocessing(data):
    #split the date,time content and the chating content
    #extract chat
    pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s\w+\s-\s"
    messages = re.split(pattern, data)[1:]

    #extract the date and time
    dates = re.findall(pattern, data)

    #create the dataframe using the message and date columns
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M %p - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    #split the user and message
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    #extract the year,month,date,day,hour,minute,dayName
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df










