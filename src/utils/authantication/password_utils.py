from passlib.hash import sha256_crypt as password_hashing


def get_password_hash(password: str) -> str:
    """
        Hash a password using SHA-256 cryptographic hash function.

        Args:
            password (str): The password to hash.

        Returns:
            str: The hashed password.
        """
    return password_hashing.encrypt(password)


def verify_password_hash(given_password: str, password_hash: str) -> bool:
    """
       Verify a given password against a stored hash.

       Args:
           given_password (str): The password to verify.
           password_hash (str): The stored hashed password.

       Returns:
           bool: True if the given password matches the hash, False otherwise.
       """
    return password_hashing.verify(given_password, password_hash)
