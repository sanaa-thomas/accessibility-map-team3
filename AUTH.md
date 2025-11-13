This is how to install the necessary things to make login work

# 1. Create + activate a venv (do this from your repo root)

python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Upgrade packaging tools (helps bcrypt install smoothly)
'''
python -m pip install --upgrade pip setuptools wheel
'''

# 3. Install packages (use uvicorn[standard] for the common extras)
'''
pip install fastapi uvicorn[standard] mysql-connector-python bcrypt python-dotenv
'''
# 4. Quick Check that bcrypt works
python -c "import bcrypt; print(bcrypt.hashpw(b'test', bcrypt.gensalt()))"

