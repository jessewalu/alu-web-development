#!/usr/bin/env python3
"""Module that defines the DB class for interacting with the database."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class for handling all interactions with the users database."""

    def __init__(self) -> None:
        """Initialize a new DB instance, dropping and recreating all tables."""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Return a memoized SQLAlchemy session object."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database and return the created User object."""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Return the first User matching the given keyword argument filters.

        Raises NoResultFound if no user matches, and InvalidRequestError if
        invalid query arguments are passed.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound
        except InvalidRequestError:
            raise InvalidRequestError
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update the attributes of the user with the given user_id.

        Raises ValueError if a keyword argument does not correspond to a
        valid user attribute.
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"{key} is not a valid user attribute")
            setattr(user, key, value)
        self._session.commit()
