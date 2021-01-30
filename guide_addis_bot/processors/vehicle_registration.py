from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, state_types
from django_tgbot.types.replykeyboardremove import ReplyKeyboardRemove
from django_tgbot.types.update import Update

from guide_addis_bot.bot import state_manager, TelegramBot
from guide_addis_bot.models import TelegramState
from ..utils import create_vehicle


@processor(state_manager, from_states='asked_for_choice', message_types=message_types.Text)
def handle_choice(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    text = update.get_message().get_text()

    if text == 'Register your vehicle':
        bot.sendMessage(chat_id,
                        'What is your car\'s make?',
                        reply_markup=ReplyKeyboardRemove.a(remove_keyboard=True))
        state.set_name('asked_for_make')
    else:
        bot.sendMessage(chat_id, 'I didn\'t get that! Use the keyboard below')


@processor(state_manager, from_states='asked_for_make', success='asked_for_model', fail=state_types.Keep,
           message_types=message_types.Text)
def get_name(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    make = update.get_message().get_text()

    # TODO: Validation should be added here. If not valid raise a ProcessFailure
    # if len(make) < 3:
    #     bot.sendMessage(chat_id, 'Name is too short! Try again:')
    #     raise ProcessFailure

    state.set_memory({
        'make': make
    })

    bot.sendMessage(chat_id, 'Beautiful! What is car\'s model?')


@processor(state_manager, from_states='asked_for_model', success=state_types.Reset, fail=state_types.Keep,
           message_types=message_types.Text)
def get_email(bot, update, state):
    chat_id = update.get_chat().get_id()
    model = update.get_message().get_text()

    make = state.get_memory()['make']

    create_vehicle(make=make, model=model, number_of_seats=4)
    bot.sendMessage(chat_id,
                    'Thanks! You successfully registered your vehicle with detail:\nName: {}\nEmail: {}'.format(make,
                                                                                                                model))

    state.set_memory({})
