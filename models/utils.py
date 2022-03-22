import secrets


def get_id():
    return secrets.token_urlsafe(6)
