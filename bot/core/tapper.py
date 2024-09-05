import asyncio
from urllib.parse import unquote, quote

from pyrogram import Client
from pyrogram.errors import Unauthorized, UserDeactivated, AuthKeyUnregistered, FloodWait
from pyrogram.raw import functions
from pyrogram.raw.functions.messages import RequestWebView

from random import randint, choices

class Tapper:
    def __init__(self, tg_client: Client):
        self.tg_client = tg_client
        self.first_name = ''
        self.last_name = ''
        self.user_id = ''

    async def get_tg_web_data(self, proxy: str | None) -> str:
        if proxy:
            proxy_dict = dict(
                scheme=proxy.split(':')[0],
                hostname=proxy.split(':')[1],
                port=int(proxy.split(':')[2]),
                username=None,
                password=None
            )
        else:
            proxy_dict = None

        self.tg_client.proxy = proxy_dict

        try:
            if not self.tg_client.is_connected:
                try:
                    await self.tg_client.connect()
                    start_command_found = False
                    async for message in self.tg_client.get_chat_history('OKX_official_bot'):
                        if (message.text and message.text.startswith('/start')) or (message.caption and message.caption.startswith('/start')):
                            start_command_found = True
                            break

                    if not start_command_found:
                        peer = await self.tg_client.resolve_peer('OKX_official_bot')
                        link = choices(['default_link'], k=1)[0]  # 使用默认链接
                        await self.tg_client.invoke(
                            functions.messages.StartBot(
                                bot=peer,
                                peer=peer,
                                start_param='linkCode_' + link,
                                random_id=randint(1, 9999999),
                            )
                        )

                except (Unauthorized, UserDeactivated, AuthKeyUnregistered):
                    raise Exception("Invalid Session")

            while True:
                try:
                    peer = await self.tg_client.resolve_peer('OKX_official_bot')
                    break
                except FloodWait as fl:
                    await asyncio.sleep(fl.value + 3)

            web_view = await self.tg_client.invoke(RequestWebView(
                peer=peer,
                bot=peer,
                platform='android',
                from_bot_menu=False,
                url="https://www.okx.com/",
            ))

            auth_url = web_view.url
            tg_web_data = unquote(
                string=unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0]))
            query_id = tg_web_data.split('query_id=')[1].split('&user=')[0]
            user = quote(tg_web_data.split("&user=")[1].split('&auth_date=')[0])
            auth_date = tg_web_data.split('&auth_date=')[1].split('&hash=')[0]
            hash_ = tg_web_data.split('&hash=')[1]

            self.user_id = tg_web_data.split('"id":')[1].split(',"first_name"')[0]
            self.first_name = tg_web_data.split('"first_name":"')[1].split('","last_name"')[0]
            self.last_name = tg_web_data.split('"last_name":"')[1].split('","username"')[0]

            if self.tg_client.is_connected:
                await self.tg_client.disconnect()

            return f"query_id={query_id}&user={user}&auth_date={auth_date}&hash={hash_}"

        except Exception as error:
            print(f"Error: {error}")
            await asyncio.sleep(3)

async def run_tapper(tg_client: Client, proxy: str | None):
    while True:
        try:
            tg_web_data = await Tapper(tg_client=tg_client).get_tg_web_data(proxy=proxy)
            print(tg_web_data)
            with open('/root/okx/token1.txt', 'w') as file:
                file.write(f"{tg_web_data}\n")
            print(f"token已写入")
        except Exception as e:
            print(f"Error: {e}")

        await asyncio.sleep(43200)  # 每隔12小时运行一次

# Example usage
# tg_client = Client(...)
# asyncio.run(run_tapper(tg_client, "http://proxy:port"))
