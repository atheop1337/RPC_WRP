import time
import pypresence
import aiohttp, asyncio, requests
import json, os, signal
import pymem, psutil, subprocess
import re
import webbrowser
from winreg import OpenKeyEx, HKEY_LOCAL_MACHINE, QueryValueEx
from colorama import Fore, Style

# Cleverly done, Mr. Freeman, but you're not supposed to be here.

class Information:

    def __init__(self):
        self.version = '1.0'

    async def get_data(self):
        user_id = self.read_id()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://forum.wayzer.ru/api/users/{user_id}") as response:
                data = await response.json()
                avatar = data['data']['attributes']['avatarUrl']
                name = data['data']['attributes']['displayName']
                realname = data['data']['attributes']['username']
                return avatar, name, realname

    def get_version(self):
        url = "https://pastebin.com/raw/HiMCYGR9"
        response = requests.get(url)
        if response.status_code == 200:
            json_data = json.loads(response.text)
            return True if json_data['version'] == self.version else False
        else: return 404

    def read_id(self):
        config_path = 'C:/RPC/settings.json'
        if not os.path.exists(config_path):
            print("Config file not found.")
            return
        with open(config_path, 'r') as configfile:
            data = json.load(configfile)
            user_id = data.get('ForumID')
        return user_id

    def get_path(self):
        return QueryValueEx(OpenKeyEx(HKEY_LOCAL_MACHINE,r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App 4000"),'InstallLocation')[0]+'\\hl2.exe'

class Mr_Freeman:

    def Mr_Freeman(self):
        url = 'https://youtu.be/1snyDYHnkL8'
        webbrowser.open(url)

    def terminate_process(self):
        pid = ServerStatus().is_runnig()
        try:
            process = psutil.Process(pid)
            process.kill()
            return True
        except psutil.NoSuchProcess:
            print(f"Process with PID {pid} not found.")
            return False

class ServerStatus:

    def __init__(self):
        self.OFS1 = 0x5B47CC
        self.OFS2 = 0x7DC1C0
        self.server_list = {"46.174.54.203": ["Riverton","riverton"], "46.174.54.52": ["Minton","minton"], "37.230.228.180": ["Carlin","carlin"], "62.122.213.48": ["Brooks","brooks"], "37.230.162.208": ["Rockford","rockford"]}

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
        server_name = self.server_list.get(ip[0])[0]
        if not server_name:
            gordon=Mr_Freeman()
            gordon.Mr_Freeman()
            gordon.terminate_process()
            quit()
        cd = str(gmod.read_bytes(client.lpBaseOfDll + self.OFS2, 100))
        if 'disconnect' in cd:return
        if "connect" in cd:
            status='Заходит на'
        else:
            status='Играет на'
        return (f"{status} {server_name}", self.server_list.get(ip[0])[1])

    def getServer(self):
        pid = self.is_runnig()
        if not pid: return
        gmod = pymem.Pymem()
        gmod.open_process_from_id(pid)
        client = pymem.pymem.process.module_from_name(gmod.process_handle, "engine.dll")
        if not client: return
        ip = re.search(r'\d+\.+\d+\.+\d+\.+\d+\d', str(gmod.read_bytes(client.lpBaseOfDll + self.OFS1, 14)))
        if not ip: return
        server_name = self.server_list.get(ip[0])[0]
        if not server_name:
            gordon = Mr_Freeman()
            gordon.Mr_Freeman()
            gordon.terminate_process()
            quit()
        return server_name

def signal_handler(sig, frame):
    gordon = Mr_Freeman()
    gordon.terminate_process()
    print('Aborting...')
    time.sleep(0.8)
    exit(0)

async def rpc_connect():
    rpc = pypresence.AioPresence(1237037992368148490)
    await rpc.connect()
    info = Information()
    ss = ServerStatus()
    time_start = int(time.time())
    avatar, name, realname = await info.get_data()
    button = [{"label": "Github", "url": r"https://github.com/v1lmok/RPC_WRP"},{"label": "Forum", "url": f"https://forum.wayzer.ru/u/{realname}"}]
    while True:
        status = ss.getStatus()
        server_name = ss.getServer()
        if not status:
            img='wrp'
        else:
            img=status[1]
            status=status[0]
        await rpc.update(state=f'My nickname on forum is {name}',
            details=status,
            buttons=button,
            large_image=img,
            large_text=server_name,
            small_image=avatar,
            small_text=name,
            start=time_start)
        await asyncio.sleep(15)

async def rpc_and_gmod():
    signal.signal(signal.SIGINT, signal_handler)
    ss = ServerStatus()
    version = Information().get_version()
    if not version:
        proceed = input(f'{Style.DIM}{Fore.YELLOW}[RPC]{Fore.RED} Invalid version! {Fore.YELLOW}Download last version or proceed?{Fore.RESET} (Y/N): ')
        if proceed.lower() == 'y': webbrowser.open('https://github.com/v1lmok/RPC_WRP')
        else:
            if not ss.is_runnig():
                subprocess.Popen(Information().get_path())
            await rpc_connect()
    elif version == 404:
        print('Cannot fetch information about latest version..\nAborting...')
        time.sleep(0.8)
        webbrowser.open('https://youtu.be/aR1-kXgDCdA')
        quit(0)
    else:
        if not ss.is_runnig():
            subprocess.Popen(Information().get_path())
        await rpc_connect()

async def main():
    print('Welcome to RPC! For exit press [CTRL+C] or close manually!')
    await rpc_and_gmod()

if __name__ == "__main__":
    asyncio.run(main())