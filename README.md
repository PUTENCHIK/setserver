# Развёртывание приложения на Ununtu

## 1. Установка пакетов
```
sudo apt install python3 python3-pip nginx gunicorn
pip install flask
```

## 2. Клонирование git-репозитория
В домашней директории клонировать проект:
```
cd
git clone https://github.com/PUTENCHIK/setserver
```

## 3. Создание сервиса для проекта
Создать файл сервиса:
` sudo vim /etc/systemd/system/setserver.service `
Вставить в созданный файл, соответственно заменив `имя_пользователя` на вашего пользователя:
```
[Unit]
Description=Service setserver for game Set server.
After=network.target

[Service]
User=имя_пользователя
Group=имя_пользователя
WorkingDirectory=/home/имя_пользователя/setserver
ExecStart=/usr/bin/gunicorn --workers 1 --bind unix:/home/имя_пользователя/setserver/setserver.sock run:app

[Install]
WantedBy=multi-user.target
```

## Настройка nginx
