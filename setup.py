import subprocess, os, json

class generate_settings:
    def setup(self):
        subprocess.run(["pip", "install", "discord-rpc", "aiohttp", "Pymem", "python-a2s", "plyer", "pystray"])

    def read_user_id_from_config(self):
        config_path = 'C:/RPC/settings.json'
        fid = input('Enter ForumID: ')
        if not os.path.exists(config_path):
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w') as configfile:
                json.dump({'ForumID': fid}, configfile, indent=4)
        else:
            with open(config_path, 'r+') as configfile:
                data = json.load(configfile)
                data['ForumID'] = fid
                configfile.seek(0)
                json.dump(data, configfile, indent=4)
                configfile.truncate()

if __name__ == '__main__':
    generate_settings().setup()
    generate_settings().read_user_id_from_config()
