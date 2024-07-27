import os
from dotenv import load_dotenv
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import app.keyboards as kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import app.database.requests as rq
from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode

bot = Bot(token=os.getenv('TG_TOKEN'))



router = Router()

class dialog(StatesGroup):
    sms = State()
    blacklist = State()
    whitelist = State()

class standgold(StatesGroup):
    id = State()
    gold = State()
    bank = State()
    verify = State()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(None)
    await rq.set_user(message.from_user.id)
    await message.answer(f'🏠Главное меню.\n'
                        f'👋Здравствуйте <b>{message.from_user.first_name}</b>,\n'
                        f'🔢Для взаимодействия с ботом используй клавиатуру.\n'
                        f'⚡️ Для покупки голды перейди в раздел «💵 <b>Купить</b>».\n'
                        f'📖 Если у тебя возникли вопросы, обращайся в <b>поддержку</b>.',parse_mode='HTML', reply_markup=kb.main)
    
    
@router.message(F.text == '🏠Главное меню')
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(None)
    await message.answer(f'🏠Главное меню.\n'
                        f'👋Здравствуйте <b>{message.from_user.first_name}</b>,\n'
                        f'🔢Для взаимодействия с ботом используй клавиатуру.\n'
                        f'⚡️ Для покупки голды перейди в раздел «💵 <b>Купить</b>».\n'
                        f'📖 Если у тебя возникли вопросы, обращайся в <b>поддержку</b>.',parse_mode='HTML', reply_markup=kb.main)

@router.message(F.text == '💵Купить')
async def buy(message: Message, state: FSMContext):
    await state.set_state(standgold.gold)
    await message.answer(f'🍯 Чтобы купить голду, \nвведи в чат <b>сумму в ₽ублях</b>\nна которую хочешь пополнить баланс. \n 💡 <b>Например</b>: <ins>100</ins>',parse_mode='HTML', reply_markup=kb.menu)
    
    
@router.message(standgold.gold)
async def sum(message: Message, state: FSMContext):    
    try:
        golds = int(message.text)
        rub = int(golds)
        if rub >= 100:
            golda = round(golds / 0.66, 2)
            await state.update_data(gold=message.text)
            await message.answer(f'📝 За <b>{rub}</b>₽ получаешь <b>{golda}</b>G. \nДля пополнения баланса выбери наиболее удобный тебе \nспособ оплаты:',parse_mode='HTML', reply_markup=kb.bank) 
            await state.set_state(standgold.bank)
        else:
            await message.answer(f'♻️Введите корректное число, минимум <b>100</b>₽', parse_mode='HTML')
    except Exception:
        await message.answer('🤖я не понимаю вас, если появились проблемы с работой бота нажмите \n<b>/start</b>', parse_mode='HTML')
    
@router.callback_query(F.data == 'Back', standgold.bank)
async def Back(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    golda = int(data['gold'])
    await callback.message.edit_text(f'📝 За <b>{golda}</b>₽ ты получаешь <b>{round(golda / 0.66, 2)}G</b>. \nДля пополнения баланса выбери наиболее удобный тебе способ оплаты:', parse_mode='HTML', reply_markup=kb.bank)
    await callback.answer('Вы вернулись назад')
    

@router.callback_query(F.data == 'Edit', standgold.bank)
async def Back(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Выберите способ оплаты')
    data = await state.get_data()
    golda = int(data['gold'])
    await callback.message.edit_text(f'📝 За <b>{golda}</b>₽ ты получаешь <b>{round(golda / 0.66, 2)}G</b>. \nДля пополнения баланса выбери наиболее удобный тебе способ оплаты:',parse_mode='HTML', reply_markup=kb.bank)


@router.callback_query(F.data == 'SBP', standgold.bank)
async def SBP(callback: CallbackQuery, state:FSMContext):
    await callback.answer('Действуйте по инструкции')
    await state.update_data(bank='⚪️СБП⚪️')
    data = await state.get_data()
    golda = int(data['gold'])
    await callback.message.edit_text(f'📱Номер для перевода по СБП⚪️: +79087976609\n'
                                  f'💳Банк <b>Тинькофф</b>(Т.Банк)\n'
                                  f'❗️Получатель <b>-Константин Александрович К</b>.\n'
                                  f'💰 Сумма: <b>{golda}</b>₽\n'
                                  f'🍯 <ins>Игровая комиссия рынка на нас</ins>.\n'
                                  f'♻️Вам на аккаунт придет ровно: <b>{round(golda / 0.66, 2)}</b>G\n\n'
                                  f'📸 После оплаты, <b>нажмите</b> «✅ Я перевел»',parse_mode='HTML', reply_markup=kb.Verify)
    
    

@router.callback_query(F.data == 'Sberbank', standgold.bank)
async def Sberbank(callback: CallbackQuery, state:FSMContext):
    await callback.answer('Действуйте по инструкции')
    await state.update_data(bank='🟢SBERBANK🟢')
    data = await state.get_data()
    golda = int(data['gold'])
    await callback.message.edit_text(f'💳Карта🟢: <b>2202202013277409</b>\n'
                                  f'❗️Получатель <b>-Константин Александрович К</b>.\n'
                                  f'💰 Сумма: <b>{golda}</b>₽\n'
                                  f'🍯 <ins>Игровая комиссия рынка на нас</ins>.\n'
                                  f'♻️Вам на аккаунт придет ровно: <b>{round(golda / 0.66, 2)}</b>G\n\n'
                                  f'📸 После оплаты, <b>нажмите</b> «✅ Я перевел»',parse_mode='HTML', reply_markup=kb.Verify)


@router.callback_query(F.data == 'Tinkoff', standgold.bank)
async def Tinkoff(callback: CallbackQuery, state:FSMContext):
    await callback.answer('Действуйте по инструкции')
    await state.update_data(bank='🟡Tinkoff🟡')
    data = await state.get_data()
    golda = int(data['gold'])
    await callback.message.edit_text(f'💳Карта🟡: <b>2200700817593386</b>\n'
                                  f'❗️Получатель <b>-Константин Александрович К</b>.\n'
                                  f'💰 Сумма: <b>{golda}</b>₽\n'
                                  f'🍯 <ins>Игровая комиссия рынка на нас</ins>.\n'
                                  f'♻️Вам на аккаунт придет ровно: <b>{round(golda / 0.66, 2)}</b>G\n\n'
                                  f'📸 После оплаты, <b>нажмите</b> «✅ Я перевел»',parse_mode='HTML', reply_markup=kb.Verify)


@router.callback_query(F.data == 'Alfa', standgold.bank)
async def Alfa(callback: CallbackQuery, state:FSMContext):
    await callback.answer('Действуйте по инструкции')
    await state.update_data(bank='🔴ALFA🔴')
    data = await state.get_data()
    golda = int(data['gold'])
    await callback.message.edit_text(f'💳Карта🔴: <b>2200150818007889</b>\n'
                                  f'❗️Получатель <b>-Константин Александрович К</b>.\n'
                                  f'💰 Сумма: <b>{golda}</b>₽\n'
                                  f'🍯 <ins>Игровая комиссия рынка на нас</ins>.\n'
                                  f'♻️Вам на аккаунт придет ровно: <b>{round(golda / 0.66, 2)}</b>G\n\n'
                                  f'📸 После оплаты, <b>нажмите</b> «✅ Я перевел»',parse_mode='HTML', reply_markup=kb.Verify)
  

@router.callback_query(F.data == 'Vtb', standgold.bank)
async def Vtb(callback: CallbackQuery, state:FSMContext):
    await callback.answer('Действуйте по инструкции')
    await state.update_data(bank='🔵ВТБ🔵')
    data = await state.get_data()
    golda = int(data['gold'])
    await callback.message.edit_text(f'💳Карта🔵: <b>2200246001639031</b>\n'
                                  f'❗️Получатель <b>-Константин Александрович К</b>.\n'
                                  f'💰 Сумма: <b>{golda}</b>₽\n'
                                  f'🍯 <ins>Игровая комиссия рынка на нас</ins>.\n'
                                  f'♻️Вам на аккаунт придет ровно: <b>{round(golda / 0.66, 2)}</b>G\n\n'
                                  f'📸 После оплаты, <b>нажмите</b> «✅ Я перевел»',parse_mode='HTML', reply_markup=kb.Verify)


@router.callback_query(F.data == 'Verify')
async def verify(callback: CallbackQuery, state: FSMContext):
    await state.update_data(id = callback.from_user.username)
    await callback.answer('Действуйте по инструкции')
    await callback.message.edit_text('📸Скиньте сюда в чат <b>скриншот перевода</b>', parse_mode='HTML')
    await callback.message.answer('⁉️ <b>Важно</b>: не обрезайте скриншот, на нем должно быть видно <b>дату</b>, <b>время</b> и <b>получателя</b>.', parse_mode='HTML')
    await state.set_state(standgold.verify)



@router.message(standgold.verify, F.photo)
async def screen(message:Message, state:FSMContext):
    await state.update_data(verify=message.photo[-1].file_id)
    await message.answer('✅<b>Ваш заказ принят!</b>', parse_mode='HTML')
    await message.answer('💵Средства поступят к вам на баланс после проверки')
    await state.set_state(None)
    data = await state.get_data()
    golda = int(data['gold'])
    id = data['id']
    await bot.send_photo(chat_id=os.getenv('ADMIN_VORTEX'), photo=data['verify'], caption=f'id:{id}\n💵Пополнение баланса💵 \n💵<b>{golda}</b> RUB\n🍯<b>{round(golda / 0.66, 2)}</b> Gold\n💵Bank: <b>{data['bank']}</b>',parse_mode='HTML', reply_markup=kb.ok)

@router.callback_query(F.data == 'Ok')
async def Ok(callback: CallbackQuery, state: FSMContext):
    await callback.answer('✅Заказ принят!')
    await bot.send_message(chat_id=id, text=f'Ваш скриншот проверен и принят, вам на баланс начислено {golda} Рублей')
    await callback.message.delete()

@router.callback_query(F.data == 'Cancel')
async def Cancel(callback: CallbackQuery):
    await callback.answer('🚫Заказ отклонён')
    await callback.message.delete()

@router.callback_query(F.data == 'Problem')
async def problem(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Действуйте по инструкции')
    await callback.message.edit_text(f'⁉️ Если у вас не получается перевести,' 
                                  f'попробуйте выбрать другой <b>способ оплаты</b>,\n'
                                  f'💡например «⚪️СБП | Другой банк».\n\n'
                                  f'Если проблема сохранилась, <b>напишите нам</b> ⤵️',parse_mode='HTML', reply_markup=kb.Faq)

@router.message()
async def send_echo(message: Message):
    await message.answer(f'🤖я не понимаю вас, если появились проблемы с работой бота нажмите\n /start')

