import logging
from typing import Union

from email_validator import EmailNotValidError, validate_email
from graphql import GraphQLError

from src.api.repository.user_repository import create_user, get_user_by_email
from src.api.schemas.definitions import UserType
from src.api.utils.helpers import hash_password

logging.basicConfig(level=logging.INFO)


async def user_register(db, email: str, password: str, role: str) -> UserType | None:
    try:
        # validate email address
        validate_email(email)

        existing_user = await get_user_by_email(db=db, email=email)
        if existing_user:
            raise GraphQLError(message="User with this email already exists.")

        hashed_password = hash_password(password)
        new_user = await create_user(
            db=db, email=email, hashed_password=hashed_password, role=role
        )
        return UserType(**new_user.__dict__)
    except GraphQLError as gql_err:
        # Handle GraphQL-specific errors first
        raise gql_err
    except EmailNotValidError as e:
        raise GraphQLError(message=str(e))
    except Exception as e:
        logging.error(f"Error in service user_register: {e}")
        raise GraphQLError(message="Something went wrong")


async def fetch_user_by_email(db, email: str) -> UserType | None:
    try:
        user = await get_user_by_email(db=db, email=email)
        if not user:
            raise GraphQLError(message="User not found")

        return UserType(**user.__dict__)
    except GraphQLError as gql_err:
        # Handle GraphQL-specific errors first
        raise gql_err
    except EmailNotValidError as e:
        raise GraphQLError(message=str(e))
    except Exception as e:
        logging.error(f"Error in service user_register: {e}")
        raise GraphQLError(message="Something went wrong")


async def validate_user_login(db, email: str, password: str) -> tuple[bool, str, object]:
    try:
        user = await get_user_by_email(db=db, email=email)
        if not user:
            return False, "User not found", None

        hashed_password = hash_password(password)
        if user.hashed_password != hashed_password:
            return False, "Invalid Password", None

        return True, "Success", user
    except Exception as e:
        logging.error(f"Error in service validate_user_login: {e}")
        return False, "Something went wrong", None
