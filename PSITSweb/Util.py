import hashlib
import warnings


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
        'LEYROS': '21435474',
        'PADOLINA': '21400973',
        'DE LOS REYES': '19903483',
        'FLORENTINO': '18725242',
        'CUICO': '19888957',
        'OPINA': '19884253',
        'TIEMPO': '19924414',
        'SIR DD': '613000'
    }
    for key, value in admins.items():
        if str(value).__eq__(str(uid)):
            return True
    return False


def deprecated(message):
    def deprecated_decorator(func):
        def deprecated_func(*args, **kwargs):
            warnings.warn("{} is a deprecated function. {}".format(func.__name__, message),
                          category=DeprecationWarning,
                          stacklevel=2)
            warnings.simplefilter('default', DeprecationWarning)
            return func(*args, **kwargs)
        return deprecated_func
    return deprecated_decorator


# Appends \ on ` \ ' and "
def contentVerifier(content: str) -> str:
    text = content.replace("'", "\\'")
    text = text.replace('"', "\\\"")
    text = text.replace('`', "\\`")
    print(text)
    return text
