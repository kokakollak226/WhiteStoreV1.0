from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import app.keyboards as kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()

class standgold(StatesGroup):
    gold = State()
    bank = State()
    translate = State()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    state.clear
    await message.answer(f'Здравствуйте {message.from_user.first_name}', reply_markup=kb.main)
    

@router.message(F.text == 'Купить')
async def buy(message: Message, state: FSMContext):
    await state.set_state(standgold.gold)
    await message.answer(f'Введите количество голды которое желаете приобрести')

    
@router.message(standgold.gold)
async def sum(message: Message, state: FSMContext):    
    try:
        golds = int(message.text)
        await state.update_data(gold=message.text)
        await message.answer(f'{int(golds * 0.66)} Руб за {golds} GOLD') 
        await message.answer('Выберите способ оплаты', reply_markup=kb.pay)
        await state.set_state(standgold.bank)
    except Exception:
        message.answer('Введите целое число')

@router.callback_query(F.data == 'Crypto')
async def cataloge(callback: CallbackQuery):
    await callback.answer('Выберите способ перевода')
    await callback.message.answer('В разработке')

@router.callback_query(F.data == 'translate' and standgold.bank)
async def cataloge(callback: CallbackQuery, state: FSMContext):
    await state.set_state(standgold.translate)
    await callback.answer('Выберите способ перевода')
    await callback.message.answer('Выберите способ перевода', reply_markup=kb.bank)

@router.callback_query(F.data == 'SBP')
async def SBP(callback: CallbackQuery):
    await callback.answer('Действуйте по инструкции')
    await callback.message.answer('Отправьте скриншот перевода и ваше Имя и Отчёство +79087976609 Константин.К Тинькофф')

@router.callback_query(F.data == 'Sberbank')
async def SBP(callback: CallbackQuery):
    await callback.answer('Действуйте по инструкции')
    await callback.message.answer('Отправьте скриншот перевода и ваше Имя и Отчёство +79087976609 Константин.К Сбербанк')

@router.callback_query(F.data == 'Tinkoff')
async def SBP(callback: CallbackQuery):
    await callback.answer('Действуйте по инструкции')
    await callback.message.answer('Отправьте скриншот перевода и ваше Имя и Отчёство +79087976609 Константин.К Тинькофф(Т.Банк)')

@router.callback_query(F.data == 'Alfa')
async def SBP(callback: CallbackQuery):
    await callback.answer('Действуйте по инструкции')
    await callback.message.answer('Отправьте скриншот перевода и ваше Имя и Отчёство +79087976609 Константин.К Альфа Банк')

@router.callback_query(F.data == 'Vtb')
async def SBP(callback: CallbackQuery):
    await callback.answer('Действуйте по инструкции')
    await callback.message.answer('Отправьте скриншот перевода и ваше Имя и Отчёство +79087976609 Константин.К Втб Банк')