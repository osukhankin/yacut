# YaCut - Сервис укорачивания ссылок
## Описание
Сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.
### Возможности

- Генерация коротких ссылок и связь их с исходными длинными ссылками.
- Переадресация на исходный адрес при обращении к коротким ссылкам.
- REST API

### Технологии

* FLask
* SQLAlchemy

## Запуск проекта:
Клонировать репозиторий и перейти в него в командной строке:


```
git clone https://github.com/osukhankin/yacut.git
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

В корне проекта создайте `.env` файл
```
FLASK_APP = yacut
FLASK_ENV = development
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=<секретный ключ>
```

Запустите команды для создания базы
```
flask db upgrade
```

Запуск сервера
```
flask run
```

## Справка
Сервисом можно воспользоваться двумя способами через Web и RestApi

### http://localhost:5000
### API (Docs: [OpenAPI](https://github.com/osukhankin/yacut/blob/master/openapi.yml))

- **POST** `/api/id/`
- **GET** `/api/id/{short_id}/`

