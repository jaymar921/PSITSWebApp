import hashlib
import warnings
import re, random
import os

ALLOWED_EXTENSIONS = set(['docx', 'pdf', 'doc', 'xls', 'txt'])


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
        'SIR DD': '613000',
        'RACUYA': '19845262'
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

"""
    I made my custom Reference code generator and parser

    Pattern -> @REFP{PRICE}-{RANDOM NUMBERS}{SINGLE CHAR}
    - created by Jayharron Mar Abejar
"""

def getRandomChar():
    a = ['A','B','C','D','E']
    return a[random.randint(0,4)]

def PriceParseRef(price: str):
    return f"@REFP{price}-{random.randint(100000000,999999999)}{getRandomChar()}"


def GetPriceRef(string: str) -> float:
    if (re.search('@REFP(\d*\.?\d)+\-[0-9]+', string)):
        return float(re.findall('((\d*\.?\d+)+\-)', string)[0][1])
    return -1.0

def GetReference(string: str):
    if (re.search('@REFP(\d*\.?\d)+\-[0-9]+', string)):
        return re.findall('([0-9]+\w)$', string)[0]
    return "INVALID"


# Rank officers
def rankOfficers(officers: list) -> list:
    new_officers: list = []

    for officer in officers:
        if 'president' in officer.position.lower():
            new_officers.append(officer)

    for officer in officers:
        if 'vp - internal' in officer.position.lower():
            new_officers.append(officer) 
    
    for officer in officers:
        if 'vp - external' in officer.position.lower():
            new_officers.append(officer)

    for officer in officers:
        if 'secretary' in officer.position.lower():
            new_officers.append(officer)

    for officer in officers:
        if 'treasurer' in officer.position.lower() and 'assistant' not in officer.position.lower():
            new_officers.append(officer)

    for officer in officers:
        if 'assistant treasurer' in officer.position.lower():
            new_officers.append(officer)

    for officer in officers:
        if 'auditor' in officer.position.lower():
            new_officers.append(officer)

    for officer in officers:
        if 'pio' in officer.position.lower():
            new_officers.append(officer)

    for officer in officers:
        if 'pro' in officer.position.lower():
            new_officers.append(officer)

    for officer in officers:
        if 'first' in officer.position.lower():
            new_officers.append(officer)

    for officer in officers:
        if 'second' in officer.position.lower():
            new_officers.append(officer)

    for officer in officers:
        if 'third' in officer.position.lower():
            new_officers.append(officer)

    for officer in officers:
        if 'fourth' in officer.position.lower():
            new_officers.append(officer)
    
    for officer in officers:
        if 'chief volunteer' in officer.position.lower():
            new_officers.append(officer)

    for officer in officers:
        if 'volunteer' in officer.position.lower() and not 'chief' in officer.position.lower():
            new_officers.append(officer)
    return new_officers


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def directoryExist(dir):
    return os.path.isdir(dir)


def createDir(dir):
    os.makedirs(dir)


def getNumberOfFiles(dir):
    return len(os.listdir(dir))


def fileExist(file):
    return os.path.exists(file)

def removeFile(file):
    return os.remove(file)


def CONFIGURATION()-> dict:
    configuration_map = {}
    with open("configuration.psits_config", "r") as config:
        lines = config.readlines()
        settings = []
        
        for line in lines:
            if '::' in line:
                settings.append(line.strip())
        for setting in settings:
            try:
                option = setting.split(' = ')[1]
                if '_' == option:
                    option = ''
                configuration_map[setting.split(' = ')[0].replace(":","").replace("=","")] = option
            except Exception as e:
                configuration_map[setting.split(' = ')[0].replace(":","").replace("=","").strip()] = ''
    return configuration_map


def CONFIGURATION_DISPLAY()-> dict:
    with open("configuration.psits_config", "r") as config:
        lines = config.readlines()
        
        for line in lines:
            print(line.strip())