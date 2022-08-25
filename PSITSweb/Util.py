import hashlib


def hashData(data: str) -> str:
    result = hashlib.md5(data.encode()).hexdigest()
    return str(result)


def isAdmin(uid) -> bool:
    admins: dict = {
        'ABEJAR': '19889781',
        'RIBO': '19895283',
        'COLONIA': '20220885',
        'BELMONTE': '19871367',
        'SIERRA': '19889898',
        'ABELLANA': '21471909',
        'DUCAL': '19880152',
        'ANIBAN': '21496369',
        'CEMPRON': '19841998',
        'COSTILLAS': '21540950',
        'LEYROS': '21435474'
    }
    for key, value in admins.items():
        if str(value).__eq__(str(uid)):
            return True
    return False
