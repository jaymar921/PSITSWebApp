import hashlib


def hashData(data: str) -> str:
    result = hashlib.md5(data.encode()).hexdigest()
    return str(result)


def isAdmin(uid) -> bool:
    admins: dict = {
        'ABEJAR': '19889781',
    }
    for key, value in admins.items():
        if str(value).__eq__(str(uid)):
            return True
    return False
