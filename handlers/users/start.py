from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart,Text
from aiogram.dispatcher import FSMContext
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Salom, {message.from_user.full_name}!")



@dp.message_handler(commands='reg')
async def bot_start(message: types.Message,state: FSMContext):
    await state.set_state("ism")
    await message.answer(f"ism kiriting")


@dp.message_handler(state='ism')
async def bot_ism(message: types.Message,state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await state.set_state("fam")
    await message.answer(f"familya kiriting")

@dp.message_handler(state='fam')
async def reg_fam(message: types.Message,state: FSMContext):
    fname = message.text
    if fname.endswith("v"):
        await state.update_data(fname=fname)
        data=await state.get_data()
        await state.set_state("rasm")
        await message.answer(f"rasm yubor")
    else:
        await message.answer("familyezni qayta kiriting")

import json

@dp.message_handler(state='rasm',content_types="photo")
async def reg_rasm(message: types.Message,state: FSMContext):
    rasm = message.photo[-1]['file_id']
    print(type(rasm))
    await state.update_data(rasm = rasm)
    data=await state.get_data()
    d=[]
    with open("malumotlar.json",'r+') as file:
        try:
            d = json.load(file)
            print(d)
        except:
            pass
        d.append(data)
        d= json.dumps(d)
        
    with open("malumotlar.json",'w') as file:
        file.write(d)
    await state.finish()
    await message.answer_photo(data['rasm'],caption=f"siz royhatdan otdiz{data['name']}{data['fname']}")



@dp.message_handler(text="/users")
async def reg_rasm(message: types.Message):
    with open("malumotlar.json",'r+') as file:
        d = json.load(file)
    for index,data  in enumerate(d):
        await message.answer_photo(data['rasm'],caption=f"{index}. Ism: {data['name']} \nFam: {data['fname']}")

      
        

