```
cd backend
python3.11 -m venv .venv
source ./.venv/bin/activate
pip install-r requirements.txt
fastapi dev main.py
```

Включите vpn (по крайнер мере у меня не грузит) и откройте `http://127.0.0.1:8000/docs#/`

Vpn нужен для прогрузки фронта OpenAPI

Сырое API есть тут `http://127.0.0.1:8000/openapi.json`, для запуска vpn не нужен

TODO чеклист:
- [x] API исследований
- [] API графиков
- [] API врачей
- [] База данных соответственно
- [] Логика распределения
- 

