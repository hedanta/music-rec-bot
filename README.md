# music-rec-bot

## Инструкция по запуску
Необходимо скачать данные по [ссылке](https://drive.google.com/drive/folders/1YBCtdfMsw-cFEqxHx00ifIpCw6WLUd0f?usp=drive_link),
поместить csv файлы в папку (например, data) в корне проекта и указать её в `.env` в качестве `DATA_DIR`.

```
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
```
cp .env.example .env
# вставить токен в .env
```
```
python tools/csv_to_db.py
```
```
python -m app.main
```

## Структура

`texts` - текста базовых сообщений бота

`app` - основная папка бота

`app/handlers` - папка с хендлерами сообщений

`app/services` - папка с логикой работы

`app/model` - папка с моделью рекомендаций

`app/storage` - папка с взаимодействиями с БД

`tools` - папка с вспомогательными скриптами (заполнение БД)
