from bot.bot import Bot
from bot.handler import MessageHandler, BotButtonCommandHandler
import json
import random
import Update
TOKEN = "001.2415440181.2901955096:754789318"

bot = Bot(token=TOKEN)

agent_beta = Update.Beta(Update.CallBacksTexts.agent)
icq_beta = Update.Beta(Update.CallBacksTexts.icq)
agent_release = Update.Release(Update.CallBacksTexts.agent)
icq_release = Update.Release(Update.CallBacksTexts.icq)
myteam_release = Update.Release(Update.CallBacksTexts.myteam)

def responsible():
    testers = ("741451770", "yulichka_mitryaeva@mail.ru")
    return random.sample(list(testers), 2)

def get_beta_main_text(agent, icq):
    text = 'Уже протестированы беты:'
    if agent.is_ready() and icq.is_ready():
        text = 'Все беты протестированы. Поздравляю!'
    else:
        if agent.is_ready():
            text += '\n☑️ ' + Update.CallBacksTexts.agent.value[1]
        if icq.is_ready():
            text += '\n☑️ ' + Update.CallBacksTexts.icq.value[1]
    return text

def get_release_main_text(agent,myteam, icq):
    text = 'Уже протестированы релизы:'
    if agent.is_ready() and myteam.is_ready() and icq.is_ready():
        text = 'Все релизы протестированы. Поздравляю!'
    else:
        if agent.is_ready():
            text += '\n☑️ ' + Update.CallBacksTexts.agent.value[1]
        if myteam.is_ready():
            text += '\n☑️ ' + Update.CallBacksTexts.myteam.value[1]
        if icq.is_ready():
            text += '\n☑️ ' + Update.CallBacksTexts.icq.value[1]
    return text

def get_beta_main_buttons(agent, icq):
    mass_buttons = []
    if not agent.is_ready():
        button = [{"text": Update.CallBacksTexts.agent.value[1],
                   "callbackData": Update.CallBacksTexts.agent.value[0] + agent_beta.type_update.value[0]}]
        mass_buttons.append(button)
    if not icq.is_ready():
        button = [{"text": Update.CallBacksTexts.icq.value[1],
                   "callbackData": Update.CallBacksTexts.icq.value[0] + icq_beta.type_update.value[0]}]
        mass_buttons.append(button)
    if len(mass_buttons) == 0:
        return None
    else:
        return mass_buttons

def get_release_main_buttons(agent, myteam, icq):
    mass_buttons = []
    if not agent.is_ready():
        button = [{"text": Update.CallBacksTexts.agent.value[1],
                    "callbackData": Update.CallBacksTexts.agent.value[0] + agent_release.type_update.value[0]}]
        mass_buttons.append(button)
    if not myteam.is_ready():
        button = [{"text": Update.CallBacksTexts.myteam.value[1],
                   "callbackData": Update.CallBacksTexts.myteam.value[0] + myteam_release.type_update.value[0]}]
        mass_buttons.append(button)
    if not icq.is_ready():
        button = [{"text": Update.CallBacksTexts.icq.value[1],
                   "callbackData": Update.CallBacksTexts.icq.value[0] + icq_release.type_update.value[0]}]
        mass_buttons.append(button)
    if len(mass_buttons) == 0:
        return None
    else:
        return mass_buttons

def buttons_answer_cb(bot, event):
    if 'beta' in event.data['callbackData']:
        if 'back' in event.data['callbackData']:
            bot.send_text(
                text=get_beta_main_text(agent_beta, icq_beta),
                chat_id=event.data['message']['chat']['chatId'],
                inline_keyboard_markup="{}".format(json.dumps(
                    get_beta_main_buttons(agent_beta, icq_beta)
                )))
        elif 'agent' in event.data['callbackData']:
            if event.data['callbackData'] == Update.CallBacksTexts.agent.value[0] + agent_beta.type_update.value[0]:
                bot.send_text(
                    text=agent_beta.description(),
                    chat_id=event.data['message']['chat']['chatId'],
                    inline_keyboard_markup="{}".format(json.dumps(
                        agent_beta.get_buttons()
                    )))
            else:
                for platform, state in agent_beta.platforms.items():
                    if platform.value[0] in event.data['callbackData']:
                        agent_beta.platforms[platform] = Update.State.tested
                        if not agent_beta.is_ready():
                            bot.send_text(
                                text=agent_beta.description(),
                                chat_id=event.data['message']['chat']['chatId'],
                                inline_keyboard_markup="{}".format(json.dumps(
                                    agent_beta.get_buttons()
                                )))
                            bot.answer_callback_query(
                                query_id=event.data['queryId'],
                                text="Ты успешно проверил " + platform.value[1] + ', ты молодец 😻',
                                show_alert=False
                            )
                        else:
                            if get_beta_main_buttons(agent_beta, icq_beta) is None:
                                bot.send_text(
                                    text=get_beta_main_text(agent_beta, icq_beta),
                                    chat_id=event.data['message']['chat']['chatId']
                                )
                                bot.answer_callback_query(
                                    query_id=event.data['queryId'],
                                    text="Ты успешно проверил " + platform.value[1] + ', ты молодец 😻',
                                    show_alert=False
                                )
                            else:
                                bot.send_text(
                                    text=get_beta_main_text(agent_beta, icq_beta),
                                    chat_id=event.data['message']['chat']['chatId'],
                                    inline_keyboard_markup="{}".format(json.dumps(
                                        get_beta_main_buttons(agent_beta, icq_beta)
                                    )))
                                bot.answer_callback_query(
                                    query_id=event.data['queryId'],
                                    text="Ты успешно проверил " + platform.value[1] + ', ты молодец 😻',
                                    show_alert=False
                                )

        elif 'icq' in event.data['callbackData']:
            if event.data['callbackData'] == Update.CallBacksTexts.icq.value[0]+icq_beta.type_update.value[0]:
                bot.send_text(
                    text=icq_beta.description(),
                    chat_id=event.data['message']['chat']['chatId'],
                    inline_keyboard_markup="{}".format(json.dumps(
                        icq_beta.get_buttons()
                    )))
            else:
                for platform, state in icq_beta.platforms.items():
                    if platform.value[0] in event.data['callbackData']:
                        icq_beta.platforms[platform] = Update.State.tested
                        if not icq_beta.is_ready():
                            bot.send_text(
                                text=icq_beta.description(),
                                chat_id=event.data['message']['chat']['chatId'],
                                inline_keyboard_markup="{}".format(json.dumps(
                                    icq_beta.get_buttons()
                                )))
                            bot.answer_callback_query(
                                query_id=event.data['queryId'],
                                text="Ты успешно проверил " + platform.value[1] + ', ты молодец 😻',
                                show_alert=False
                            )
                        else:
                            if get_beta_main_buttons(agent_beta, icq_beta) is None:
                                bot.send_text(
                                    text=get_beta_main_text(agent_beta, icq_beta),
                                    chat_id=event.data['message']['chat']['chatId']
                                )
                                bot.answer_callback_query(
                                    query_id=event.data['queryId'],
                                    text="Ты успешно проверил " + platform.value[1] + ', ты молодец 😻',
                                    show_alert=False
                                )
                            else:
                                bot.send_text(
                                    text=get_beta_main_text(agent_beta, icq_beta),
                                    chat_id=event.data['message']['chat']['chatId'],
                                    inline_keyboard_markup="{}".format(json.dumps(
                                        get_beta_main_buttons(agent_beta, icq_beta)
                                    )))
                                bot.answer_callback_query(
                                    query_id=event.data['queryId'],
                                    text="Ты успешно проверил " + platform.value[1] + ', ты молодец 😻',
                                    show_alert=False
                                )

    elif 'release' in event.data['callbackData']:
        if 'back' in event.data['callbackData']:
            bot.send_text(
                text=get_release_main_text(agent_release, myteam_release, icq_release),
                chat_id=event.data['message']['chat']['chatId'],
                inline_keyboard_markup="{}".format(json.dumps(
                    get_release_main_buttons(agent_release, myteam_release, icq_release)
                )))
        elif 'agent' in event.data['callbackData']:
            if event.data['callbackData'] == Update.CallBacksTexts.agent.value[0]+agent_release.type_update.value[0]:
                bot.send_text(
                    text=agent_release.description(),
                    chat_id=event.data['message']['chat']['chatId'],
                    inline_keyboard_markup="{}".format(json.dumps(
                        agent_release.get_buttons()
                    )))
            else:
                for platform, state in agent_release.platforms.items():
                    if platform.value[0] in event.data['callbackData']:
                        agent_release.platforms[platform] = Update.State.tested
                        if not agent_release.is_ready():
                            bot.send_text(
                                text=agent_release.description(),
                                chat_id=event.data['message']['chat']['chatId'],
                                inline_keyboard_markup="{}".format(json.dumps(
                                    agent_release.get_buttons()
                                )))
                            bot.answer_callback_query(
                                query_id=event.data['queryId'],
                                text="Ты успешно проверил " + platform.value[1] + ', ты молодец 😻',
                                show_alert=False
                            )
                        else:
                            if get_release_main_buttons(agent_release, myteam_release, icq_release) is None:
                                bot.send_text(
                                    text=get_release_main_text(agent_release, myteam_release, icq_release),
                                    chat_id=event.data['message']['chat']['chatId']
                                )
                                bot.answer_callback_query(
                                    query_id=event.data['queryId'],
                                    text="Ты успешно проверил " + platform.value[1] + ', ты молодец 😻',
                                    show_alert=False
                                )
                            else:
                                bot.send_text(
                                    text=get_release_main_text(agent_release, myteam_release, icq_release),
                                    chat_id=event.data['message']['chat']['chatId'],
                                    inline_keyboard_markup="{}".format(json.dumps(
                                        get_release_main_buttons(agent_release, myteam_release, icq_release)
                                    )))
                                bot.answer_callback_query(
                                    query_id=event.data['queryId'],
                                    text="Ты успешно проверил " + platform.value[1] + ', ты молодец 😻',
                                    show_alert=False
                                )
        elif 'myteam' in event.data['callbackData']:
            if event.data['callbackData'] == Update.CallBacksTexts.myteam.value[0]+myteam_release.type_update.value[0]:
                bot.send_text(
                    text=myteam_release.description(),
                    chat_id=event.data['message']['chat']['chatId'],
                    inline_keyboard_markup="{}".format(json.dumps(
                        myteam_release.get_buttons()
                    )))
            else:
                for platform, state in myteam_release.platforms.items():
                    if platform.value[0] in event.data['callbackData']:
                        myteam_release.platforms[platform] = Update.State.tested
                        if not myteam_release.is_ready():
                            bot.send_text(
                                text=myteam_release.description(),
                                chat_id=event.data['message']['chat']['chatId'],
                                inline_keyboard_markup="{}".format(json.dumps(
                                    myteam_release.get_buttons()
                                )))
                            bot.answer_callback_query(
                                query_id=event.data['queryId'],
                                text="Ты успешно проверил " + platform.value[1] + ', ты молодец 😻',
                                show_alert=False
                            )
                        else:
                            if get_release_main_buttons(agent_release, myteam_release, icq_release) is None:
                                bot.send_text(
                                    text=get_release_main_text(agent_release, myteam_release, icq_release),
                                    chat_id=event.data['message']['chat']['chatId']
                                )
                                bot.answer_callback_query(
                                    query_id=event.data['queryId'],
                                    text="Ты успешно проверил " + platform.value[1] + ', ты молодец 😻',
                                    show_alert=False
                                )
                            else:
                                bot.send_text(
                                    text=get_release_main_text(agent_release, myteam_release, icq_release),
                                    chat_id=event.data['message']['chat']['chatId'],
                                    inline_keyboard_markup="{}".format(json.dumps(
                                        get_release_main_buttons(agent_release, myteam_release, icq_release)
                                    )))
                                bot.answer_callback_query(
                                    query_id=event.data['queryId'],
                                    text="Ты успешно проверил " + platform.value[1] + ', ты молодец 😻',
                                    show_alert=False
                                )
        elif 'icq' in event.data['callbackData']:
            if event.data['callbackData'] == Update.CallBacksTexts.icq.value[0]+icq_release.type_update.value[0]:
                bot.send_text(
                    text=icq_release.description(),
                    chat_id=event.data['message']['chat']['chatId'],
                    inline_keyboard_markup="{}".format(json.dumps(
                        icq_release.get_buttons()
                    )))
            else:
                for platform, state in icq_release.platforms.items():
                    if platform.value[0] in event.data['callbackData']:
                        icq_release.platforms[platform] = Update.State.tested
                        if not icq_release.is_ready():
                            bot.send_text(
                                text=icq_release.description(),
                                chat_id=event.data['message']['chat']['chatId'],
                                inline_keyboard_markup="{}".format(json.dumps(
                                    icq_release.get_buttons()
                                )))
                            bot.answer_callback_query(
                                query_id=event.data['queryId'],
                                text="Ты успешно проверил " + platform.value[1] + ', ты молодец 😻',
                                show_alert=False
                            )
                        else:
                            if get_release_main_buttons(agent_release, myteam_release, icq_release) is None:
                                bot.send_text(
                                    text=get_release_main_text(agent_release, myteam_release, icq_release),
                                    chat_id=event.data['message']['chat']['chatId']
                                )
                                bot.answer_callback_query(
                                    query_id=event.data['queryId'],
                                    text="Ты успешно проверил " + platform.value[1] + ', ты молодец 😻',
                                    show_alert=False
                                )
                            else:
                                bot.send_text(
                                    text=get_release_main_text(agent_release, myteam_release, icq_release),
                                    chat_id=event.data['message']['chat']['chatId'],
                                    inline_keyboard_markup="{}".format(json.dumps(
                                        get_release_main_buttons(agent_release, myteam_release, icq_release)
                                    )))
                                bot.answer_callback_query(
                                    query_id=event.data['queryId'],
                                    text="Ты успешно проверил " + platform.value[1] + ', ты молодец 😻',
                                    show_alert=False
                                )

def message_cb(bot, event):
    if event.text == '/start' or event.text == '/help':
        bot.send_text(
            chat_id=event.from_chat,
            text='Список команд UpdateQABot:\n '
                 '/startBeta - Начинаем тестирование беты!\n '
                 '/startRelease - Начинаем тестирование релиза!\n '
                 '/currentBeta - Тестирование беты уже идет, присоединяйся!\n '
                 '/currentRelease - Тестирование релиза уже идет, присоединяйся!\n'
                 '/help - Список команд, чтобы не потерять 📒'
        )
    elif event.text == '/startBeta':
        global agent_beta
        agent_beta = Update.Beta(Update.CallBacksTexts.agent)
        global icq_beta
        icq_beta = Update.Beta(Update.CallBacksTexts.icq)
        test_user = responsible()
        bot.send_text(
            chat_id=event.from_chat,
            text=f'@[{test_user[0]}] и @[{test_user[1]}] \n Начинаем тестирование беты! ',
            inline_keyboard_markup="{}".format(json.dumps(
                get_beta_main_buttons(agent_beta, icq_beta)
            )))
    elif event.text == '/startRelease':
        global agent_release
        agent_release = Update.Release(Update.CallBacksTexts.agent)
        global icq_release
        icq_release = Update.Release(Update.CallBacksTexts.icq)
        global myteam_release
        myteam_release = Update.Release(Update.CallBacksTexts.myteam)
        test_user = responsible()
        bot.send_text(
            chat_id=event.from_chat,
            text=f'@[{test_user[0]}] и @[{test_user[1]}] \n Начинаем тестирование релиза! ',
            inline_keyboard_markup="{}".format(json.dumps(
                get_release_main_buttons(agent_release, myteam_release, icq_release)
            )))
    elif event.text == '/currentBeta':
        bot.send_text(
            chat_id=event.from_chat,
            text=get_beta_main_text(agent_beta, icq_beta),
            inline_keyboard_markup="{}".format(json.dumps(
                get_beta_main_buttons(agent_beta, icq_beta)
            )))
    elif event.text == '/currentRelease':
        bot.send_text(
            chat_id=event.from_chat,
            text=get_release_main_text(agent_release, myteam_release, icq_release),
            inline_keyboard_markup="{}".format(json.dumps(
                get_release_main_buttons(agent_release, myteam_release, icq_release)
            )))

bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
bot.dispatcher.add_handler(BotButtonCommandHandler(callback=buttons_answer_cb))

bot.start_polling()
bot.idle()
