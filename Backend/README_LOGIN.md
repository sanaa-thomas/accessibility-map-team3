# Backend — How to run and test the /auth/login flow

This short guide explains how to create an admin account and test the `/auth/login` endpoint for the backend FastAPI app.
It uses PowerShell examples (Windows). Adjust commands for other shells if needed.

## Prerequisites
- Python 3.8+ or 3.12
- The project dependencies installed in your environment (example installs below)
- A running MariaDB/MySQL server with the `campus_map` database

Recommended packages (install in your virtualenv):
```powershell
python -m pip install -U pip
python -m pip install fastapi uvicorn aiomysql mysql-connector-python
```
# PSA: If you see yellow marking on the file type "# type: ignore" it'll remove that. Also I removed Bcrypt

## Files referenced
- `Backend/create_admin.py` — helper script to create/update an admin account (interactive)
- `Backend/Login.py` — login endpoint (POST `/auth/login`)
- `Backend/database.py` — async pool provider (reads DB_* env vars)
- `Backend/main.py` — FastAPI app entrypoint

## 1) Set DB environment variables (PowerShell)
Set these in the same PowerShell session you will use to start the server.
Replace values with your local DB credentials.

```powershell
$env:DB_HOST     = "127.0.0.1"
$env:DB_PORT     = "3306"
$env:DB_USER     = "root"
$env:DB_PASSWORD = "secret1234"
$env:DB_NAME     = "campus_map"
```

Notes:
- Use `127.0.0.1` for `DB_HOST` to force TCP (avoids socket vs localhost auth differences on some systems).
- These vars are read by `database.py`, `Login.py`, and `Threshold.py`.

## 2) Create or update an admin user
Option A — interactive helper (recommended):

```powershell
cd C:\path\to\repo\Backend
python create_admin.py
# follow the prompts: username and password (won't echo)
```

This script uses the same `DB_*` env vars and will INSERT or UPDATE the admin password.

Option B — SQL (use the mariadb client):
You can use your own password and username
This is just an example
```sql
USE campus_map;
INSERT INTO Admin (username, password) VALUES ('testadmin', 'secret1234')  
  ON DUPLICATE KEY UPDATE password = VALUES(password);
```

Important: passwords are stored plaintext in the current implementation (we recommend hashing; see Security section).

## 3) Verify the admin entry exists (optional)
In the MariaDB client:

```sql
USE campus_map;
SELECT admin_id, username, password FROM Admin WHERE username = 'testadmin';
```

You should see the row you just created.

## 4) Start the FastAPI server (backend)
From the `Backend` folder (same shell with env vars set):

```powershell
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Watch for `Application startup complete.` in the console. The OpenAPI/Swagger UI will be available at `http://127.0.0.1:8000/docs`.

## 5) Test `/auth/login` in Swagger (visual)
1. Open: `http://127.0.0.1:8000/docs`
2. Find POST `/auth/login`.
3. Click **Try it out**.
4. Use a JSON body like:
```json
{ "username": "testadmin", "password": "secret1234" }
```
Or the one you just create for  yourself
5. Click **Execute** and check the response — expected success body:
```json
{ "success": true, "message": "Login successful" }
```
## Optional (Not required)

## 6) Test from PowerShell (programmatic)
Use `Invoke-RestMethod` for a quick check:

```powershell
$body = @{ username = 'testadmin'; password = 'secret1234' } | ConvertTo-Json
Invoke-RestMethod -Method Post -ContentType 'application/json' -Body $body http://127.0.0.1:8000/auth/login
```

Or use `curl`:

```powershell
curl -X POST http://127.0.0.1:8000/auth/login -H "Content-Type: application/json" -d '{"username":"testadmin","password":"secret1234"}'
```

## Troubleshooting
- Access denied (1045) when starting the app:
  - Confirm the env vars are set in the same shell used to start uvicorn.
  - Use `127.0.0.1` for `DB_HOST` if your DB user is bound to TCP.
  - Verify you can connect to the DB using the same credentials from a client (mariadb/mysql client or a small Python test script).

- Login returns 401 (Invalid username or password):
  - Verify the admin row exists and the password matches (case-sensitive).
  - Confirm request JSON uses keys `username` and `password`.

- Login returns 500 (Server error):
  - Check the uvicorn console for a Python traceback. It usually indicates a DB connectivity problem or a coding bug.


Example SQL to create a dedicated app user (run as a DB admin):
```sql
CREATE USER 'app_user'@'127.0.0.1' IDENTIFIED BY 'strongpassword';
GRANT SELECT, INSERT, UPDATE, DELETE ON campus_map.* TO 'app_user'@'127.0.0.1';
FLUSH PRIVILEGES;
```
Then update your env vars to use `app_user`/`strongpassword`.

