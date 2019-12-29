# tcpping

Версия 0.3.0

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
* Тестовый файл *.yaml: `conf.yaml` 


## Справка
Справка по запуску: `sudo python3 tcpping.py -h`

## Консольная версия
Пример запуска : 
* `$ sudo python3 tcping.py conf.yaml`

Вывод:
    ![Output](https://github.com/PavelCherentsov/tcpping/raw/master/image/image.png)

## Подробности реализации
Модули, отвечающие за работу утилиты, расположены в пакете modules.
На данные модули (`modules`) написаны тесты, их можно найти в `tests/`.
Покрытие по строкам составляет около 80%:

    Name                Stmts   Miss  Cover
    ---------------------------------------
    modules/Packet.py      68      0   100%
    modules/TCPing.py      85     14    84%
    tcping.py              33     33     0%
    tests/server.py        11      3    73%
    tests/test_all.py      55      1    98%
    ---------------------------------------
    TOTAL                 252     51    80%
