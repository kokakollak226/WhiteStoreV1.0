from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Купить'), KeyboardButton(text='Продать')],
    [KeyboardButton(text='Игры')],
    [KeyboardButton(text='Курс'), KeyboardButton(text='Новости')],
    [KeyboardButton(text='Отзывы')]
], 
resize_keyboard=True, input_field_placeholder='Привет, нажми кнопку интересующую тебя'
)

pay = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Перевод', callback_data='translate')],
    [InlineKeyboardButton(text='Крипта', callback_data='Crypto')]
])

bank = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='СБП', callback_data='SBP')],
    [InlineKeyboardButton(text='Сбербанк', callback_data='Sberbank')],
    [InlineKeyboardButton(text='Тинькофф', callback_data='Tinkoff')],
    [InlineKeyboardButton(text='Альфа', callback_data='Alfa')],
    [InlineKeyboardButton(text='ВТБ', callback_data='Vtb')],
])
