from app.db.database import engine, Base
from app.models.user import User
from app.models.faq import FAQ

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()

