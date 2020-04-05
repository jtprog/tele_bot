Прокси для Telegram
===================

Из документации [Telegram Bot API (зеркало)](https://tlgrm.ru/docs/bots/api) запросы должны иметь вид:
```
https://api.telegram.org/bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11/getMe
```

Где `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` -- это токен, полученый от @BotFather.

Так же можно посмотреть исходники какой-нибудь библиотеки, как именно они отправляют запросы:

https://github.com/python-telegram-bot/python-telegram-bot/blob/master/telegram/bot.py#L136

Есть примерно такой код:
```python
if base_url is None:
    base_url = 'https://api.telegram.org/bot'
self.base_url = str(base_url) + str(self.token)
```


Своя прокси
-----------

Допустим у нас есть домен `test.com`, тогда мы можем сделать следующий механизм: все запросы, попадающие
на адрес `test.com/tg` будут проксироваться на адрес `api.telegram.org`.

У меня используется виртуальный сервер Ubuntu 14.04 и nginx/1.4.6.

Пример Nginx-конфига:
```
server {
    server_name test.com;

    location /tg/ {
        proxy_pass https://api.telegram.org/;
    }
}
```

https://nginx.org/ru/docs/http/ngx_http_proxy_module.html#proxy_pass

Тогда библиотеку можно будет использовать следующим образом:
```python
bot = Bot(
    base_url='http://test.com/tg/bot',
    token='123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11',
)
```

Директива `proxy_pass` в Nginx будет перенаправлять запрос с `http://test.com/tg/bot` на `https://api.telegram.org/bot`,
а так как токен дописан уже после bot, то токен тоже будет включен в запрос.

Желательно иметь корректно настроенное доменное имя (для красоты), но это необязательно.
Подключение SSL (https) так же необязательно. Nginx умеет корректно прокидывать запросы с http на https внутри себя.


Анализ на безопасность
----------------------

Смотрим лог Nginx:
```
tail -f /var/log/nginx/access.log
```

Пример запросов:
```
34.227.117.142 - - [04/Apr/2020:19:51:32 +0300] "POST /orig/bot934311337:XXX/getUpdates HTTP/1.1" 499 0 "-" "Python Telegram Bot (https://github.com/python-telegram-bot/python-telegram-bot)"
195.161.41.201 - - [04/Apr/2020:19:51:32 +0300] "POST /orig/bot902808272:XXX/getUpdates HTTP/1.1" 200 23 "-" "Python Telegram Bot (https://github.com/python-telegram-bot/python-telegram-bot)"
78.47.162.138 - - [04/Apr/2020:19:51:33 +0300] "POST /orig/bot1031351941:XXX/getUpdates HTTP/1.1" 200 23 "-" "Python Telegram Bot (https://github.com/python-telegram-bot/python-telegram-bot)"
109.252.134.144 - - [04/Apr/2020:19:51:33 +0300] "POST /orig/bot1028834795:XXX/getUpdates HTTP/1.1" 200 1408 "-" "python-requests/2.21.0"
```

Давайте разберём что тут есть:

* `34.227.117.142` -- IP автора запроса (сервера)
* ``[04/Apr/2020:19:51:32 +0300]`` -- точное время запроса
* `POST /orig/bot934311337:XXX/getUpdates HTTP/1.1` -- сам запрос, который проксируется
* `499` -- статус-код ответа (от Telegram)
* `Python Telegram Bot (https://github.com/python-telegram-bot/python-telegram-bot)`` -- заголовок "user-agent" запроса


Результат работы парсера логов:
```
INFO | 2020-04-05 16:10:45,290 | Stopped! Worked 884.13154912 sec
INFO | 2020-04-05 16:10:45,291 | Found 83 unique tokens, and 2 bad tokens
INFO | 2020-04-05 16:10:45,291 | Total requests: 11477, RPS: 12.9810999409
INFO | 2020-04-05 16:10:45,291 | Top 10 user-agents:
INFO | 2020-04-05 16:10:45,291 | #1 Python Telegram Bot (https://github.com/python-telegram-bot/python-telegram-bot) - 7059 requests
INFO | 2020-04-05 16:10:45,292 | #2 python-requests/2.18.4 - 2887 requests
INFO | 2020-04-05 16:10:45,292 | #3 python-requests/2.21.0 - 639 requests
INFO | 2020-04-05 16:10:45,292 | #4 python-requests/2.23.0 - 504 requests
INFO | 2020-04-05 16:10:45,292 | #5 Python/3.8 aiohttp/3.6.2 - 216 requests
INFO | 2020-04-05 16:10:45,292 | #6 Python/3.7 aiohttp/3.6.2 - 107 requests
INFO | 2020-04-05 16:10:45,292 | #7 python-requests/2.7.0 CPython/3.8.2 Windows/10 - 62 requests
INFO | 2020-04-05 16:10:45,292 | #8 Mozilla/4.0 (compatible; Win32; WinHttp.WinHttpRequest.5) - 3 requests
```

Довольно неплохо, получается 13 RPS от 83 ботов проходят через данную прокси!
