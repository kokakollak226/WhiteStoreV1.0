from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='💵Купить'), KeyboardButton(text='⚡️Вывести')],
    [KeyboardButton(text='🎮Игры'), KeyboardButton(text='📖Поддержка')],
    [KeyboardButton(text='📝Отзывы')]
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
    [KeyboardButton(text='🎮Игры'), KeyboardButton(text='📖Поддержка')],
    [KeyboardButton(text='📝Отзывы'), KeyboardButton(text='👑Админка')]
], resize_keyboard=True)

Admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Рассылка', callback_data='sms')],
    [InlineKeyboardButton(text='Добавить в ЧС', callback_data='ban'), InlineKeyboardButton(text='Убрать из чс', callback_data='unban')],
    [InlineKeyboardButton(text='Статистика', callback_data='static')]
])

ok = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅Принять', callback_data='Ok'), InlineKeyboardButton(text='🚫Отклонить', callback_data='Cancel')]
])
