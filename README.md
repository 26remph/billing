
#### Changelog:
v0.0.10 - notify mvp version
v0.0.20 - templater service complete
v0.0.20 - newsletter service add

Этот репозиторий: [https://github.com/26remph/notifications_sprint_1.git](https://github.com/26remph/notifications_sprint_1.git)


# Notification сервис для on-line кинотеатра

## О сервисе

Сервис реализующий возможность работы с маркетинговыми рассылками и уведомлениями пользователей.  

## 1. Описание разрабатываемой функциональности
Севрис состоит из слкедуэщих компонент.

#### Templater
- Реализует CRUD API для работы с шаблонами рассылок. 
- Шалоны сохраняются в базе данных MongoDB. Тип шаблонов jinga2 
- Парсит макеты и проводит валидацию переменных;

#### Notify
Микросервис отвечающий за реализацию доставки уведомлений пользователей.
В основе своей имеет Celery + RabbitMQ + Cellery worker + Cellery bit. В качесвте результирующего бэкэнад Redis.
Сообщения сначала попадают в воркер отвечающий за обогащение макетов, потом в воркер по отправке макетов. Для периодической рассылки имеет свой воркер. Так же имеется воркер для системных событий. Что обеспечивет распределение нагрузки.

- Принимает и отправляет мгновенные сообщения от ссервисов auth, ugc;
- Отправляет немедленную рассылку ручную от сервиса newsletter;
- Принимает и выполняет переодические задач от сервиса маркетинговой рассылки newsletter
- Выполняет системные задачи синхронизации

### NewsLetter
Занимается отправкой созданных рассылок от менеджеров кинотеатра. Имеет сво базу данных
[Схема базы данных](https://dbdesigner.page.link/Fnz83LWdQYdgChVo6)

Стек: PostgresSQL + alchemy + alembic + sqlaadmin

- Сервис создает рассылку, указывает получателей и шаблон после чего отправляет его в сервис `notify`;
- имеет свою админ панель

<img src="./doc/2023-11-23_09-00-38.png" width="600"/>

## 2. Архитектура решения

### Схемы архитектуры

Архитектурно выбрано REST API c реализацией на fastapi и в качестве хранилища MongoDB, Postgres, Redis

<img src="./doc/img.png" width="600"/>

### Технологии

Для реализации выбран следующий стек технологий  
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)  
![RabbitMQ](https://img.shields.io/badge/Rabbitmq-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)  
![pythonversion](https://img.shields.io/badge/python-%3E%3D3.10.8-blue)  

## 3. Как запустить проект

<details>
<summary>Полный запуск на локальном хосте</summary>
<p>

1. Для работы проекта необходимо установить `docker`. Проверить доступность команды `docker compose` в вашей ОС.

    ```shell
        docker compose -f ./docker-compose.yml up -d
    ```

2. Запустить сервсисы в режиме разработки:

    ```shell
        make run-notify
        make run-news
        make rin-templater
    ```
Дождаться запуска. Процедура должна завершится бкз ошибок.


6. Если все прошло успешно, то будут доступны адреса (при настройке как в `.env.example`):

    * [notify API](http://localhost:8080/)  
    * [templater API](http://localhost:8088/)  
    * [newsletter API](http://localhost:8090/)  
    * [admin panel](http://localhost:8090/admin)  


7. Остановить сервисы командой:

    ```shell
        docker compose -f ./infra/docker-compose.yml down
    ```

</p>
</details>

## 4. Реализация

Представлена в репозитарии.  

## Об авторах

* [Вадим Барсуков](https://git.yandex-academy.ru/v.bars), python-developer

