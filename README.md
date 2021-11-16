# jpFlash
The is a tool to scrape Japanese information from JLPT sensei and generate Anki flashcards.

[Anki](https://apps.ankiweb.net/) is a flashcard software that uses Spaced repetition learning to efficiently teach you information, but for most subjects the decks need to be created by oneself.
For learning Japanese there are many websites that provide lots of grammar and vocabulary such as [JLPTSensei](https://jlptsensei.com/). Manually generating flashcards from each of the example sentences can be time consuming. 
JPFlash uses beautiful soup to scrape the grammar portion of the website and save the example sentences, translations, etc to a SQLite database. It then generates flashcards in Anki, using the Anki Connect API.  
It operates through a command line interface.

## Installation
1. Clone the repo
2. Install the requirements
   ``` 
   pip install -r requirements.txt 
   ```

## Usage
This script generates flashcards using anki. To properly generate flashcards, [anki](https://apps.ankiweb.net/) and [ankiconnect](https://foosoft.net/projects/anki-connect/) must be installed and anki must be running.

For Anki Connect to work, the deck name "Japanese Grammar::\<level\>" must be created previously in anki and the Note Type "Japanese Grammar" must be created

1. Run the python script 
``` 
python3 main.py
```
2. Select the function you want to use. i.e. "d" to make the database, "s" to scrape grammar, "h" to list the options
   \*Note\* Make sure you generate the database before scraping

