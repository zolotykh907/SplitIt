from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


TOKEN = '7739333487:AAH1D6lZRz8CNm1mRqVd9HpB125CEYD75BU'

keyboards = {'welcome':[[KeyboardButton(text="Мой токен")],
                        [KeyboardButton(text="Мои транзакции")],
                        [KeyboardButton(text="Новая транзакция")]],
             'cancel': [[KeyboardButton(text="Отмена")]]}

cancel_keyboard = ReplyKeyboardMarkup(
            keyboard=keyboards['cancel'],
            resize_keyboard=True
        )

welcome_keyboard = ReplyKeyboardMarkup(
        keyboard=keyboards['welcome'],
        resize_keyboard=True
    )

messages = {'not_in_system': 'Вы еще не зарегистрированы в системе. Введите /start для регистрации.'}