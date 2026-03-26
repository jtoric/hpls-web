# HPLS Powerlifting Website

Web stranica Hrvatskog powerlifting saveza — moderna zamjena za postojeći WordPress site.

## Tehnologije

| Komponenta | Stack |
|---|---|
| Backend | FastAPI, SQLAlchemy, SQLite, JWT auth |
| Frontend | Vue 3, Vite, TailwindCSS v4, Pinia, TipTap |
| Testovi | pytest (34 testa) |

## Pokretanje

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Inicijaliziraj bazu i seed podatke
python seed.py

# Pokreni dev server
uvicorn app.main:app --reload   # http://localhost:8000
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev                     # http://localhost:5173
```

### 3. Testovi

```bash
cd backend
python -m pytest tests/ -v
```

## Arhitektura

```
backend/
  app/
    main.py                  # FastAPI aplikacija
    config.py                # Konfiguracija (env varijable)
    database.py              # SQLAlchemy engine + sesija
    auth.py                  # JWT autentikacija
    models.py                # ORM modeli
    schemas.py               # Pydantic validacija
    routers/                 # API endpointi
      auth.py, posts.py, pages.py, documents.py, upload.py
    services/                # Poslovna logika
      auth_service.py, post_service.py, page_service.py,
      document_service.py, search_service.py, upload_service.py
    repositories/            # Upiti prema bazi
      user_repository.py, post_repository.py,
      page_repository.py, document_repository.py
  tests/                     # pytest testovi
  seed.py                    # Seed skripta (admin + početne stranice)

frontend/
  src/
    api/index.js             # Axios HTTP klijent
    stores/auth.js           # Pinia auth store
    router/index.js          # Vue Router
    components/              # Dijeljene komponente
    views/                   # Stranice (javne + admin/)
```

## Funkcionalnosti

- **Vijesti i kalendar** — Objave s kategorijama, WYSIWYG editor (TipTap), slike i prilozi
- **Statičke stranice** — Rekordi, Poredak, Kontakt, O nama (podstranice)
- **Dokumenti** — Upload i preuzimanje PDF-ova
- **Pretraga** — Pretraga po svim sadržajima
- **Admin panel** — Login, uređivanje sadržaja, upload datoteka
- **Responzivni dizajn** — Mobilni izbornik, prilagodljiv layout

## Konfiguracija

Okolišne varijable (`.env` ili export):

| Varijabla | Default | Opis |
|---|---|---|
| `DATABASE_URL` | `sqlite:///data/hpls.db` | URL baze podataka |
| `SECRET_KEY` | `dev-secret-change-in-production` | JWT secret key |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` | Trajanje tokena (min) |

## API dokumentacija

Nakon pokretanja backenda, Swagger UI dostupan na: `http://localhost:8000/docs`

## Default pristup

- **Admin:** `admin` / `admin123` (promijeni u produkciji!)
