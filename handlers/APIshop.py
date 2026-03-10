'''
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile


router = Router()

#_____________

import aiohttp

async def get_product(product_id):
    url = f'https://fakestoreapi.com/products/{product_id}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 404:
                return None
            
            data = await resp.json()
            return data

#_____________


@router.message(Command('start'))
async def start (message: Message):
    await message.answer('Я бот магазин\nВведите командy: /product ID\n\nПример: <b>/product 1</b>',
                         parse_mode='HTMl')


@router.message(Command('product'))
async def get_product_cmd(message: Message):
    parts = message.text.strip().split()

    # /product 3
    if len(parts) != 2:
        await message.answer('Вот так должен выглядеть запрос: /product 1')
        return 
    
    product_id = parts[1]
    if not product_id.isdigit():
        await message.answer('Вот так должен выглядеть запрос: /product 1')
        return

    await message.answer(f'Ищу товар с id: {product_id}')


    try: 
        product = await get_product(int(product_id))
    except Exception:
        await message.answer('Не удалось обратиться к серверу')
        return
    
    
    if product is None:
        await message.answer('Такого товара не существует')
        return

    title = product.get('title', 'No name')
    price = product.get('price', '-')
    description = product.get('description', '-')
    category = product.get('category', '-')
    image = product.get('image')

    text = (
        f'<b>title</b>\n\n'
        f'Категория: <i>{category}</i>\n'
        f'Цена: <b>{price}$</b>\n'
        f'{description}'
    )

    photo = FSInputFile('image.jpg')
    await message.answer_photo(photo=photo, caption=text, parse_mode='HTML')

    
    if image:
        await message.answer_photo(photo=image, caption=text, parse_mode='HTML')
    else:
        await message.answer(text, parse_mode='HTML')
    
'''