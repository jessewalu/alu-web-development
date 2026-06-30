#!/usr/bin/env python3
"""
User model module
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """User model representing the `users` table.

    Attributes:
        id (int): the primary key.
        email (str): the user's email.
        hashed_password (str): the user's hashed password.
        session_id (str): the user's session id.
        reset_token (str): the user's reset token.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
