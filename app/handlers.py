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
import aiogram.utils.markdown as md


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
    await state.set_state(None)
    await rq.set_user(message.from_user.id)
    await message.answer(f'🏠Главное меню.\n'
                        f'👋Здравствуйте <b>{message.from_user.first_name}</b>\n\n'
                        f'📱Используй кнопки для \n-взаимодействия.\n\n'
                        f'⚡️ Для покупки Gолды\n-нажмите «💵 <b>Купить</b>».\n\n'
                        f'📖 Если у тебя возникли вопросы, обращайся в <b>поддержку</b>.',parse_mode='HTML', reply_markup=kb.main)
    
    if message.from_user.id == int(os.getenv('ADMIN_VORTEX')):
        await message.answer('Вы авторизовались как админ', reply_markup=kb.main_admin)

@router.message(F.text == '👑Админка')
async def admin(message: Message, state: FSMContext, bot: Bot):
    if message.from_user.id == int(os.getenv('ADMIN_VORTEX')):
        await message.answer('Нажмите кнопку', reply_markup=kb.Admin)
    else:
        await message.answer('🤖я не понимаю вас, если появились проблемы с работой бота нажмите\n /start')
    

@router.message(F.text == '🏠Главное меню')
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(None)
    await message.answer(f'🏠Главное меню.\n'
                        f'👋Здравствуйте <b>{message.from_user.first_name}</b>\n\n'
                        f'📱Используй кнопки для \n-взаимодействия.\n\n'
                        f'⚡️ Для покупки Gолды\n-нажмите «💵 <b>Купить</b>».\n\n'
                        f'📖 Если у тебя возникли вопросы, обращайся в <b>поддержку</b>.',parse_mode='HTML', reply_markup=kb.main)

@router.message(F.text == '💵Купить')
async def buy(message: Message, state: FSMContext):
    await state.set_state(standgold.gold)
    await message.answer(f'🍯Введи в чат <b>сумму в Рублях</b>\nна которую хочешь пополнить баланс. \n 💡 <b>Например</b>: <b>100₽</b> = <b>151.52G</b>',parse_mode='HTML', reply_markup=kb.menu)
    
    
@router.message(standgold.gold)
async def sum(message: Message, state: FSMContext):    
    try:
        golds = int(message.text)
        rub = int(golds)
        if rub >= 100:
            golda = round(golds / 0.66, 2)
            await state.update_data(gold=message.text)
            await message.answer(f'📝 За <b>{rub}</b>₽ ты получаешь <b>{golda}G</b>. \n<b>Выбери удобный способ оплаты</b>:',parse_mode='HTML', reply_markup=kb.bank) 
            await state.set_state(standgold.bank)
        else:
            await message.answer(f'♻️Введите корректное число, минимум <b>100</b>₽', parse_mode='HTML')
    except Exception:
        await message.answer('🤖я не понимаю вас, если появились проблемы с работой бота нажмите \n<b>/start</b>', parse_mode='HTML')
    
@router.callback_query(F.data == 'Back')
async def Back(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    golda = int(data['gold'])
    await callback.message.edit_text(f'📝 За <b>{golda}</b>₽ ты получаешь <b>{round(golda / 0.66, 2)}G</b>. \n<b>Выбери удобный способ оплаты</b>:', parse_mode='HTML', reply_markup=kb.bank)
    await callback.answer('Вы вернулись назад')
    

@router.callback_query(F.data == 'Edit')
async def Back(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Выберите способ оплаты')
    data = await state.get_data()
    golda = int(data['gold'])
    await callback.message.edit_text(f'📝 За <b>{golda}</b>₽ ты получаешь <b>{round(golda / 0.66, 2)}G</b>. \n<b>Выбери удобный способ оплаты</b>:',parse_mode='HTML', reply_markup=kb.bank)


@router.callback_query(F.data == 'SBP')
async def SBP(callback: CallbackQuery, state:FSMContext):
    await callback.answer('Действуйте по инструкции')
    await state.update_data(bank='⚪️СБП⚪️')
    data = await state.get_data()
    golda = int(data['gold'])
    await callback.message.edit_text(f'📱*Номер СБП*⚪️: *+79087976609*\n'
                                  f'💳*Банк*: *Тинькофф*(Т.Банк)\n'
                                  f'❗️*Получатель*: -Константин.К.\n'
                                  f'💰 *Сумма*: `{golda}`₽\n'
                                  f'🍯 *Игровая комиссия рынка на нас*.\n'
                                  f'♻️*Вам придет ровно*: *{round(golda / 0.66, 2)}G*\n\n'
                                  f'📸 После оплаты, *нажмите* \n«✅ *Я перевел*»',parse_mode='Markdown', reply_markup=kb.Verify)

    

@router.callback_query(F.data == 'Sberbank')
async def Sberbank(callback: CallbackQuery, state:FSMContext):
    await callback.answer('Действуйте по инструкции')
    await state.update_data(bank='🟢SBERBANK🟢')
    data = await state.get_data()
    golda = int(data['gold'])
    await callback.message.edit_text(f'💳*Карта*🟢: *2202202013277409*\n'
                                  f'❗️*Получатель*: -Константин.К.\n'
                                  f'💰 *Сумма*: `{golda}`₽\n'
                                  f'🍯 *Игровая комиссия рынка на нас*.\n'
                                  f'♻️*Вам придет ровно*: *{round(golda / 0.66, 2)}G*\n\n'
                                  f'📸 После оплаты, *нажмите* \n«✅ *Я перевел*»',parse_mode='Markdown', reply_markup=kb.Verify)


@router.callback_query(F.data == 'Tinkoff')
async def Tinkoff(callback: CallbackQuery, state:FSMContext):
    await callback.answer('Действуйте по инструкции')
    await state.update_data(bank='🟡Tinkoff🟡')
    data = await state.get_data()
    golda = int(data['gold'])
    await callback.message.edit_text(f'💳*Карта*🟡: *2200700817593386*\n'
                                  f'❗️*Получатель*: -Константин.К.\n'
                                  f'💰 *Сумма*: `{golda}`₽\n'
                                  f'🍯 *Игровая комиссия рынка на нас*.\n'
                                  f'♻️*Вам придет ровно*: *{round(golda / 0.66, 2)}G*\n\n'
                                  f'📸 После оплаты, *нажмите* \n«✅ *Я перевел*»',parse_mode='Markdown', reply_markup=kb.Verify)


@router.callback_query(F.data == 'Alfa')
async def Alfa(callback: CallbackQuery, state:FSMContext):
    await callback.answer('Действуйте по инструкции')
    await state.update_data(bank='🔴ALFA🔴')
    data = await state.get_data()
    golda = int(data['gold'])
    await callback.message.edit_text(f'💳*Карта*🔴: *2200150818007889*\n'
                                  f'❗️*Получатель*: -Константин.К.\n'
                                  f'💰 *Сумма*: `{golda}`₽\n'
                                  f'🍯 *Игровая комиссия рынка на нас*.\n'
                                  f'♻️*Вам придет ровно*: *{round(golda / 0.66, 2)}G*\n\n'
                                  f'📸 После оплаты, *нажмите* \n«✅ *Я перевел*»',parse_mode='Markdown', reply_markup=kb.Verify)


@router.callback_query(F.data == 'Vtb')
async def Vtb(callback: CallbackQuery, state:FSMContext):
    await callback.answer('Действуйте по инструкции')
    await state.update_data(bank='🔵ВТБ🔵')
    data = await state.get_data()
    golda = int(data['gold'])
    await callback.message.edit_text(f'💳*Карта*🔵: *2200246001639031*\n'
                                  f'❗️*Получатель*: -Константин.К.\n'
                                  f'💰 *Сумма*: `{golda}`₽\n'
                                  f'🍯 *Игровая комиссия рынка на нас*.\n'
                                  f'♻️*Вам придет ровно*: *{round(golda / 0.66, 2)}G*\n\n'
                                  f'📸 После оплаты, *нажмите* \n«✅ *Я перевел*»',parse_mode='Markdown', reply_markup=kb.Verify)


@router.callback_query(F.data == 'Verify')
async def verify(callback: CallbackQuery, state: FSMContext):
    await state.update_data(id = callback.from_user.username)
    await callback.answer('Действуйте по инструкции')
    await callback.message.edit_text('📸Скиньте сюда в чат <b>скриншот перевода</b>', parse_mode='HTML')
    await callback.message.answer('⁉️ <b>Важно</b>: не обрезайте скриншот, на нем должно быть видно <b>дату</b>, <b>время</b> и <b>получателя</b>.', parse_mode='HTML')
    await state.set_state(standgold.verify)



@router.message(standgold.verify, F.photo)
async def screen(message:Message, state:FSMContext, bot: Bot):
    await state.update_data(verify=message.photo[-1].file_id)
    await message.answer('✅<b>Ваш заказ принят!</b>', parse_mode='HTML')
    await message.answer('💵Средства поступят к вам на баланс после проверки')
    await state.set_state(None)
    data = await state.get_data()
    golda = int(data['gold'])
    id = data['id']
    await bot.send_photo(chat_id=os.getenv('ADMIN_VORTEX'), photo=data['verify'], caption=f'*id*:`@{id}`\n💵*Пополнение баланса*💵 \n💵*{golda}RUB*\n🍯*{round(golda / 0.66, 2)}G*\n💵*Bank*: *{data['bank']}*',parse_mode='Markdown', reply_markup=kb.ok)
    await state.clear()

@router.callback_query(F.data == 'Ok')
async def Ok(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer('✅Заказ принят!')
    await bot.send_message(chat_id=id, text=f'Ваш скриншот проверен и принят, вам на баланс начислено Рублей')
    await callback.message.delete()

@router.callback_query(F.data == 'Cancel')
async def Cancel(callback: CallbackQuery, bot: Bot):
    await callback.answer('🚫Заказ отклонён')
    await callback.message.delete()

@router.callback_query(F.data == 'Problem')
async def problem(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Действуйте по инструкции')
    await callback.message.edit_text(f'⁉️Если у вас не получается перевести\n' 
                                  f'✨Выберите другой <b>способ оплаты</b>,\n'
                                  f'💡<b>Например</b> «⚪️СБП | Другой банк».\n\n'
                                  f'🫣Если проблема сохранилась, <b>напишите нам в поддержку</b> ⤵️',parse_mode='HTML', reply_markup=kb.Faq)

@router.message()
async def send_echo(message: Message):
    await message.answer(f'🤖я не понимаю вас, если появились проблемы с работой бота нажмите\n /start')

