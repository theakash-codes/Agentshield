from app.database.connection import engine
from app.database.schema import Base

from app.models import Agent


Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")