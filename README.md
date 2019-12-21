# tcpping

Версия 0.2.2

Автор: Черенцов Павел (pavelcherentsov23@gmail.com)

Ревью выполнили: Самунь Виктор Сергеевич


## Описание
Сетевая утилита tcpping.

Этот скрипт представляет собой эмуляцию хорошо известной команды ping, 
за исключением того, что он использует пакеты TCP SYN.


## Состав
* Консольная версия: `tcpping.py`
* Модули: `modules/`
* Тесты: `tests/` 


## Справка
Справка по запуску: `sudo python3 tcpping.py -h`

## Консольная версия
Пример запуска : 
* `$ sudo python3 tcping.py google.com:80 127.0.0.1:8888 255.255.0.0:1 
-c 1 -t 3 -i 1`

Вывод:

    TCPing google.com (108.177.14.101:80).
    Flag.SYN_ACK	 44 bytes from google.com:80 	 time=50.52 ms
    --- google.com tcping statistics ---
    1 transmitted, 1 received 0.0% packet loss, time 50.52 ms
    rtt min/avg/max = 50.52/50.52/50.52 ms
    TCPing 127.0.0.1 (127.0.0.1:8888).
    Flag.RST	 40 bytes from 127.0.0.1:8888 	 time=0.09 ms
    --- 127.0.0.1 tcping statistics ---
    1 transmitted, 0 received 100.0% packet loss, time 0.09 ms
    rtt min/avg/max = 0.09/0.09/0.09 ms
    TCPing 255.255.0.0 (255.255.0.0:1).
    Flag.NO_ANSWER	 0 bytes from 255.255.0.0:1 	 time=3003.44 ms
    --- 255.255.0.0 tcping statistics ---
    1 transmitted, 0 received 100.0% packet loss, time 3003.44 ms
    rtt min/avg/max = 3003.44/3003.44/3003.44 ms



## Подробности реализации
Модули, отвечающие за работу утилиты, расположены в пакете modules.
На данные модули (`modules`) написаны тесты, их можно найти в `tests/`.
Покрытие по строкам составляет около 92%:

    Name                Stmts   Miss  Cover
    ---------------------------------------
    modules/Packet.py      61      0   100%
    modules/TCPing.py      63      6    90%
    tcping.py              19      9    53%
    tests/test_all.py      51      1    98%
    ---------------------------------------
    TOTAL                 194     16    92%