'''
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery, 
    ReplyKeyboardMarkup, 
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

router = Router()


def get_main_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='/about')],
            [KeyboardButton(text='Старт'), KeyboardButton(text='Помощь')]
        ],
        resize_keyboard=True
    )

    return keyboard


def get_main_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Перейти на сайт', url='https://google.com')],
            [InlineKeyboardButton(text='Подробнее', callback_data='info_more')]
        ]
    )

    return keyboard

@router.callback_query(lambda c: c.data == 'info_more')
async def process_more_info(callback: CallbackQuery):
    await callback.message.answer('Бро шо тебе еще от меня надо')
    await callback.answer()


@router.message(Command('start'))
@router.message(F.text.lower() == 'старт')
async def start(message: Message):
    await message.answer('*Дарова* надоел!\nНапиши /help для помощи', 
                         parse_mode='Markdown')


@router.message(Command('help'))
async def help(message: Message):
    await message.answer('Команды:\n/start - запустить бот\n<i>/help</i> - список команд\n/about - про нас <a href="https://www.youtube.com"> </a> и не только',
                         parse_mode='HTML',
                         reply_markup=get_main_reply_keyboard())


@router.message(Command('about'))
async def about(message: Message):
    await message.answer(f'Всё тебе прям знать надо {message.from_user.first_name}', reply_markup=get_main_inline_keyboard())


@router.message()
async def mess(message: Message):
    await message.answer('Text message')
'''
