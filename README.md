# music-rec-bot

## Инструкция по запуску

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
python tools/db.py
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
