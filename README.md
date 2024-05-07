# Интеграция RPC в Discord для WRP

![logo](Images/WRP_logo.png)

**RPC (Rich Presence) в Discord позволяет отображать информацию о текущей игре пользователям. Этот проект позволяет автоматически устанавливать RPC при запуске вашей игры.**

## Установка

1. **Склонируйте репозиторий:**
   ```bash
   cd Desktop
   git clone https://github.com/v1lmok/RPC_WRP.git
   ```
2. **Установите зависимости:**
   ```
   python setup.py
   ```
## Использование
1. **Запустите скрипт:**
   ```
   python main.py
   ```
2. **Отредактируйте файл `settings.ini` по пути `C:\RPC` согласно вашему [ID](https://youtu.be/4qT4BbN-yNU):**

   ```settigs.ini
   [Settings]
   user_id = *ur id*
   ```
3. **Запустите main.py повторно с измененым ID, чтобы увидеть статус в Discord.**

## Пример

![Example](Images/Example.png)

## Лицензия
**Этот проект лицензирован по лицензии MIT. Подробности см. в файле [LICENSE](LICENSE).**
