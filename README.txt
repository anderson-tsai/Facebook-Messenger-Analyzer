Facebook Messenger Analyzer

Features:
	1. Shows most active chat
	2. Shows most used word/phrase/reactions
	3. Shows type of content shown in chat
	4. First message ever
	5. Talk to a simulation of a friend/group chat through a chatterbot trained with information from a conversation

Dependencies:
	1. chatterbot
	2. chatterbot_corpus

How to use:
	Download message history from Facebook, and place messages folder in the same directory as the script. 
	Then run analyzer.py to analyze data and provide user statistics or run chatbot.py, and enter the name 
	of a group chat or the name of a person that you have chatted with, and get an interactive chatbot for a person or group.

To the name of user or file directory, edit only settings.ini

If you get an error like:

Resource stopwords not found.
  Please use the NLTK Downloader to obtain the resource:

  >>> import nltk
  >>> nltk.download('stopwords')

Copy and paste the following in a terminal or editor to fix:

import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download()

Choose to download all corpus