from vkbottle.dispatch.rules import ABCRule
from vkbottle.bot import Bot, Message
from datetime import datetime
import asyncio
from sys import argv

adm_ids = [348406748, 530160180]
ignore_ids = [630090001, 348406748, 530160180, 223964340]
timer = dict({3:0, 4:0, 5:0})
timer_ls = dict()
task = 0
worker = True


class PeechatRule(ABCRule[Message]):
    async def check(self, event: Message) -> bool:
        global worker
        return ("печат" in event.text.lower() or "скан" in event.text.lower()) and event.from_id not in ignore_ids and worker and "цвет" not in event.text.lower()


class AdminRule(ABCRule[Message]):
    async def check(self, event: Message) -> bool:
        return event.from_id in adm_ids


async def typing():
    while True:
        await bot.api.messages.set_activity(type='typing', peer_id=2e9+5)
        await asyncio.sleep(4)


bot = Bot(token=f"{argv[1]}")
bot.labeler.vbml_ignore_case = True


@bot.on.private_message(AdminRule(), text="515старт")
async def typer(message: Message):
    global task
    try:
        if not task.done():
            await message.answer("Тайпинг уже был установлен")
        else:
            raise Exception('typing successful')
    except:
        task = asyncio.create_task(typing())
        await message.answer("Тайпинг установлен")


@bot.on.private_message(AdminRule(), text="515стоп")
async def typer(message: Message):
    global task
    try:
        if not task.done():
            task.cancel()
            await message.answer("Тайпинг снят")
        else:
            raise Exception("typing_not")
    except Exception:
        await message.answer("Тайпинг не был установлен")


@bot.on.private_message(AdminRule(), text=["515нет", "515да"])
async def working(message: Message):
    global worker, timer_ls
    worker = True if message.text=="515да" else False
    await message.answer(f"Установлено \"{message.text[3:]}\"")
    timer_ls = dict()

@bot.on.chat_message(PeechatRule())
async def print_handler(message: Message):
    if datetime.now().timestamp() - timer[message.chat_id] > 100:
        await message.reply(message="Пиши мне в лсь!")
        timer[message.chat_id] = datetime.now().timestamp()

@bot.on.private_message()
async def retranc(message: Message):
    if message.from_id not in timer_ls.keys():
        timer_ls.update({message.from_id: 1500})
    if datetime.now().timestamp() - timer_ls[message.from_id] > 900:
        if worker:
            await message.answer("515 работает и получила сообщение. Скидывайте файлы, заходите, ждём!")
        else:
            await message.answer("515 временно не работает, но сообщение получила. Мы сообщим Вам, когда комната будет работать.")
        timer_ls[message.from_id] = datetime.now().timestamp()
    await bot.api.messages.send(forward_messages=[message.id], user_id=530160180, random_id=0)
    await bot.api.messages.send(forward_messages=[message.id], user_id=348406748, random_id=0)

bot.run_forever()
