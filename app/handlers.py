from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import app.keyboards as kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import time

router = Router()

class standgold(StatesGroup):
    gold = State()
    bank = State()
    verify = State()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    state.clear
    await message.answer(f'👋Здравствуйте {message.from_user.first_name},\n 🏠Главное меню.\n'
                        f'🔢Для взаимодействия с ботом используй клавиатуру.\n'
                        f'⚡️ Для покупки голды перейди в раздел «💵 Купить».\n'
                        f'📖 Если у тебя возникли вопросы, обращайся в поддержку.', reply_markup=kb.main)
    
    
@router.message(F.text == '🏠Главное меню')
async def cmd_start(message: Message, state: FSMContext):
    state.clear
    await message.answer(f'👋Здравствуйте {message.from_user.first_name},\n 🏠Главное меню.\n'
                        f'🔢Для взаимодействия с ботом используй клавиатуру.\n'
                        f'⚡️ Для покупки голды перейди в раздел «💵 Купить».\n'
                        f'📖 Если у тебя возникли вопросы, обращайся в поддержку.', reply_markup=kb.main)
    


@router.message(F.text == '💵Купить')
async def buy(message: Message, state: FSMContext):
    await state.set_state(standgold.gold)
    await message.answer(f'🍯 Чтобы купить голду, введи в чат сумму ₽ на которую хочешь пополнить баланс. \n 💡 Например: 100', reply_markup=kb.menu)
    
    
@router.message(standgold.gold)
async def sum(message: Message, state: FSMContext):    
    try:
        golds = int(message.text)
        rub = int(golds)
        golda = round(golds / 0.66, 2)
        await state.update_data(gold=message.text)
        await message.answer(f'📝 За {rub} ₽ ты получаешь {golda} голды. Для пополнения баланса выбери наиболее удобный тебе способ оплаты:', reply_markup=kb.bank) 
        await state.set_state(standgold.bank)
    except Exception:
        message.answer('Введите целое число')
    
@router.callback_query(F.data == 'Back')
async def Back(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    golda = int(data['gold'])
    await callback.message.answer(f'📝 За {golda} ₽ ты получаешь {round(golda / 0.66, 2)} голды. Для пополнения баланса выбери наиболее удобный тебе способ оплаты:', reply_markup=kb.bank)
    await callback.answer('Вы вернулись назад')
    await callback.message.delete()

@router.callback_query(F.data == 'Edit')
async def Back(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    golda = int(data['gold'])
    await callback.message.answer(f'📝 За {golda} ₽ ты получаешь {round(golda / 0.66, 2)} голды. Для пополнения баланса выбери наиболее удобный тебе способ оплаты:', reply_markup=kb.bank)
    await callback.answer('Выберите способ оплаты')
    await callback.message.delete()

@router.callback_query(F.data == 'SBP')
async def SBP(callback: CallbackQuery, state:FSMContext):
    await callback.answer('Действуйте по инструкции')
    data = await state.get_data()
    golda = int(data['gold'])
    await callback.message.answer(f'📱Номер для перевода по СБП⚪️: +79087976609\n'
                                  f'💳Банк Тинькофф(Т.Банк)\n'
                                  f'❗️Получатель -Константин Александрович К.\n'
                                  f'💰 Сумма: {golda} ₽\n'
                                  f'🍯 Игровая комиссия рынка на нас.\n'
                                  f'♻️Вам на аккаунт придет ровно: {round(golda / 0.66, 2)}G\n\n'
                                  f'📸 После оплаты, нажмите «✅ Я перевел»', reply_markup=kb.Verify)
    await callback.message.delete()
    

@router.callback_query(F.data == 'Sberbank')
async def Sberbank(callback: CallbackQuery, state:FSMContext):
    await callback.answer('Действуйте по инструкции')
    data = await state.get_data()
    golda = int(data['gold'])
    await callback.message.answer(f'💳Карта🟢: 2202202013277409\n'
                                  f'❗️Получатель -Константин Александрович К.\n'
                                  f'💰 Сумма: {golda} ₽\n'
                                  f'🍯 Игровая комиссия рынка на нас.\n'
                                  f'♻️Вам на аккаунт придет ровно: {round(golda / 0.66, 2)}G\n\n'
                                  f'📸 После оплаты, нажмите «✅ Я перевел»', reply_markup=kb.Verify)
    await callback.message.delete()

@router.callback_query(F.data == 'Tinkoff')
async def Tinkoff(callback: CallbackQuery, state:FSMContext):
    await callback.answer('Действуйте по инструкции')
    data = await state.get_data()
    golda = int(data['gold'])
    await callback.message.answer(f'💳Карта🟡: 2200700817593386\n'
                                  f'❗️Получатель -Константин Александрович К.\n'
                                  f'💰 Сумма: {golda} ₽\n'
                                  f'🍯 Игровая комиссия рынка на нас.\n'
                                  f'♻️Вам на аккаунт придет ровно: {round(golda / 0.66, 2)}G\n\n'
                                  f'📸 После оплаты, нажмите «✅ Я перевел»', reply_markup=kb.Verify)
    await callback.message.delete()

@router.callback_query(F.data == 'Alfa')
async def Alfa(callback: CallbackQuery, state:FSMContext):
    await callback.answer('Действуйте по инструкции')
    data = await state.get_data()
    golda = int(data['gold'])
    await callback.message.answer(f'💳Карта🔴: 2200150818007889\n'
                                  f'❗️Получатель -Константин Александрович К.\n'
                                  f'💰 Сумма: {golda} ₽\n'
                                  f'🍯 Игровая комиссия рынка на нас.\n'
                                  f'♻️Вам на аккаунт придет ровно: {round(golda / 0.66, 2)}G\n\n'
                                  f'📸 После оплаты, нажмите «✅ Я перевел»', reply_markup=kb.Verify)
    await callback.message.delete()

@router.callback_query(F.data == 'Vtb')
async def Vtb(callback: CallbackQuery, state:FSMContext):
    await callback.answer('Действуйте по инструкции')
    data = await state.get_data()
    golda = int(data['gold'])
    await callback.message.answer(f'💳Карта🔵: 2200246001639031\n'
                                  f'❗️Получатель -Константин Александрович К.\n'
                                  f'💰 Сумма: {golda} ₽\n'
                                  f'🍯 Игровая комиссия рынка на нас.\n'
                                  f'♻️Вам на аккаунт придет ровно: {round(golda / 0.66, 2)}G\n\n'
                                  f'📸 После оплаты, нажмите «✅ Я перевел»', reply_markup=kb.Verify)
    await callback.message.delete()

@router.callback_query(F.data == 'Verify')
async def verify(callback: CallbackQuery, state: FSMContext):
    #await state.set_state(standgold.verify)
    await callback.answer('Действуйте по инструкции')
    await callback.message.answer('📸Скиньте сюда в чат скриншот перевода')
    await callback.message.answer('⁉️ Важно: не обрезайте скриншот, на нем должно быть видно дату, время и получателя.')
    await callback.message.delete()

@router.callback_query(F.data == 'Problem')
async def problem(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Действуйте по инструкции')
    await callback.message.answer(f'⁉️ Если у вас не получается перевести,' 
                                  f'попробуйте выбрать другой способ оплаты,\n'
                                  f'💡например «⚪️СБП | Другой банк».\n\n'
                                  f'Если проблема сохранилась, напишите нам ⤵️', reply_markup=kb.Faq)
    await callback.message.delete()


@router.message()
async def send_echo(message: Message):
    await message.answer(f'🤖я не понимаю вас, если появились проблемы с работой бота нажмите /start')