# Automax Cart API (Backend)

## Rodando
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --reload --port 8000
