from aiogram.filters import Command
from aiogram import Dispatcher
from aiogram.fsm.state import StatesGroup, State

from func import tokens, user_ids, create_token, add_transaction, get_user_transactions
from config import cancel_keyboard, welcome_keyboard, messages


class States(StatesGroup):
    username_wait = State()
    amount_wait = State()


async def send_welcome(message):
    user_id = message.from_user.username

    if user_id in tokens:
        token = tokens[user_id]
        await message.answer(f'Ваш токен для входа в систему уже существует: '
                             f'`{token}`', parse_mode='Markdown')
    else:
        token = create_token(message.from_user.id, user_id, message.bot)
        await message.answer(f'Ваш токен:\n`{token}`', parse_mode='Markdown')



    await message.answer("Добро пожаловать!")#, reply_markup=welcome_keyboard)


async def get_personal_token(message):
    user_id = message.from_user.username

    if user_id in tokens:
        token = tokens[user_id]
        await message.answer(f'Ваш токен для входа в систему: '
                             f'`{token}`', parse_mode='Markdown')
    else:
        await message.answer(messages['not_in_system'])


async def new_transaction(message, state):
    user_id = message.from_user.username
    if user_id in tokens:
        await state.set_state(States.username_wait)


        await message.answer("Введите имя пользователя, для которого нужно создать транзакцию",
                             reply_markup=cancel_keyboard)
    else:
        await message.answer(messages['not_in_system'])


async def get_username_for_transaction(message, state):
    username = message.text
    if username.startswith('@'):
        username = username[1:]
    if username in tokens:
        await state.update_data(username=username)
        await state.set_state(States.amount_wait)

        await message.answer(f"Введите сумму для @{username}.", reply_markup=cancel_keyboard)
    else:
        await message.answer(f'Такого пользователя не существует либо он не зарегистрирован в системе, '
                             f'повотрите попытку')


async def get_transaction_amount(message, state):
    amount = message.text
    if not amount.isdigit() and not (amount.startswith('-') and amount[1:].isdigit()):
        await message.answer("Пожалуйста, введите корректную сумму.")
    else:
        amount = int(amount)
        data = await state.get_data()
        username = data.get('username')

        user_id = message.from_user.username

        reset_transaction = add_transaction(user_id, username, amount)

        recipient_user_id = user_ids.get(username)
        if recipient_user_id:
            await message.bot.send_message(recipient_user_id,f'С вами была совершена транзакция на сумму {amount}'
                                                                  f' с пользователем @{user_id}')

        await message.answer(f"Транзакция на сумму {amount} с @{username} успешно создана.")
        await state.clear()

        if not reset_transaction:
            await message.answer('Долг погашен, транзакция удалена')
            if recipient_user_id:
                await message.bot.send_message(recipient_user_id, 'Долг погашен, транзакция удалена')

        #await message.answer("Вы вернулись в главное меню.", reply_markup=welcome_keyboard)


async def get_my_transactions(message):
    user_id = message.from_user.username
    if user_id in tokens:
        user_transactions = get_user_transactions(user_id)
        if user_transactions:
            answer = ''
            for user_transaction in user_transactions:
                answer += f'@{user_transaction["username"]}: {user_transaction["amount"]}\n'
            await message.answer(f'Ваши транзакции:\n{answer}')
        else:
            await message.answer(f'У вас нет транзакций')
    else:
        await message.answer(messages['not_in_system'])


async def cancel_handler(message, state):
    await state.clear()

    await message.answer("Ввод отменен.")#, reply_markup=welcome_keyboard)

async def delete_profile(message):
    user_id = message.from_user.username
    if user_id in tokens:
        del tokens[user_id]
        await message.answer(f"Ваш профиль был успешно удален.")
    else:
        await message.answer(messages['not_in_system'])
def register_handlers(dp: Dispatcher):
    # dp.message.register(send_welcome, Command("start"))
    # dp.message.register(cancel_handler, lambda message: message.text.lower() == "отмена")
    # dp.message.register(get_personal_token, lambda message: message.text.lower() == "мой токен")
    # dp.message.register(new_transaction, lambda message: message.text.lower() == "новая транзакция")
    # dp.message.register(get_username_for_transaction, States.username_wait)
    # dp.message.register(get_transaction_amount, States.amount_wait)
    # dp.message.register(get_my_transactions, lambda message: message.text.lower() == "мои транзакции")
    # dp.message.register(delete_profile, Command("delete"))
    dp.message.register(send_welcome, Command("start"))
    dp.message.register(cancel_handler, lambda message: message.text.lower() == "отмена")
    dp.message.register(get_personal_token, Command("my_token"))
    dp.message.register(new_transaction, Command("new_transaction"))
    dp.message.register(get_username_for_transaction, States.username_wait)
    dp.message.register(get_transaction_amount, States.amount_wait)
    dp.message.register(get_my_transactions, Command("my_transactions"))
    dp.message.register(delete_profile, Command("delete"))
