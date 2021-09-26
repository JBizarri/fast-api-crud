import os

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from .company.models import Company
from .user.auth import generate_password
from .user.models import User, UserStatus


def create_initial_state(base, engine: Engine):
    base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        root_email = os.environ["ROOT_EMAIL"]
        query = select(User).where(User.email == root_email)
        if not session.execute(query).unique().scalar_one_or_none():
            root_company = Company(name="Administration")
            password = generate_password(os.environ["ROOT_PASSWORD"])
            root_user = User(
                email=root_email,
                username="root",
                password=password,
                status=UserStatus.ACTIVE,
                company=root_company,
            )
            session.add(root_user)
            session.commit()
