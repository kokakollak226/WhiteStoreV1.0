import os
from dotenv import load_dotenv
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from app.database.models import User
import app.keyboards as kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import app.database.requests as rq
from app.database.requests import Profile, Profiles, orm_get_orders, orm_get_order, delete_order, orm_order, orm_update_balance, user_balance
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Bot


router = Router()

class dialog(StatesGroup):
    sms = State()
    blacklist = State()
    whitelist = State()

class standgold(StatesGroup):
    tg_name = State()
    tg_id = State()
    rub = State()
    gold = State()
    bank = State()
    image = State()
    order_change = None


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, session: AsyncSession):
    await state.set_state(None)
    await rq.orm_add_user(session, message.from_user.id, 0)
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
        await state.clear()
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
    if message.from_user.id == int(os.getenv('ADMIN_VORTEX')):
        await message.answer('Вы авторизовались как админ', reply_markup=kb.main_admin)

@router.message(F.text == '💵Купить')
async def buy(message: Message, state: FSMContext):
    await state.set_state(standgold.gold)
    await message.answer(f'🍯Введи в чат <b>сумму в Рублях</b>\nна которую хочешь пополнить баланс. \n 💡 <b>Например</b>: <b>💵100₽</b> = <b>🍯151.52G</b>',parse_mode='HTML', reply_markup=kb.menu)
    
@router.message(F.text == '🆔Профиль')
async def buy(message: Message, state: FSMContext, session: AsyncSession):
    tg_id = message.from_user.id
    balance = await user_balance(session=session, tg_id=tg_id)
    profile = await Profile(session=session, tg_id=tg_id)
    await message.answer(f'🆔:*{profile}*\n🍯*Баланс*:*{round(balance / 0.66, 2)}*\n\n🔥Ваш ранг: *Новичек*', parse_mode='Markdown')

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
    await callback.answer('Действуйте по инструкции')
    await callback.message.edit_text('📸Скиньте сюда в чат <b>скриншот перевода</b>', parse_mode='HTML')
    await callback.message.answer('⁉️ <b>Важно</b>: не обрезайте скриншот, на нем должно быть видно <b>дату</b>, <b>время</b> и <b>получателя</b>.', parse_mode='HTML')
    await state.set_state(standgold.image)


@router.message(standgold.image, F.photo)
async def screen(message:Message, state:FSMContext, bot: Bot, session: AsyncSession):
    await state.update_data(image=message.photo[-1].file_id)
    if message.from_user.username != None:
        await state.update_data(tg_name=message.from_user.username)
    else:
        await state.update_data(tg_name = 'Noname')
    await state.update_data(tg_id = message.from_user.id)
    try:
        data = await state.get_data()
        await orm_order(session, data)
        await message.answer('✅<b>Ваш заказ принят!</b>', parse_mode='HTML')
        await message.answer('💵Средства поступят к вам на баланс после проверки(до 48Ч)')
        await bot.send_message(chat_id=os.getenv('ADMIN_VORTEX'), text=f'💵*Заказ на пополнение баланса*', parse_mode='Markdown')
    except Exception:
        await message.answer('Произошла ошибка. попробуйте снова или напишите в поддержку')
        await state.set_state(None)
    await state.clear()

@router.callback_query(F.data == 'Problem')
async def problem(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Действуйте по инструкции')
    await callback.message.edit_text(f'⁉️Если у вас не получается перевести\n' 
                                  f'✨Выберите другой <b>способ оплаты</b>,\n'
                                  f'💡<b>Например</b> «⚪️СБП | Другой банк».\n\n'
                                  f'🫣Если проблема сохранилась, <b>напишите нам в поддержку</b> ⤵️',parse_mode='HTML', reply_markup=kb.Faq)

@router.callback_query(F.data == 'orders')
async def Order(callback: CallbackQuery, session: AsyncSession):
    await callback.message.delete()
    await callback.answer('✅Заказы!')
    count = 0
    for order in await orm_get_orders(session):
        count += 1
        await callback.message.answer_photo(
            order.image,
            caption=f'💵Пополнение баланса💵\n\n'
            f'*id*:`@{order.tg_name}`\n'
            f'*bank*:{order.bank}\n'
            f'💵{order.price_rub}RUB\n'
            f'🍯{round(order.price_gold, 2)}\n',
            parse_mode='Markdown',
            reply_markup=kb.get_callback_btns(
                btns={
                    "Принять": f"ok_{order.id}",
                    "Отклонить": f"delete_{order.id}",
                }
            ),
        )
    await callback.message.answer(f"Количество заказов *{count}* ⁉️", parse_mode='Markdown')


@router.callback_query(F.data.startswith('ok_'))
async def Ok(callback: CallbackQuery, bot: Bot, state: FSMContext, session: AsyncSession):
    order_id = callback.data.split("_")[-1]
    order_change = await orm_get_order(session, int(order_id))
    standgold.order_change=order_change
    await orm_update_balance(session=session, user_tg_id=int(order_change.tg_id), balance=int(order_change.price_rub))
    await bot.send_message(chat_id=order_change.tg_id, text=f'✅*Ваш заказ проверен и принят*. \n\n*вам начислено*: \n💵`{order_change.price_rub}` *RUB* : 🍯*{round(order_change.price_gold, 2)} GOLD*', parse_mode='Markdown')
    await callback.answer("Заказ принят!", show_alert=True)
    await delete_order(session, int(order_id))
    await callback.message.delete()

@router.callback_query(F.data.startswith("delete_"))
async def delete_ord(callback: CallbackQuery, bot: Bot, session: AsyncSession):
    order_id = callback.data.split("_")[-1]
    order_change = await orm_get_order(session, int(order_id))
    standgold.order_change=order_change
    await bot.send_message(chat_id=order_change.tg_id, text=f'⁉️*Ваш заказ на сумму* `{order_change.price_rub}` *RUB отклонён*\n\n*❗Если не согласны с решением напишите в поддержку*', parse_mode='Markdown')
    await delete_order(session, int(order_id))
    await callback.answer("Заказ отменён!", show_alert=True)
    await callback.message.delete()
    
@router.callback_query(F.data == 'sms')
async def sms(callback:CallbackQuery, state: FSMContext):
    await callback.answer('Введите текст для рассылки')
    await callback.message.delete()
    await callback.message.answer('Введите текст для рассылки')
    await state.set_state(dialog.sms)

@router.message(dialog.sms, F.text)
async def spam(message: Message, state:FSMContext, session: AsyncSession, bot:Bot):
    text = message.text
    tgid = await Profiles(session=session)
    for i in tgid:
        await bot.send_message(chat_id=i, text=text)
    await message.answer('SMS доставлено всем')

@router.message()
async def send_echo(message: Message):
    await message.answer(f'🤖я не понимаю вас, если появились проблемы с работой бота нажмите\n /start')

