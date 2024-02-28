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
``` 
sudo vim /etc/systemd/system/setserver.service
```
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

## 4. Настройка nginx
Открыть файл `/etc/nginx/sites-available/default`:
```
sudo vim /etc/nginx/sites-available/default
```
и в двух строках, начинающихся с `listen`, убрать инструкцию `default_server`.
Создать файл в папке `/etc/nginx/sites-available`:
``` 
sudo vim /etc/nginx/sites-available/setserver
```
и вставить в него, также заменив `имя_пользователя` на вашего пользователя:
```
server {
        listen 80 default_server;
        listen [::]:80 default_server;

        root /var/www/html;
        index _;
        server_name _;

        location / {
                proxy_pass http://unix:/home/имя_пользователя/setserver/setserver.sock;
        }
}
```
Создать символическую ссылку на этот созданный файл в папке `/etc/nginx/sites-enabled`:
```
sudo ln -s /etc/nginx/sites-available/setserver /etc/nginx/sites-enabled/
```
Открыть конфигурационный файл:
```
sudo vim /etc/nginx/nginx.conf
```
и в нём поменять в первой строке `user www-data;` на `user имя_пользователя;`.

## 5. Проверка изменений
```
sudo service nginx configtest
sudo service nginx reload
```
При возникновении ошибок необходимо проверить файл `/etc/nginx/sites-available/setserver` на соответствие с шаблоном выше или просмотреть лог ошибок при помощи команды `journalctl -xeu nginx.service`.
Далее обновить созданный сервис и запустить его:
```
sudo systemctl daemon-reload
sudo service setserver start
sudo systemctl enable setserver
```
Для проверки статуса сервиса можно использовать команду `sudo service setserver status`.









