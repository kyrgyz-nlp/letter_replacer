# ӨҮҢизатор -- Telegram bot that replaces incorrectly used 'О', 'У', and 'Н' with 'Ө', 'Ү', or 'Ң'.


### Note: the bot is just a proof of concept. If you are interested in enhancing it, I'll be happy to help to collaborate!


## Installation

1. Pull the repository
2. Create a virtual env and activate it
3. Install dependencies: pip install -r requirements.txt
4. Download and copy the trained models (links are given below) to the root of the project (the same directory where `manage.py` lives)


## Links to models
1. [Unsupervised model (Kloop model)](https://github.com/kyrgyz-nlp/letter_replacer/releases/download/v0.1-alpha/kloop_with_books_model.bin)
2. [Ң vs Н classification model](https://github.com/kyrgyz-nlp/letter_replacer/releases/download/v0.1-alpha/n_and_n_umlaut_dataset.bin)
3. [Ө vs О classification model](https://github.com/kyrgyz-nlp/letter_replacer/releases/download/v0.1-alpha/o_and_o_umlaut_dataset.bin)
4. [Ү vs У classification model](https://github.com/kyrgyz-nlp/letter_replacer/releases/download/v0.1-alpha/u_and_u_umlaut_dataset.bin)


## To run you instance of a bot, you should do the following:
1. Create `.env` file (just rename the template file `env_template` to `.env`)
2. Go to Telegram's Botfather and register a new bot
3. Write its credentials (BOT_TOKEN and BOT_USERNAME) there
4. Activate you virtual env and run `python manage.py tgbotwebhook`. After that you will see a prompt `Enter bot username:`. Write there your bot's username and as the next step you'll have to choose one of the two options. Select 1 and set your hostname (example: https://yourawesomesite.com).
5. Find your bot and send some sentences, for example: `комур жакканда зыян тутун чыгат`. The bot will respond with `көмүр жакканда зыян түтүн чыгат`.


## Running locally
1. Register your bot and setup the project (see the previous section)
1. Download and run `ngrok` (e.g. ./ngrok http 8000)
2. Run your django (e.g. ./manage.py runserver 8000)
3. Register your ngrok's URL as a host for webhook by running `python manage.py tgbotwebhook` (e.g. https://ff24e741518f.ngrok.io). See Step #4 of the previous section of this README.
4. Now your bot can be served from your local computer!
