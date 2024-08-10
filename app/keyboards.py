from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardRemove


def get_callback_btns(
    *,
    btns: dict[str, str],
    sizes: tuple[int] = (2,)):

    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():
        
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()


def get_url_btns(
    *,
    btns: dict[str, str],
    sizes: tuple[int] = (2,)):

    keyboard = InlineKeyboardBuilder()

    for text, url in btns.items():
        
        keyboard.add(InlineKeyboardButton(text=text, url=url))

    return keyboard.adjust(*sizes).as_markup()


#Создать микс из CallBack и URL кнопок
def get_inlineMix_btns(
    *,
    btns: dict[str, str],
    sizes: tuple[int] = (2,)):

    keyboard = InlineKeyboardBuilder()

    for text, value in btns.items():
        if '://' in value:
            keyboard.add(InlineKeyboardButton(text=text, url=value))
        else:
            keyboard.add(InlineKeyboardButton(text=text, callback_data=value))

    return keyboard.adjust(*sizes).as_markup()

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='💵Купить'), KeyboardButton(text='⚡️Вывести')],
    [KeyboardButton(text='🍯Продать')],
    [KeyboardButton(text='🎮Игры'), KeyboardButton(text='🆔Профиль')],
    [KeyboardButton(text='📖Информация')], 
], 
resize_keyboard=True, input_field_placeholder='Привет, нажми кнопку интересующую тебя'
)

pay = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Перевод', callback_data='translate')]
])

bank = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сбербанк🟢', callback_data='Sberbank'), InlineKeyboardButton(text='Тинькофф🟡', callback_data='Tinkoff')],
    [InlineKeyboardButton(text='Альфа🔴', callback_data='Alfa'),InlineKeyboardButton(text='ВТБ🔵', callback_data='Vtb')],
    [InlineKeyboardButton(text='СБП⚪️', callback_data='SBP')]
])

url_adm = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='📝Поддержка', url='https://t.me/KooStyyYaa')]])

menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🏠Главное меню')]
], resize_keyboard=True)

Verify = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Я перевел', callback_data='Verify')], 
    [InlineKeyboardButton(text='🚫Проблема с оплатой', callback_data='Problem')],
    [InlineKeyboardButton(text='⬅️Изменить способ оплаты', callback_data='Edit')]
])

Faq = InlineKeyboardMarkup(inline_keyboard=[

    [InlineKeyboardButton(text='⬅️Назад', callback_data='Back'), InlineKeyboardButton(text='📝Поддержка', url='https://t.me/KooStyyYaa')]
])

main_admin= ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='💵Купить'), KeyboardButton(text='⚡️Вывести')],
    [KeyboardButton(text='🍯Продать')],
    [KeyboardButton(text='🎮Игры'), KeyboardButton(text='🆔Профиль')],
    [KeyboardButton(text='📖Информация')], 
    [KeyboardButton(text='👑Админка')]
], resize_keyboard=True)

Admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Рассылка', callback_data='sms')],
    [InlineKeyboardButton(text='Админы', callback_data='admins')],
    [InlineKeyboardButton(text='Заказы', callback_data='orders')],
    [InlineKeyboardButton(text='Баны', callback_data='bans')],
    [InlineKeyboardButton(text='Розыгрыш', callback_data='bonus')],
    [InlineKeyboardButton(text='Статистика', callback_data='static')],
    [InlineKeyboardButton(text='Курс', callback_data='course')]
])

Bans = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Забанить', callback_data='ban')],
    [InlineKeyboardButton(text='Разбанить', callback_data='unban')],
    [InlineKeyboardButton(text='Список', callback_data='banned')]])

type_order = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Пополнения', callback_data='Rub'), InlineKeyboardButton(text='Выводы', callback_data='Gold')]
])

fq = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📝Поддержка', url='https://t.me/KooStyyYaa')], 
    [InlineKeyboardButton(text='📖Отзывы', url='https://t.me/WhiteStoreReview')], 
    [InlineKeyboardButton(text='📰Новости', url='https://t.me/WhiteStoreGold')],
    [InlineKeyboardButton(text='📰Курс', callback_data='curse')],
])

remove = ReplyKeyboardRemove()

add_del_adm = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить', callback_data='adm_add')],
    [InlineKeyboardButton(text='Список', callback_data='adm_list')],
    [InlineKeyboardButton(text='Удалить', callback_data='adm_del')]
])