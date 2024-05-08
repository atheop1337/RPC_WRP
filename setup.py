import subprocess, os, importlib.util
import configparser

class generate_settings:
    def setup(self):
        subprocess.run(["pip", "install", "discord-rpc", "aiohttp", "Pymem"])

    def read_user_id_from_config(self):
        config_path = 'C:/RPC/settings.ini'
        config = configparser.ConfigParser()
        fid = input('Enter ForumID: ')
        if not os.path.exists(config_path):
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
        config.add_section('ForumID')
        config.set('ForumID', 'ID', fid)
        with open(config_path, "w") as configfile:
            config.write(configfile)

if __name__ == '__main__':
    generate_settings().setup()
    generate_settings().read_user_id_from_config()
