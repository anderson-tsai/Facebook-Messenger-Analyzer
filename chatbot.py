import os
import json
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import configparser
import tkinter as tk

config = configparser.RawConfigParser()
config.read('settings.ini')

messages_dir = config.get('settings', 'messages_directory')

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

'''
ChatBotGUI class modified from https://github.com/gunthercox/ChatterBot/blob/master/examples/tkinter_gui.py
'''
try:
    import ttk as ttk
    import ScrolledText
except ImportError:
    import tkinter.ttk as ttk
    import tkinter.scrolledtext as ScrolledText
import time


class ChatBotGUI(tk.Tk):

    def __init__(self, chat_name, *args, **kwargs):
        """
        Create & set window variables.
        """
        tk.Tk.__init__(self, *args, **kwargs)
        remove_starter_files()
        self.chat_name = chat_name
        self.chatbot = ChatBot(
            self.chat_name,
            storage_adapter="chatterbot.storage.SQLStorageAdapter",
            logic_adapters=[
                "chatterbot.logic.BestMatch"
            ],
            database_uri="sqlite:///database.sqlite3"
        )

        self.trainer = ListTrainer(self.chatbot)
        self.trainer.train(get_info(chat_name))

        self.title(chat_name)

        self.initialize()

    def initialize(self):
        """
        Set window layout.
        """
        self.grid()

        self.respond = ttk.Button(self, text='Get Response', command=self.get_response)
        self.respond.grid(column=0, row=0, sticky='nesw', padx=3, pady=3)

        self.usr_input = ttk.Entry(self, state='normal')
        self.usr_input.grid(column=1, row=0, sticky='nesw', padx=3, pady=3)

        self.conversation_lbl = ttk.Label(self, anchor=tk.E, text='Conversation:')
        self.conversation_lbl.grid(column=0, row=1, sticky='nesw', padx=3, pady=3)

        self.conversation = ScrolledText.ScrolledText(self, state='disabled')
        self.conversation.grid(column=0, row=2, columnspan=2, sticky='nesw', padx=3, pady=3)

    def get_response(self):
        """
        Get a response from the chatbot and display it.
        """
        user_input = self.usr_input.get()
        self.usr_input.delete(0, tk.END)

        response = self.chatbot.get_response(user_input)

        self.conversation['state'] = 'normal'
        self.conversation.insert(
            tk.END, "You: " + user_input + "\n" + self.chat_name + ": " + str(response.text) + "\n"
        )
        self.conversation['state'] = 'disabled'

def run_from_gui(chat_name):
    chatbot = ChatBotGUI(chat_name)
    chatbot.mainloop()

#Used to run from terminal
if __name__ == '__main__':
    group = input('Enter name of chat or person\'s name: ')
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