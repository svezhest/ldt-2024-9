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

Пользовательский путь:

1. ADMIN или HR регистрирует новую запись.
2. Обязательно с ADMIN-ской учентной записи подтвердить создание (PATCH /doctors/{doctor_id}/account_status {account_status = 'OK'}),
3. HR может создавать и смотреть учетные записи.
4. ADMIN может подтверждать заявки, вызывать из отпуска, и т.д.
5. Также видит предсказания системы и рекомендации, сколько врачей нужно дополнительно при текущей нагрузке.
6. DOCTOR может заполнять, сколько делал за день.
7. Всем доступен личный кабинет.
 
