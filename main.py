import time
import pypresence
import aiohttp, asyncio
import configparser
import subprocess
from winreg import OpenKeyEx, HKEY_LOCAL_MACHINE, QueryValueEx
import pymem
import re


# Cleverly done, Mr. Freeman, but you're not supposed to be here.
class Information:
    async def get_data(self):
        user_id = self.read_id()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://forum.wayzer.ru/api/users/{user_id}") as response:
                data = await response.json()
                avatar = data['data']['attributes']['avatarUrl']
                name = data['data']['attributes']['displayName']
                realname = data['data']['attributes']['username']
                return avatar, name, realname

    def read_id(self):
        config_path = 'C:/RPC/settings.ini'
        config = configparser.ConfigParser()
        config.read(config_path)
        user_id = config.get('ForumID', 'id')
        return user_id
    def get_path(self):
        return QueryValueEx(OpenKeyEx(HKEY_LOCAL_MACHINE,r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App 4000"),'InstallLocation')[0]+'\\hl2.exe'


class ServerStatus:
    def __init__(self):
        self.OFS1 = 0x5B47CC
        self.OFS2 = 0x7DC1C0
        self.server_list = {"46.174.54.203": "Riverton", "46.174.54.52": "Minton", "37.230.228.180": "Carlin","62.122.213.48": "Brooks", "37.230.162.208": "Rockford"}

    def is_runnig(self):
        for i in ('gmod.exe', 'hl2.exe'):
            try:
                return pymem.Pymem(i).process_id
            except:
                continue
        return False

    def getStatus(self):
        pid=self.is_runnig()
        if not pid:return
        gmod=pymem.Pymem()
        gmod.open_process_from_id(pid)
        client = pymem.pymem.process.module_from_name(gmod.process_handle, "engine.dll")
        if not client:return
        ip=re.search(r'\d+\.+\d+\.+\d+\.+\d+\d',str(gmod.read_bytes(client.lpBaseOfDll + self.OFS1, 14)))
        if not ip:return
        server_name = self.server_list.get(ip[0])
        if not server_name:return
        cd = str(gmod.read_bytes(client.lpBaseOfDll + self.OFS2, 100))
        if 'disconnect' in cd:return
        if "connect" in cd:
            status='Заходит на'
        else:
            status='Играет на'
        return f"{status}: {server_name}\n{ip[0]}"


async def rpc_connect():
    rpc = pypresence.AioPresence(1237037992368148490)
    await rpc.connect()
    info = Information()
    ss = ServerStatus()
    time_start = int(time.time())
    avatar, name, realname = await info.get_data()
    button = [{"label": "Forum", "url": r"https://forum.wayzer.ru/"},{"label": "Me on forum", "url": f"https://forum.wayzer.ru/u/{realname}"}]
    while True:
        status = ss.getStatus()
        await rpc.update(state=f'My nickname on forum is {name}',
            details=status,
            buttons=button,
            large_image='wrp',
            large_text='WayZer RolePlay',
            small_image=avatar,
            small_text=name,
            start=time_start)
        await asyncio.sleep(15)


async def rpc_and_gmod():
    ss = ServerStatus()
    if not ss.is_runnig():
        subprocess.Popen(Information().get_path())
    await rpc_connect()


async def main():
    await rpc_and_gmod()

if __name__ == "__main__":
    asyncio.run(main())
