import os
import asyncio
from dotenv import load_dotenv
from aiogram import F, Router
from aiogram.filters import CommandStart, or_f
from aiogram.types import Message, CallbackQuery
from app.database.models import User
import app.keyboards as kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import app.database.requests as rq
from app.database.requests import Profile, Profiles, adm_list, check_adm, check_lvl, delete_admin, delete_all_order, delete_all_order_gold, delete_order_gold, orm_add_admin, orm_get_order_gold, orm_get_orders, orm_get_order, delete_order, orm_get_orders_gold, orm_get_orders_gold_error, orm_get_orders_gold_id, orm_get_orders_id, orm_order, orm_order_gold, orm_update_balance, orm_update_balance_gold, user_balance
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Bot
from aiogram.types import InputMediaPhoto
from aiogram.utils.media_group import MediaGroupBuilder


router = Router()

class what(StatesGroup):
    whats = State()

class admin_set(StatesGroup):
    adm_set = State()
    add = State()
    delete = State()


class dialog(StatesGroup):
    order_rub = State()
    count = State()
    skin = State()
    sms = State()
    text = State()
    photo = State()
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

class order_golds(StatesGroup):
    translate = State()
    nick = State()
    screenshot_profile = State()
    screenshot_skin = State()
    order_verify = None

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, session: AsyncSession):
    await state.set_state(None)
    await rq.orm_add_user(session, message.from_user.id, 0, 0)
    await message.answer(f'🏠Главное меню.\n'
                        f'👋Здравствуйте <b>{message.from_user.first_name}</b>\n\n'
                        f'📱Используй кнопки для \n-взаимодействия.\n\n'
                        f'⚡️ Для покупки Gолды\n-нажмите «💵 <b>Купить</b>».\n\n'
                        f'📖 Если у тебя возникли вопросы, обращайся в <b>поддержку</b>.',parse_mode='HTML', reply_markup=kb.main)
    if message.from_user.id == (int(os.getenv('ADMIN'))):
        await message.answer('Вы авторизовались как админ', reply_markup=kb.main_admin)
    elif await check_adm(session, message.from_user.id) != None:
        await message.answer('Вы авторизовались как админ', reply_markup=kb.main_admin)


@router.message(F.text == '👑Админка')
async def admin(message: Message, state: FSMContext, session: AsyncSession):
    if message.from_user.id == (int(os.getenv('ADMIN'))):
        await message.answer('*Выберите пункт интересующий вас*', parse_mode='Markdown', reply_markup=kb.Admin)
    elif await check_adm(session, message.from_user.id) != None:
        await message.answer('*Выберите пункт интересующий вас*', parse_mode='Markdown', reply_markup=kb.Admin)
        await state.clear()
    else: 
        await message.answer('🤖я не понимаю вас, если появились проблемы с работой бота нажмите\n /start')

@router.message(F.text == '🏠Главное меню')
async def main_menu(message: Message, state: FSMContext, session: AsyncSession):
    await state.set_state(None)
    await message.answer(f'🏠Главное меню.\n'
                        f'👋Здравствуйте <b>{message.from_user.first_name}</b>\n\n'
                        f'📱Используй кнопки для \n-взаимодействия.\n\n'
                        f'⚡️ Для покупки Gолды\n-нажмите «💵 <b>Купить</b>».\n\n'
                        f'📖 Если у тебя возникли вопросы, обращайся в <b>поддержку</b>.',parse_mode='HTML', reply_markup=kb.main)
    if message.from_user.id == (int(os.getenv('ADMIN'))):
        await message.answer('Вы авторизовались как админ', reply_markup=kb.main_admin)
    elif await check_adm(session, message.from_user.id) != None:
        await message.answer('Вы авторизовались как админ', reply_markup=kb.main_admin)

@router.message(F.text == '💵Купить')
async def buy(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    try:
        tg_id = message.from_user.id
        profile = await Profile(session=session, tg_id=tg_id)
        if profile != None:
            for order in await orm_get_orders(session):
                error = len(await orm_get_orders_id(session, order.tg_id)) 
                if error > 7:
                    await delete_all_order(session, order.tg_id)
                    await message.answer('❗️*Заказы отменены за багоюз*', parse_mode='Markdown')
                    break
                elif error >= 5 and error <= 7:
                    await message.answer('❗️*Приостановили возможность пополнения\n💡Причина: Багоюз*', parse_mode='Markdown')
                    await state.clear()
                    break
            else:
                await state.set_state(standgold.gold)
                await message.answer(f'🍯Введи в чат <b>сумму в Рублях</b>\nна которую хочешь пополнить баланс. \n 💡 <b>Например</b>: <b>💵100</b> = <b>🍯151.52G</b>',parse_mode='HTML', reply_markup=kb.menu)
        else:
            await message.answer('*Для начала авторизуйтесь \n/start*', parse_mode="Markdown")
    except Exception:
        await message.answer('*Произошла ошибка, повторите попытку позже\n/start*', parse_mode='Markdown')

@router.message(F.text == '⚡️Вывести')
async def ordered(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    await state.clear()
    tg_id = message.from_user.id
    profile = await Profile(session=session, tg_id=int(tg_id))
    if profile != None:
        for order in await orm_get_orders_gold(session):
            error = len(await orm_get_orders_gold_id(session, order.tg_id)) 
            if error == 1:
                await message.answer('❗️*У вас уже есть заявка на вывод*', parse_mode='Markdown')
                break
            elif error >= 2 and error <= 3:
                await message.answer('❗️*Вывод приостановлен\n💡Причина: Багоюз*', parse_mode='Markdown')
                break
            elif error > 3:
                await delete_all_order_gold(session, order.tg_id)
                await message.answer('❗️*Заказы отменены за багоюз*', parse_mode='Markdown')
                break
                
        else:
            await state.set_state(order_golds.translate)
            await message.answer(f'🍯Введи в чат *сумму Gold*\nкоторую хочешь вывести. \n 💡 *Например*: 🍯`100`',parse_mode='Markdown', reply_markup=kb.menu)
    else:
        await message.answer('*Для начала авторизуйтесь\n/start*', parse_mode='Markdown')

@router.message(order_golds.translate, F.text)
async def translate(message: Message, state: FSMContext, session: AsyncSession):
    tg_id = message.from_user.id
    balance = await user_balance(session=session, tg_id=tg_id)
    gold_balance = round(int(balance) / 0.66, 2)
    try:
        golda = round(float(message.text), 2)
        if golda < 100 and golda > 0:
            await message.answer('*Минимальная сумма вывода*: \n🍯`100` *GOLD*', parse_mode='Markdown')
        elif golda <= gold_balance and golda > 0:
            await state.update_data(translate=golda)
            await message.answer(f'❗*Отлично далее*'
                                 f'\n👾*напиши свой ник*'
                                 f'\n*👻оружие(с паттерном)*'
                                 f'\n🚀*паттерн*'
                                 f'\n❗*ВАЖНО*: *Укажите Nick Gun pattern*',parse_mode='Markdown') 
            await state.set_state(order_golds.nick)
        elif golda < 0:
            await message.answer('♻️*Введите корректное число*\n💡*Например*: 🍯`100`', parse_mode='Markdown')
        else:
            await message.answer(f'❗*Недостаточно средств на балансе*\n*🍯Ваш баланс*: `{gold_balance}` *GOLD*', parse_mode='Markdown')
    except Exception:
        await message.answer('🤖*я не понимаю вас, если появились проблемы с работой бота нажмите \n/start*', parse_mode='Markdown')
    
@router.message(order_golds.nick, F.text)
async def nick(message: Message, state: FSMContext):
    await state.update_data(nick = message.text)
    await message.answer(f'❗*Отправьте сюда в чат скриншот вашего профиля* `StandOff2`', parse_mode='Markdown', reply_markup=kb.menu)
    await state.set_state(order_golds.screenshot_profile)

@router.message(order_golds.screenshot_profile, F.photo)
async def screen_prof(message: Message, state: FSMContext):
    await state.update_data(screenshot_profile=message.photo[-1].file_id)
    data = await state.get_data()
    await message.answer(f'*🥳Отлично, далее выставляйте скин: \n🎲указанный ранее(с паттерном)*\n'
                        f'🍯*за* `{round(float(data['translate']) * 1.25, 2)}`*G*\n'
                        f'❗*Отправьте сюда в чат скриншот выставленного на продажу оружия* `StandOff2`\n'
                        f'💡*Инструкция*: *Рынок* -> *Мои запросы* -> *Запросы на продажу*',
                        parse_mode='Markdown', reply_markup=kb.menu)
    await state.set_state(order_golds.screenshot_skin)

@router.message(order_golds.screenshot_skin, F.photo)
async def translate(message: Message, state: FSMContext, bot: Bot, session: AsyncSession):
    await state.update_data(screenshot_skin=message.photo[-1].file_id)
    if message.from_user.username != None:
        await state.update_data(tg_name=message.from_user.username)
    else:
        await state.update_data(tg_name = 'Noname')
    await state.update_data(tg_id = message.from_user.id)
    try:
        data = await state.get_data()
        await orm_order_gold(session, data)
        await bot.send_message(chat_id=os.getenv('ADMIN'), text=f'🍯*Заказ на вывод*', parse_mode='Markdown')
        await message.answer(f'✅*Ваша заявка на вывод отправлена на рассмотрение*', parse_mode='Markdown', reply_markup=kb.menu)
        await message.answer('🍯*GOLD поступит к вам на баланс после проверки*(*до* `48`*Ч*)', parse_mode='Markdown')
    except Exception:
        await message.answer('Произошла ошибка. попробуйте снова или напишите в поддержку')
        await state.set_state(None)
    await state.clear()


@router.message(F.text == '🆔Профиль')
async def buy(message: Message, session: AsyncSession):
    tg_id = message.from_user.id
    try:
        balance = await user_balance(session=session, tg_id=tg_id)
        gold = round(balance / 0.66, 2)
        profile = await Profile(session=session, tg_id=tg_id)
        await message.answer(f'🆔: *{profile}*\n🍯*Баланс*: *{gold}* G\n\n🔥Ваш ранг: *Новичек*', parse_mode='Markdown')
    except Exception:
        await message.answer('*Для начала авторизуйтесь \n/start*', parse_mode='Markdown')

@router.message(F.text == '🎮Игры')
async def game(message: Message):
    await message.answer('*Этот пункт в разработке*', parse_mode='Markdown')

@router.message(F.text == '📖О нас')
async def faq(message:Message):
    await message.answer('📖О нас:', reply_markup=kb.fq)

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
        await message.answer('🤖*я не понимаю вас, если появились проблемы с работой бота нажмите \n/start*', parse_mode='Markdown')
    
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
        await bot.send_message(chat_id=os.getenv('ADMIN'), text=f'💵*Заказ на пополнение баланса*', parse_mode='Markdown')
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
async def Order(callback: CallbackQuery):
    await callback.answer('✅Заказы!')
    await callback.message.edit_text('✅*Выберити тип заказов*', parse_mode='Markdown', reply_markup=kb.type_order)
    
        
@router.callback_query(F.data == 'Rub')
async def Rub_ord(callback: CallbackQuery, session: AsyncSession, bot: Bot):
    if callback.from_user.id == int(os.getenv('ADMIN')) or await check_lvl(session, callback.from_user.id) >= 1:
        await callback.answer('✅Заказы на пополнение')
        orders = len(await orm_get_orders(session))
        try:
            if int(orders) != 0 and int(orders) > 0:
                await callback.message.edit_text(f"Количество заказов *{orders}* ⁉️", parse_mode='Markdown', reply_markup=kb.type_order)
                for order in await orm_get_orders(session):
                    error = len(await orm_get_orders_id(session, order.tg_id))
                    for order_er in await orm_get_orders_id(session, order.tg_id): 
                        if error > 7:
                            await delete_all_order(session, order_er.tg_id)
                            await bot.send_message(chat_id=order_er.tg_id, text='❗️*Заказы отменены за багоюз*', parse_mode='Markdown')
                            await callback.answer('Заказы отменены')
                            await callback.message.answer('❗️*Заказы отменены за багоюз*', parse_mode='Markdown')
                            break
                        else:
                            await callback.message.answer_photo(
                                order_er.image,
                                caption=f'💵*Пополнение баланса*💵\n\n'
                                f'🆔*id*:`@{order_er.tg_name}`\n'
                                f'💲*bank*:{order_er.bank}\n'
                                f'💵{order_er.price_rub}RUB\n'
                                f'🍯{round(order_er.price_gold, 2)}\n',
                                parse_mode='Markdown',
                                reply_markup=kb.get_callback_btns(
                                    btns={
                                        "Принять": f"ok_{order_er.id}",
                                        "Отклонить": f"delete_{order_er.id}",
                                    }
                                ),
                            ) 
                    break
            else:
                await callback.message.delete()
                await callback.message.answer(f'*Заказов нет*', parse_mode='Markdown', reply_markup=kb.main_admin)
        except Exception:
            await callback.message.delete()
            await callback.message.answer(f'*Количество заказов {orders}* ⁉️', parse_mode='Markdown', reply_markup=kb.type_order)
    else:
        await callback.message.delete()
        await callback.answer('Не доступно')
        await callback.message.answer('❗️*Доступно только админам с lvl: 1*', parse_mode='Markdown')
        

@router.callback_query(F.data.startswith('ok_'))
async def Ok(callback: CallbackQuery, bot: Bot, session: AsyncSession):
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
   
@router.callback_query(F.data == 'Gold')
async def Rub_ord(callback: CallbackQuery, session: AsyncSession, bot: Bot):
    if callback.from_user.id == int(os.getenv('ADMIN')) or await check_lvl(session, callback.from_user.id) >= 2:
        await callback.answer('🍯Заказы на Вывод')
        orders = len(await orm_get_orders_gold(session))
        try:
            if int(orders) != 0 and int(orders) > 0:
                await callback.message.edit_text(f"Количество заказов *{orders}* ⁉️", parse_mode='Markdown', reply_markup=kb.type_order)
                for order in await orm_get_orders_gold(session):
                    error = len(await orm_get_orders_gold_id(session, order.tg_id))
                    for order_er in await orm_get_orders_gold_id(session, order.tg_id):
                        if error > 1:
                            await delete_all_order_gold(session, order_er.tg_id)
                            await bot.send_message(chat_id=order_er.tg_id, text='❗️*Заявки на вывод отменены за багоюз*', parse_mode='Markdown')
                            await callback.answer('Заказы отменены')
                            await callback.message.answer('❗️*Заявки отменены за багоюз*', parse_mode='Markdown')
                            break
                        else:
                            await callback.message.answer_photo(order_er.screen_prof)
                            await callback.message.answer_photo(
                                order_er.screen_skin,
                                caption=f'🍯*Вывод Gold*\n\n'
                                f'*id*:`@{order_er.tg_name}`\n'
                               f'*nick*:{order_er.nick}\n'
                                f'🍯{round(float(order_er.price_gold) * 1.25, 2)}G\n',
                                parse_mode='Markdown',
                                reply_markup=kb.get_callback_btns(
                                    btns={
                                        "Принять": f"YesGold_{order_er.id}",
                                       "Отклонить": f"NoGold_{order_er.id}"
                                    }
                                ),
                            ) 
                    break
            else:
                await callback.message.delete()
                await callback.message.answer(f'❗️*Заказов нет*', parse_mode='Markdown', reply_markup=kb.main_admin)
        except Exception:
            await callback.message.delete()
            await callback.message.answer(f'❗️*Количество заказов {orders}* ⁉️', parse_mode='Markdown', reply_markup=kb.type_order)
    else:
        await callback.message.delete()
        await callback.answer('Не доступно')
        await callback.message.answer('❗️*Доступно только админам с lvl: 2*', parse_mode='Markdown')
        
@router.callback_query(F.data.startswith('YesGold_'))
async def Okgold(callback: CallbackQuery, bot: Bot, session: AsyncSession):
    order_id = callback.data.split("_")[-1]
    order_verify = await orm_get_order_gold(session, int(order_id))
    order_golds.order_verify=order_verify.price_gold
    await orm_update_balance_gold(session=session, user_tg_id=int(order_verify.tg_id), balance_gold=order_verify.price_gold, balance=(float(order_verify.price_gold)*0.66))
    await bot.send_message(chat_id=order_verify.tg_id, text=f'✅*Ваша заявка на вывод проверена и принята*. \n\n*С баланса снято*:🍯`{round(order_verify.price_gold, 2)}` *GOLD*', parse_mode='Markdown')
    await callback.answer("Заказ принят!", show_alert=True)
    await delete_order_gold(session, int(order_id))
    await callback.message.delete()

@router.callback_query(F.data.startswith("NoGold_"))
async def Nogold(callback: CallbackQuery, state: FSMContext, bot: Bot, session: AsyncSession):
    order_id = callback.data.split("_")[-1]
    order_verify = await orm_get_order_gold(session, int(order_id))
    order_golds.order_verify=order_verify
    await bot.send_message(chat_id=order_verify.tg_id, text=f'⁉️*Ваша заявка на вывод:* `{round(order_verify.price_gold, 2)}` *GOLD отклонена*\n\n*❗Если не согласны с решением напишите в поддержку*', parse_mode='Markdown')
    await delete_order_gold(session, int(order_id))
    await callback.answer("Заказ отменён!", show_alert=True)
    await callback.message.delete()


@router.callback_query(F.data == 'sms')
async def sms(callback:CallbackQuery, state: FSMContext, session: AsyncSession):
    if callback.from_user.id == int(os.getenv('ADMIN')) or await check_lvl(session, callback.from_user.id) == 3:
        await callback.answer('Отправьте фото или текст')
        await callback.message.edit_text('*Отправьте* `фото` *или* `текст` *если хотите рассылку без* `фото`', parse_mode='Markdown')
        await state.set_state(dialog.sms)
    else:
        await callback.answer('Нет доступа')
        await callback.message.edit_text('❗️*Доступно только главному админу*', parse_mode='Markdown')

@router.message(dialog.sms, F.photo)
async def spam(message: Message, state:FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await message.answer('*Теперь напишите* `текст` *рассылки*', parse_mode='Markdown')
    await state.set_state(dialog.text)

@router.message(dialog.sms, F.text)
async def spam(message: Message, session: AsyncSession, bot: Bot):
    text = message.text
    try:
        tgid = await Profiles(session=session)
        for i in tgid:
            await bot.send_message(chat_id=i, text=text)
    except Exception:
        pass
    await message.answer('*SMS доставлено всем*', parse_mode='Markdown')

@router.message(dialog.text, F.text)
async def spam_sms(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    text = message.text
    data = await state.get_data()
    try:
        tgid = await Profiles(session=session)
        for i in tgid:
            await bot.send_photo(chat_id=i, photo=data['photo'], caption=text)
    except Exception:
        pass
    await message.answer('*SMS доставлено всем*', parse_mode='Markdown')

@router.callback_query(F.data == 'admins')
async def admins(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    if callback.from_user.id == int(os.getenv('ADMIN')) or await check_lvl(session, callback.from_user.id) == 3:
        await callback.answer('Выберите')
        await callback.message.edit_text('*Выберите действие*',reply_markup=kb.add_del_adm ,parse_mode='Markdown')
        await state.set_state(admin_set.adm_set)
    else:
        await callback.answer('Не доступно')
        await callback.message.edit_text('❗️*Не доступно*', parse_mode='Markdown')

@router.callback_query(admin_set.adm_set, F.data == 'adm_add')
async def admins(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Введите id lvl кого хотите сделать админом')
    await callback.message.edit_text('*Введите* `ID LVL NAME` *нового админа*', parse_mode='Markdown')
    await state.set_state(admin_set.add)

@router.message(admin_set.add, F.text)
async def add_adm(message: Message, state: FSMContext, session: AsyncSession):
    try:
        adm = message.text.split(' ')
        await orm_add_admin(session, int(adm[0]),int(adm[1]), str(adm[2]))
        await message.answer('✅*Админ добавлен*', parse_mode='Markdown')
        await state.clear()
    except:
        await message.answer('*Введите ID LVL NAME*', parse_mode='Markdown')


@router.message(admin_set.add, F.text)
async def add_adm(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(add = int(message.text))
    await orm_add_admin(session, int(message.text)) 
    await message.answer('✅*Админ добавлен*', parse_mode='Markdown')
    await state.clear()


@router.callback_query(admin_set.adm_set, F.data == 'adm_del')
async def admins(callback: CallbackQuery, state: FSMContext):
        await callback.answer('Введите id кого хотите убрать с админки')
        await callback.message.edit_text('Введите ID админа которого убрать')
        await state.set_state(admin_set.delete)
        
@router.message(admin_set.delete, F.text)
async def add_adm(message: Message, state: FSMContext, session: AsyncSession):
    try:
        if await check_adm(session, int(message.text)) != None:
            if int(message.text) != 918212173:
                await delete_admin(session=session, tg_id=int(message.text))
                await message.answer('❗️*Админ удалён*', parse_mode='Markdown')
            else:
                await message.answer('❗️Это главный админ')
        else:
            await message.answer('❗️*Админ не найден*', parse_mode='Markdown')
    except:
        await message.answer('❗️*Произошла ошибка*',parse_mode='Markdown')


@router.callback_query(admin_set.adm_set, F.data == 'adm_list')
async def admins_list(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
        await callback.message.delete()
        await callback.answer('Список админов')
        ids_adm = len(await adm_list(session))
        for admins in await adm_list(session):
            await callback.message.answer(f'*Админ*: `{admins.id}`\n'
                                        f'*ID*: `{admins.tg_id}`\n'
                                        f'*LVL*: `{admins.lvl}`\n'
                                        f'*NAME*: `{admins.name}`\n', parse_mode='Markdown')
        await callback.message.answer(f'*Всего админов*: `{ids_adm}`', parse_mode='Markdown')


@router.message()
async def send_echo(message: Message):
    await message.answer(f'🤖*я не понимаю вас, если появились проблемы с работой бота нажмите\n /start*', parse_mode='Markdown')

