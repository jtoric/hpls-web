"""Seed script: creates admin user and initial pages."""
import sys
sys.path.insert(0, ".")

from app.auth import hash_password
from app.database import Base, SessionLocal, engine
from app.models import Page, User

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Create admin user
if not db.query(User).filter(User.username == "admin").first():
    admin = User(username="admin", password_hash=hash_password("admin123"))
    db.add(admin)
    print("Created admin user (username: admin, password: admin123)")
else:
    print("Admin user already exists")

# Create initial pages
PAGES = [
    {"title": "Rekordi", "slug": "rekordi", "content": "<p>Stranica rekorda - uskoro.</p>", "sort_order": 1},
    {"title": "Poredak", "slug": "poredak", "content": "<p>Stranica poretka - uskoro.</p>", "sort_order": 2},
    {"title": "Kontakt", "slug": "kontakt", "content": "<p>Kontaktirajte nas.</p>", "sort_order": 3},
    # O nama sub-pages
    {"title": "Osnivanje kluba", "slug": "osnivanje-kluba", "parent_slug": "o-nama", "content": "<p>Informacije o osnivanju kluba.</p>", "sort_order": 1},
    {"title": "Pravila", "slug": "pravila", "parent_slug": "o-nama", "content": "<p>Pravila saveza.</p>", "sort_order": 2},
    {"title": "Anti doping", "slug": "anti-doping", "parent_slug": "o-nama", "content": "<p>Anti doping informacije.</p>", "sort_order": 3},
    {"title": "Registracija natjecatelja", "slug": "registracija-natjecatelja", "parent_slug": "o-nama", "content": "<p>Informacije o registraciji.</p>", "sort_order": 4},
    {"title": "Članstvo", "slug": "clanstvo", "parent_slug": "o-nama", "content": "<p>Informacije o članstvu.</p>", "sort_order": 5},
    {"title": "Pristup informacijama", "slug": "pristup-informacijama", "parent_slug": "o-nama", "content": "<p>Pristup informacijama.</p>", "sort_order": 6},
]

for page_data in PAGES:
    if not db.query(Page).filter(Page.slug == page_data["slug"]).first():
        page = Page(**page_data)
        db.add(page)
        print(f"Created page: {page_data['title']}")
    else:
        print(f"Page already exists: {page_data['title']}")

db.commit()
db.close()
print("\nDone! You can now run: uvicorn app.main:app --reload")
