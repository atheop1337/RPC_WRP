import discordrpc
from discordrpc.utils import timestamp
import aiohttp, asyncio
import os
import configparser

class Information:
    async def get_data(self):
        user_id = self.read_user_id_from_config()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://forum.wayzer.ru/api/users/{user_id}") as response:
                data = await response.json()
                avatar = data['data']['attributes']['avatarUrl']
                name = data['data']['attributes']['displayName']
                realname = data['data']['attributes']['username']
                return avatar, name, realname

    def read_user_id_from_config(self):
        config_path = 'C:/RPC/settings.ini'
        if not os.path.exists(config_path):
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w') as f:
                config = configparser.ConfigParser()
                config.add_section('Settings')
                config.set('Settings', 'user_id', '96')
                config.write(f)

        config = configparser.ConfigParser()
        config.read(config_path)
        user_id = config.get('Settings', 'user_id')
        return user_id

async def rpc_connect():
    rpc = discordrpc.RPC(app_id=1237037992368148490, output=False)
    info = Information()
    avatar, name, realname = await info.get_data()
    button = discordrpc.Button(
        button_one_label="Forum",
        button_one_url=r"https://forum.wayzer.ru/",
        button_two_label="Me on forum",
        button_two_url=f"https://forum.wayzer.ru/u/{realname}"
    )
    rpc.set_activity(
        state=f'My nickname on forum is {name}',
        details=f'I\'m playing Garry\'s mod',
        buttons=button,
        large_image='wrp',
        large_text='WayZer RolePlay',
        small_image=avatar,
        small_text=name,
        ts_start=timestamp,
        ts_end=86400000000,
    )
    rpc.run()

async def main():
    await rpc_connect()

if __name__ == "__main__":
    asyncio.run(main())
