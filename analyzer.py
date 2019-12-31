import os
import json
import collections
from datetime import datetime
import configparser

config = configparser.RawConfigParser()
config.read('settings.ini')

messages_dir = config.get('settings', 'messages_directory')
user = config.get('settings', 'user')

everyone_words = collections.Counter()
user_words = collections.Counter()
everyone_reacts = collections.Counter()
user_reacts = collections.Counter()
ear_mes_r = ''
ear_mes_s = ''
ear_time_r = float('inf')
ear_time_s = float('inf')
ear_sender = ''
ear_reciever = ''
message_times = collections.Counter()

reactions = {'\u00f0\u009f\u0098\u008d': 'heart_eyes',
             '\u00e2\u009d\u00a4' : 'heart',
             '\u00f0\u009f\u0098\u0086' : 'laughing',
             '\u00f0\u009f\u0098\u00ae' : 'surprise',
             '\u00f0\u009f\u0098\u00a2' : 'sad',
             '\u00f0\u009f\u0098\u00a0' : 'angry',
             '\u00f0\u009f\u0091\u008d' : 'thumb_up',
             '\u00f0\u009f\u0091\u008e' : 'thumb_down' 
            }



def json_reader():
    '''
    Goes through every message in directory and calls a different analyze function on each one. Returns None.
    '''
    for filename in os.listdir(messages_dir):
        if os.path.isdir(os.path.join(messages_dir, filename)):
            for file_in_chat in os.listdir(os.path.join(messages_dir, filename)):
                if file_in_chat.lower().endswith('.json'):
                    with open(os.path.join(messages_dir, os.path.join(filename, file_in_chat))) as f:
                        data = json.load(f)
                        for message in data['messages']:
                            if 'content' in message.keys():
                                count_words(message)
                                find_first_message(message, data['participants'])
                            if 'reactions' in message.keys():
                                count_reactions(message)
                            find_time(message)
    
'''
Analyze Functions
'''
def count_words(message):
    '''
    Counts how often each word is used by the user and all chats by updating the counter most_used_words. Returns None.
    '''
    content = message['content']
    everyone_words[content] += 1
    if message['sender_name'] == user:
        user_words[content] += 1

def count_reactions(message):
    '''
    Counts how many of each reaction user uses and how many across all chats. Returns None
    '''
    for reaction in message['reactions']:
        react = reaction['reaction']
        actor = reaction['actor']
        everyone_reacts[reactions[react]] += 1
        if actor == user:
            user_reacts[reactions[react]] += 1

def find_first_message(message, members):
    '''
    Gets the first message ever send and recieved. Returns None.
    '''
    global ear_mes_r, ear_mes_s, ear_time_s, ear_time_r, ear_sender, ear_reciever
    timestamp = message['timestamp_ms']
    sender = message['sender_name']
    content = message['content']
    if timestamp < ear_time_s and sender == user:
        ear_mes_s, ear_time_s, ear_reciever = content, timestamp, ''
        for member in members:
            if member['name'] != user:
                ear_reciever += member['name'] + ', '
        ear_reciever = ear_reciever[:-2]
    elif timestamp < ear_time_r and sender != user:
        ear_mes_r, ear_time_r, ear_sender = content, timestamp, sender

def find_time(message):
    '''
    Counts the hour of each message sent by user. Returns None.
    '''
    if message['sender_name'] == user:
        message_times[(datetime.fromtimestamp(message['timestamp_ms']/1000).hour)] += 1

if __name__ == '__main__':
    json_reader()
    print('Most commonly used words in your chats: ')
    for word in everyone_words.most_common(10):
        print(word)
    print('Most commony used words by you: ')
    for word in user_words.most_common(10):
        print(word)
    print('Most commonly used reacts in your chats: ')
    for react in everyone_reacts.most_common(8):
        print(react)
    print('Most commonly used reacts by you: ')
    for react in user_reacts.most_common(8):
        print(react)
    print('First message recieved: ' + ear_mes_r + ' ***', datetime.fromtimestamp(ear_time_r/1000), 'from ' + ear_sender + ' ***')
    print('First message sent: ' + ear_mes_s + ' ***', datetime.fromtimestamp(ear_time_s/1000), 'sent to ' + ear_reciever + ' ***')
    print('You text the most often around', message_times.most_common(1)[0][0], 'and you\'ve sent', message_times.most_common(1)[0][1], 'messages.')