import os
import subprocess
import pystray
from PIL import Image
import threading, psutil
from mainNNN import ServerStatus
from plyer import notification

class ScriptTrayIcon:
    def __init__(self, icon_path, script_path):
        self.icon_path = icon_path
        self.script_path = script_path
        self.process = None

    def load_icon(self):
        return Image.open(self.icon_path)

    def run_script(self):
        command = ["pythonw", self.script_path]
        self.process = subprocess.Popen(command, creationflags=subprocess.CREATE_NO_WINDOW)

    def show_notification(self, title, message):
        notification.notify(
            title=title,
            message=message,
            app_name='RPC',
            app_icon=icon_path,
            timeout=3
    )

    def stop_script(self, icon, item):     
        if self.process:
            self.process.terminate()
        icon.stop()
        try:
            pid = ServerStatus().is_runnig()
            process = psutil.Process(pid)
            process.kill() 
            self.show_notification("Closed", "RPC and GMOD was closed succesfully.\nStar boy ты мой герой")
            return True
        except psutil.NoSuchProcess:
            return False
        
    def setup_tray_icon(self):
        icon = pystray.Icon("RPC")
        icon.icon = self.load_icon()
        icon.title = "RPC"
        icon.menu = pystray.Menu(
            pystray.MenuItem("Abort", self.stop_script)
        )
        icon.run()

    def start(self):
        script_thread = threading.Thread(target=self.run_script)
        script_thread.start()
        self.setup_tray_icon()

if __name__ == "__main__":
    icon_path = os.path.abspath("26dd3c2b4f3e5c8cf596d9c8ad6bdd8b.ico")
    script_path = os.path.abspath("mainNNN.py")
    tray_icon = ScriptTrayIcon(icon_path, script_path)
    tray_icon.start()
