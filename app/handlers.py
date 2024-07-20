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
    translate = State()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    state.clear
    await message.answer(f'Здравствуйте {message.from_user.first_name}', reply_markup=kb.main)
    
    
@router.message(F.text == 'Главное меню')
async def cmd_start(message: Message, state: FSMContext):
    state.clear
    await message.answer(f'Здравствуйте {message.from_user.first_name}', reply_markup=kb.main)
    


@router.message(F.text == 'Купить')
async def buy(message: Message, state: FSMContext):
    await state.set_state(standgold.gold)
    await message.answer(f'🍯 Чтобы купить голду, введи в чат сумму на которую хочешь пополнить баланс. \n 💡 Например: 100', reply_markup=kb.menu)
    

    
@router.message(standgold.gold)
async def sum(message: Message, state: FSMContext):    
    try:
        golds = int(message.text)
        rub = int(golds)
        golda = round(golds / 0.66, 2)
        await state.update_data(gold=message.text)
        await message.answer(f'📝 За {rub} ₽ ты получаешь {golda} голды. Для пополнения баланса выбери наиболее удобный тебе способ оплаты:', reply_markup=kb.pay) 
        await state.set_state(standgold.bank)
    except Exception:
        message.answer('Введите целое число')
    return golda, rub

@router.callback_query(F.data == 'translate' and standgold.bank)
async def cataloge(callback: CallbackQuery, state: FSMContext):
    await state.set_state(standgold.translate)
    await callback.answer('Выберите способ перевода')
    await callback.message.answer('Выберите способ перевода', reply_markup=kb.bank)
    await callback.message.delete()

@router.callback_query(F.data == 'SBP')
async def SBP(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Действуйте по инструкции')
    data = await state.get_data()
    golda = int(data['gold'])
    await callback.message.answer(f'Отправьте скриншот перевода, {data['gold']} и получите {round(golda / 0.66, 2)} ваше Имя и Отчёство +79087976609 Константин.К Тинькофф')
    await callback.message.delete()
    

@router.callback_query(F.data == 'Sberbank')
async def SBP(callback: CallbackQuery):
    await callback.answer('Действуйте по инструкции')
    await callback.message.answer(f'💳Карта: 2202202013287409 ❗️Получатель -Константин Алекандрович К. 💰 Сумма: {rub} ₽ 🍯 Игровая комиссия рынка на нас. Вам на аккаунт придет ровно: {golda} 📸 После оплаты, нажмите ✅ Я перевел')
    await callback.message.delete()

@router.callback_query(F.data == 'Tinkoff')
async def SBP(callback: CallbackQuery):
    await callback.answer('Действуйте по инструкции')
    await callback.message.answer('Отправьте скриншот перевода, ваше Имя и Отчёство +79087976609 Константин.К Тинькофф(Т.Банк)')
    await callback.message.delete()

@router.callback_query(F.data == 'Alfa')
async def SBP(callback: CallbackQuery):
    await callback.answer('Действуйте по инструкции')
    await callback.message.answer('Отправьте скриншот перевода, ваше Имя и Отчёство +79087976609 Константин.К Альфа Банк')
    await callback.message.delete()

@router.callback_query(F.data == 'Vtb')
async def SBP(callback: CallbackQuery):
    await callback.answer('Действуйте по инструкции')
    await callback.message.answer('Отправьте скриншот перевода, ваше Имя и Отчёство +79087976609 Константин.К Втб Банк')
    await callback.message.delete()

@router.callback_query(F.data == 'Qiwi')
async def SBP(callback: CallbackQuery):
    await callback.answer('Действуйте по инструкции')
    await callback.message.answer('Отправьте скриншот перевода, ваше Имя и Отчёство +79087976609 Константин.К Qiwi Кошелек')
    await callback.message.delete()

@router.callback_query(F.data == 'Ymoney')
async def SBP(callback: CallbackQuery):
    await callback.answer('Действуйте по инструкции')
    await callback.message.answer('В разработке')
    await callback.message.delete()