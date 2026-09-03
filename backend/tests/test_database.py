from sqlalchemy import text

from app.database.connection import engine


try:
    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT current_database(), current_user;")
        )

        row = result.fetchone()

        print("\n==============================")
        print("DATABASE CONNECTION SUCCESS")
        print("==============================")

        print(f"Database: {row[0]}")
        print(f"User:     {row[1]}")

except Exception as error:

    print("\n==============================")
    print("DATABASE CONNECTION FAILED")
    print("==============================")

    print(error)