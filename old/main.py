import asyncio
import secrets

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

TOKEN = '7739333487:AAH1D6lZRz8CNm1mRqVd9HpB125CEYD75BU'

bot = Bot(token=TOKEN)
dp = Dispatcher()

class States(StatesGroup):
    username_wait = State()
    amount_wait = State()

tokens = {}
user_ids = {}
transactions = {}

@dp.message(Command("start"))
async def send_welcome(message):
    user_id = message.from_user.username

    if user_id in tokens:
        token = tokens[user_id]
        await message.answer(f'Ваш токен для входа в систему уже существует: '
                             f'`{token}`', parse_mode='Markdown')
    else:
        token = secrets.token_hex(16)
        tokens[user_id] = token
        user_ids[user_id] = message.from_user.id  # Добавляем Telegram ID пользователя
        await message.answer(f'Ваш токен:\n`{token}`', parse_mode='Markdown')

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Мой токен")],
            [KeyboardButton(text="Мои транзакции")],
            [KeyboardButton(text="Новая транзакция")]
        ], resize_keyboard=True
    )

    await message.answer("Добро пожаловать!", reply_markup=keyboard)

@dp.message(lambda message: message.text.lower() == "мой токен")
async def get_personal_token(message):
    user_id = message.from_user.username

    if user_id in tokens:
        token = tokens[user_id]
        await message.answer(f'Ваш токен для входа в систему: '
                             f'`{token}`', parse_mode='Markdown')
    else:
        await message.answer(f'Вы еще не зарегистрированы в системе. Введите /start для регистрации.')
    print(user_ids)

@dp.message(lambda message: message.text.lower() == "новая транзакция")
async def ask_for_username(message, state):
    user_id = message.from_user.username
    if user_id in tokens:
        await state.set_state(States.username_wait)
        await message.answer("Введите имя пользователя, для которого нужно создать новую транзакцию:")
    else:
        await message.answer(f'Вы еще не зарегистрированы в системе. Введите "/start" для регистрации.')

@dp.message(States.username_wait)
async def get_username_for_transaction(message, state):
    username = message.text
    if username in tokens:
        await state.update_data(username = username)
        await state.set_state(States.amount_wait)
        await message.answer(f'Введите сумму для @{username}')
    else:
        await message.answer(f'Такого пользователя не существует либо он не зарегистрирован в системе')
        await state.clear()

@dp.message(States.amount_wait)
async def get_transaction_amount(message: types.Message, state: FSMContext):
    try:
        success_transaction = False
        amount = int(message.text)

        data = await state.get_data()
        username = data.get('username')

        user_id = message.from_user.username
        if user_id not in transactions:
            transactions[user_id] = []

        for i in range(len(transactions[user_id])):
            if transactions[user_id][i]['username'] == username:
                transactions[user_id][i]['amount'] += amount
                success_transaction = True
                break

        if not success_transaction:
            transactions[user_id].append({"username": username, "amount": amount})

        await bot.send_message(user_ids[username], f'С вами была совершена транзакция на сумму {amount} '
                                                        f'с пользователем @{user_id}')
        await message.answer(f"Транзакция на сумму {amount} с @{username} успешно создана.")

        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите корректную сумму.")


@dp.message(lambda message: message.text.lower() == "мои транзакции" or Command("my_transaction"))
async def get_my_transaction(message):
    user_id = message.from_user.username
    if user_id in tokens:
        if user_id in transactions:
            await message.answer(f'Ваши транзакции: {transactions[user_id]}')
        else:
            await message.answer(f'У вас еще нет транзакций')
    else:
        await message.answer(f'Вы еще не зарегистрированы в системе. Введите "/start" для регистрации.')

async def main():
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

