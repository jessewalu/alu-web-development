#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt


def _hash_password(password: str) -> str:
    """Hashes a password with a randomly generated bcrypt salt.

    Args:
        password (str): the password to hash.

    Returns:
        str: the salted hash of the password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
