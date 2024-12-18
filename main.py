from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import API_TOKEN, OPENAI_API_KEY, ADMIN_LIST, CHANNEL_ID
from chat_gpt_manager import ChatGPTClient
from json_db_tool import json_tool
json_tool = json_tool()
import time, asyncio
from quotes_api import QuotesAPI
from fusion_brain_manager import create_image, delete_image

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

examples_db = json_tool.load_db("examples.json")
text_examples_list = []
for text in examples_db["post_text"]:
    text_examples_list.append(text)

image_prompt_examples_list = []
for prompt in examples_db["post_text"]:
    image_prompt_examples_list.append(prompt)

runned = False

@dp.message_handler(content_types=['text'])
async def send_welcome(message: types.Message):
    global runned

    async def make_post():
        random_quote = QuotesAPI.get_random_quote()
        ai_role="Ты редактор платформы на которой публикуются мотивационные фразы и к ним привязанные изображения великих личностей нашего мира."
        ai_prompt=f"Вот фраза: {random_quote}\n\nСейчас оформишь ее так, чтобы можно было легко и быстро прочесть, при этом добавь красивого оформления (отступы \n), переведи и напиши только на русском, соблюдай в формальном стиле, убери лишние кавычки. Вот примеры, ориентируйся, но не используй их: {", ".join(text_examples_list)}"
        post_text = chat_gpt_request(role=ai_role, prompt=ai_prompt)
        post_image_prompt = chat_gpt_request(role=ai_role, prompt=f"Вот фраза: {random_quote}, нужно к ней написать промпт для генерации изображения как в этих примерах: {", ".join(image_prompt_examples_list)}\n")
        print(post_image_prompt)
        image_path = await create_image(message.message_id, prompt=post_image_prompt)
        image = open(image_path, 'rb')
        await bot.send_photo(CHANNEL_ID, caption=post_text, photo = image)
        await delete_image(image_path)

    if str(message.from_user.id) in ADMIN_LIST:
        if message.text == "/post":
            await message.reply("Отправляем...")
            await make_post()
            await message.answer("Отправлено!")

        if message.text == "/start":
            if not runned:
                await message.reply("Запущено")
                print("Запущено")
                runned = True
                
                while runned:
                    await make_post()
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
    return response

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)