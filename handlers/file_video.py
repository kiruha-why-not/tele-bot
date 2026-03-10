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
from forms.user import Form
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from aiogram.types import FSInputFile

router = Router()


@router.message(Command('start'))
async def start (message: Message, state: FSMContext):
    await message.answer('Давай заполним анкету\nВведи свое имя:')
    await state.set_state(Form.name)


@router.message(Command('cancel'))
async def cancel_form(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Заполнение прервано')


@router.message(Form.name, F.text)
async def proccess_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer('Красаучик\nСколько тебе лет?')
    await state.set_state(Form.age)


@router.message(Form.age, F.text)
async def proccess_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Число введи придурок!')
        return
    
    if 100 > int(message.text) < 1:
        await message.answer('Возраст должен быть от 1 до 100 лет')
        return
    
    await state.update_data(age=int(message.text))

    await message.answer('Старичок\nТеперь введи свою почту')
    await state.set_state(Form.email)


@router.message(Form.email, F.text)
async def proccess_email(message: Message, state: FSMContext):
    email_text = message.text

    if '@' not in email_text or '.' not in email_text:
        await message.answer('Email не корректный')
        return
    
    await state.update_data(email=email_text)

    data = await state.get_data()
    name = data['name']
    age = data['age']
    email = data['email']

    await message.answer(f'Анкета готова\nИмя: {name}\nВозраст: {age}\nПочта: {email}')
    await state.clear()


@router.message(F.photo)
async def process_photo(message: Message):
    photo = message.photo[-1]
    file_id = photo.file_id

    await message.answer(
        f'Вы отправили photo\nID video: <code>{file_id}</code>',
        parse_mode='HTML'
    )

    await message.answer_photo(file_id, caption='Вот шо ты отправил!')


@router.message(F.video)
async def process_video(message: Message):
    video = message.video
    file_id = video.file_id
    duration = video.duration

    await message.answer(
        f'Вы отправили video\nID video: <code>{file_id}</code>\nДлительность видео - <code>{duration}</code> секунд',
        parse_mode='HTML'
    )

    await message.answer_video(file_id, caption='Вот шо ты отправил!')


@router.message(F.animation)
async def process_animation(message: Message):
    animation = message.animation
    

    await message.answer(
        f'Вы отправили animation\nID animation: <code>{animation.file_id}</code>',
        parse_mode='HTML'
    )

    await message.answer_animation(animation.file_id, caption='Вот шо ты отправил!')


@router.message(F.document)
async def process_document(message: Message, bot: Bot):
    document = message.document
    file_id = document.file_id

    file = await bot.get_file(file_id)
    file_path = file.file_path

    local_path = f'downloads/{document.file_name}'

    await bot.download_file(file_path=file_path, destination=local_path)

    await message.answer('File saved)')


@router.message(Command('file'))
async def send_file(message: Message):
    file = FSInputFile('files/example.txt')

    await message.answer_document(file)
'''
