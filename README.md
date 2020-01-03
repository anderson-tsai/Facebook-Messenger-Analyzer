# Facebook Messenger Analyzer

Analyze all your Facebook messenger messages and chat with a chatbot trained on a conversation of your choosing.

Features:<br/>
    1. Shows most active chat<br/>
    2. Shows most used word/phrase/reactions<br/>
    3. First message ever<br/>
    4. Talk to a simulation of a friend/group chat through a chatbot trained with information from a conversation

## Installing

Download files, and download Facebook messenger history. Place folder titled "messages" into same directory as python files. Open "settings.ini" and change the variable names accordingly. Run analyzer.py to analyze messages, or run chatbot.py to create chatbot of conversation.

### Prerequisites

pip install:<br/>
    1. chatterbot<br/>
    2. chatterbot_corpus

### Troubleshooting

If you get an error like:

```
Resource stopwords not found.
  Please use the NLTK Downloader to obtain the resource:

  >>> import nltk
  >>> nltk.download('stopwords')
```

Copy and paste the following in a terminal or editor to fix:

```
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download()
```

Choose to download all corpus.

## Authors

* **Anderson Tsai** - [Github Page](https://github.com/PurpleBooth)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details