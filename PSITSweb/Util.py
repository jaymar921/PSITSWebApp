import hashlib


def hashData(data: str) -> str:
    result = hashlib.md5(data.encode()).hexdigest()
    return str(result)


def isAdmin(uid) -> bool:
    return str(uid).__eq__('19889781')
