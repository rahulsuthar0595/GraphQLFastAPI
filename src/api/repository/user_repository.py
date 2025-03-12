import logging

from sqlalchemy import func

from src.api.models.users import User

logging.basicConfig(level=logging.INFO)


async def create_user(db, email: str, hashed_password: str, role: str):
    try:
        new_user = User(email=email, hashed_password=hashed_password, role=role)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        logging.error(f"Error in repository create_user: {e}")
        raise e


async def get_user_by_email(db, email: str):
    try:
        user = (
            db.query(User)
            .filter(func.lower(User.email) == email.strip().lower())
            .first()
        )
        return user
    except Exception as e:
        logging.error(f"Error in repository get_user_by_email: {e}")
        raise e
