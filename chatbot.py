import os
import json
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import configparser

config = configparser.RawConfigParser()
config.read('settings.ini')

messages_dir = config.get('settings', 'messages_directory')
group = input('Enter name of chat or person\'s name: ')

def get_info(group):
    '''
    Finds specified group and retrieves all messages from the group. Returns a list of all the messages.
    '''
    sentences = []
    prev_user = None
    for filename in os.listdir(messages_dir):
        if group.lower().replace(' ', '') in filename.lower():
            for file_in_chat in os.listdir(os.path.join(messages_dir, filename)):
                if file_in_chat.lower().endswith('.json'):
                    with open(os.path.join(messages_dir, os.path.join(filename, file_in_chat))) as f:
                        data = json.load(f)
                        for message in reversed(data['messages']):
                            sender = message['sender_name']
                            if 'content' in message.keys():
                                if prev_user != sender:
                                    sentences.append(message['content'])
                                else:
                                    sentences[-1] = sentences[-1] + '. ' + message['content']
                            if prev_user != sender:
                                prev_user = sender

 
            break
    return sentences

def remove_starter_files():
    '''
    Removes trained data from previous runs so that data is new. Returns None
    '''
    for filename in os.listdir():
        if filename == 'sentence_tokenizer.pickle' or filename == 'db.sqlite3-wal' or filename == 'db.sqlite3-shm' or filename == 'db.sqlite3':
            os.remove(filename)

chat_bot = ChatBot(name='PyBot', read_only=True,
                 logic_adapters=['chatterbot.logic.BestMatch'])
training_data = get_info(group)
trainer = ListTrainer(chat_bot)
trainer.train(training_data)

print('Type anything to the bot (Press CTRL+C to exit)')
try:
    while True:
        prompt = input('You: ')
        print(group + ': ', chat_bot.get_response(prompt))
except KeyboardInterrupt:
    remove_starter_files()
    print('\nSee you later!')