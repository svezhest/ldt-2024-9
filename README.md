Ожидается установленный npm, python3.11 + pip, sqlite3.
Скрипты рассчитаны под Linux.

```
cd backend
python3.11 -m venv .venv
source ./.venv/bin/activate
pip install-r requirements.txt
fastapi dev main.py
```

В другом окне терминала:

```
cd frontend
npm i --legacy-peer-deps
npm run dev
```

`http://127.0.0.1:8080/` -- Веб-сайт.

`http://127.0.0.1:8000/docs#/` -- Swagger, почитать доки бэкэнда.
