from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import API_TOKEN, OPENAI_API_KEY, ADMIN_LIST, CHANNEL_ID
from chat_gpt_manager import ChatGPTClient
from json_db_tool import json_tool
json_tool = json_tool()
import time, asyncio

print(CHANNEL_ID)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

posted_db = json_tool.load_db("posted.json")
posted_list = []
for post in posted_db["posted"]:
    posted_list.append(post)

runned = False

@dp.message_handler(content_types=['text'])
async def send_welcome(message: types.Message):
    global runned
    if str(message.from_user.id) in ADMIN_LIST:
        if message.text == "/post":
            await message.reply("Отправлен новый пост")
            print("Отправлен новый пост")
            await bot.send_message(CHANNEL_ID, chat_gpt_request(role="Ты редактор платформы на которой публикуются мотивационные фразы великих личностей нашего мира", prompt=f'Напиши реальную фразу известной личности в интересной подаче. Чтобы не отправлять одну и ту же фразу несколько раз, ниже список уже отправленных\n\n{posted_list}'))
            
        if message.text == "/start":
            if not runned:
                await message.reply("Запущено")
                print("Запущено")
                runned = True
                
                while runned:
                    await bot.send_message(CHANNEL_ID, chat_gpt_request(role="Ты редактор платформы на которой публикуются мотивационные фразы великих личностей нашего мира", prompt=f'Напиши реальную фразу известной личности в интересной подаче. Чтобы не отправлять одну и ту же фразу несколько раз, ниже список уже отправленных\n\n{posted_list}'))
                    await asyncio.sleep(3600)
            else: 
                await message.reply("Уже запущено")
        
        if message.text == "/stop":
            if runned:
                await message.reply("Остановлено")
                print("Остановлено")
                runned = False
            else:
                await message.reply("Уже остановлено")

        

def chat_gpt_request(role, prompt):
    api_key = OPENAI_API_KEY
    client = ChatGPTClient(api_key)
    response = client.get_response(role=role, prompt=prompt)
    posted_db["posted"].append(f'Пора бы {response}')
    posted_db["posted"] = posted_db["posted"][-30:]  # Оставляем только последние 30 записей
    json_tool.save_db("posted.json", posted_db)
    return response

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
