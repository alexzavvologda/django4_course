# django4_course


Доработки к ДЗ № 3
---

1. инфроструктура

     виртуалка - Ubuntu 

     бд - Postgresql

приложение запущено через:
первый раз делал потратил порядка 4 часов.
т.к. делал по разным инструкциям и поиску ошибок
- сокет gunicorn.socket
- сервис gunicorn.service
- конфигурация nginx

 исходники в папке install_for_server

2. в работе приложения:

- на главной странице временно вынес пример работы ajax вывод данных из бд без перезагрузки страницы
 

- проверка авторизации как на функциях, так и на классах 
    + переброс на страницу авторизации если она необходима


- ссылки скрыты на стороне шаблонов по признаку принадлежности к группам автор,
также проверяется на стороне бекенда


- сделал если не авторизированный пытается в избранное добавить, то перекидываю на авторизацию

3.  добавил работу с почтой.

 - при регистрации или авторизации получаю письмо с логином и ip адресом
также при создании новости


4. :( На чистку статей сил и времени уже не хватило.
        может что-то еще подчищу.
5. в проекте много где есть комменты и всякие принты.
этот проект для меня будет как записная книжка, где реализовали разные подходы в задачах.


PS:
!!!!! не получилось на сервере из requirements.txt доустанавливал поштучно  2 библиотеки
#Pillow==10.1.0
#psycopg2==2.9.9

pip install --only-binary Pillow Pillow
pip install psycopg2 

на сервере для запуска через сервис  ставил gunicorn

