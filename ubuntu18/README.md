# Описание

Инструкция по установке Python-бота c нуля на Ubuntu 18.

Если это оказалось полезно, то вы можете меня поблагодарить в комментариях к видео и даже задонатить http://patreon.com/iteveryday

* Посмотреть видео-урок: https://youtu.be/wO2Po55qMuI
* Ссылка на хостинг из видео: http://bit.ly/2E6CrAh

# Установка с нуля

Выполнить в консоле сервера при первом включении:
```
apt update
apt install -y htop git build-essential libssl-dev libffi-dev python3-pip python3-dev python3-setuptools python3-venv 
```

Создать пользователя:
```
adduser vladimir
```

Переключиться на нового пользователя:
```
whoami
su - vladimir
whoami
```

Клонировать репозиторий:
```
cd /home/vladimir
git clone https://deQUone@bitbucket.org/vkasatkin/tele_bot.git
```

Создать вирутальное окружение:
```
cd /home/vladimir/tele_bot
python3 -m venv .venv
```

Активировать вирутальное окружение и установить пакеты:
```
source /home/vladimir/tele_bot/.venv/bin/activate
pip install -r /home/vladimir/tele_bot/pip-requirements.txt
```

Проверить что бот работает (из виртуального окружения):
```
/home/vladimir/tele_bot/.venv/bin/python /home/vladimir/tele_bot/ubuntu18/main.py
```

Использовать конфиг для автоматического запуска "tgbot.service"

Прописать в нём своего пользователя, пути и положить его в папку (из-под root):
```
sudo cp /home/vladimir/tele_bot/ubuntu18/tgbot.service /etc/systemd/system/tgbot.service
```

Запустить бота:
```
sudo systemctl start tgbot
sudo systemctl enable tgbot
```

Проверить как дела:
```
sudo systemctl status tgbot
```


# Обновление кода

Скачать свежий код из репозитория:
```
cd /home/vladimir/tele_bot
git fetch && git checkout -f origin/master 
```

Перезапустить бота:
```
sudo systemctl start tgbot
```
