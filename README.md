# Gluten-Free AI Recipe Generator Backend (Fixed)

This is the updated Flask backend for your gluten-free AI recipe generator. It includes:
- Compatibility with openai>=1.0.0
- CORS support for local HTML testing
- A friendly homepage route

## Setup

1. Set `OPENAI_API_KEY` as an environment variable.
2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run the app:

```
python app.py
```

## Endpoints

- `GET /` – basic test message
- `POST /generate` – accepts a prompt and returns a recipe

Enjoy!
