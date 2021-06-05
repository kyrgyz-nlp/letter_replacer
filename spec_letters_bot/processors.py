from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from corrector.ai import correct_sentence
from .bot import state_manager
from .models import TelegramState
from .bot import TelegramBot


ANSWERED = 'answered'
STARTED = 'started'


@processor(state_manager, from_states=state_types.Reset, success=STARTED)
def start(bot: TelegramBot, update: Update, state: TelegramState):
    text = 'Insert your text'
    chat_id = update.get_chat().get_id()
    bot.sendMessage(chat_id, text)


@processor(state_manager, from_states=[state_types.Reset, STARTED, ANSWERED], success=ANSWERED)
def send_comment(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    msg = update.get_message().get_text()
    corr = correct_sentence(msg)
    bot.sendMessage(chat_id, corr)
