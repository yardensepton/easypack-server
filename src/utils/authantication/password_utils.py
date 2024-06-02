from passlib.hash import sha256_crypt as password_hashing


def get_password_hash(password: str) -> str:
    return password_hashing.encrypt(password)


def verify_password_hash(given_password: str, password_hash: str) -> bool:
    return password_hashing.verify(given_password, password_hash)
