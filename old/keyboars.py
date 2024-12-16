from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboards = {'welcome':[[KeyboardButton(text="Мой токен")],
                        [KeyboardButton(text="Мои транзакции")],
                        [KeyboardButton(text="Новая транзакция")]],
             'cancel': [[KeyboardButton(text="Отмена")]]}