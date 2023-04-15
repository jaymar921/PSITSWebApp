import hashlib
import warnings
import re, random
import os
import json
from decimal import Decimal
from datetime import datetime


ALLOWED_EXTENSIONS = set(['docx', 'pdf', 'doc', 'xls', 'txt'])


def hashData(data: str) -> str:
    result = hashlib.md5(data.encode()).hexdigest()
    return str(result)

def admins():
    return CONFIGURATION()['ADMINS']

def isAdmin(uid) -> bool:
    for key, value in admins().items():
        if str(value).__eq__(str(uid)):
            return True
    return False


def ifKeyPermitted(api_key) -> bool:
    for key, value in admins().items():
        if str("API_SECRET-"+hashData(str((int(value)*250)))).strip().__eq__(str(api_key).strip()):
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

def UpdatePriceParseRef(old_ref: str,price: str):
    return f"@REFP{price}-{old_ref}"


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
    with open("PSITSweb/configuration.psits_config", "r") as config:
        lines = config.readlines()
        settings = []
        
        dictionary_append = False
        dictionary_builder: dict = {}
        dictionary_title: str = ''
        for line in lines:
            if '::' in line:
                settings.append(line.strip())
            
            if '{' in line and '::' in line:
                dictionary_append = True
                dictionary_builder.clear()
                dictionary_title = line.replace('::','').replace('=','').replace('{','').replace('}','').replace('\n','').strip()
            if '}' in line and dictionary_append:
                dictionary_append = False
                configuration_map[dictionary_title] = dictionary_builder
                continue
            if dictionary_append:
                try:
                    key: str = line.split(':')[0].strip().replace('\'','').replace('"','')
                    val: str = line.split(':')[1].strip().replace(',','').replace('\'','').replace('"','')
                    if key and val:
                        dictionary_builder[key] = val
                except:
                    print('An error occured parsing '+line)
                continue
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
    with open("PSITSweb/configuration.psits_config", "r") as config:
        lines = config.readlines()
        
        for line in lines:
            print(line.strip())


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        # 👇️ if passed in object is instance of Decimal
        # convert it to a string
        if isinstance(obj, Decimal):
            return str(obj)
        # 👇️ otherwise use the default behavior
        return json.JSONEncoder.default(self, obj)

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)

def saveToFile(filename, data):
    with open(filename, "a+") as f:
        f.write(data)

def loadFileToDict(filename)->dict:
    configuration_map = {}
    with open(filename, "r") as config:
        lines = config.readlines()
        settings = []
    
    dictionary_append = False
    dictionary_builder: dict = {}
    dictionary_title: str = ''
    for line in lines:
        if '::' in line:
            settings.append(line.strip())

        if '{' in line and '::' in line:
            dictionary_append = True
            dictionary_builder.clear()
            dictionary_title = line.replace('::','').replace('=','').replace('{','').replace('}','').replace('\n','').strip()
        if '}' in line and dictionary_append:
            dictionary_append = False
            configuration_map[dictionary_title] = dictionary_builder
            continue
        if dictionary_append:
            try:
                key: str = line.split(':')[0].strip().replace('\'','').replace('"','')
                val: str = line.split(':')[1].strip().replace(',','').replace('\'','').replace('"','')
                if key and val:
                    dictionary_builder[key] = val
            except:
                print('An error occured parsing '+line)
            continue
        for setting in settings:
            try:
                option = setting.split(' = ')[1]
                if '_' == option:
                    option = ''
                configuration_map[setting.split(' = ')[0].replace(":","").replace("=","")] = option
            except Exception as e:
                configuration_map[setting.split(' = ')[0].replace(":","").replace("=","").strip()] = ''
    return configuration_map

# saveToFile('jaymar.txt','::admin = 1\n')
# saveToFile('jaymar.txt','::2nd = 2\n')
#print(loadFileToDict('jaymar.txt'))

# Iterative Binary Search Function
# It returns index of x in given array arr if present,
# else returns -1
def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0
 
    while low <= high:
 
        mid = (high + low) // 2
 
        # If x is greater, ignore left half
        if arr[mid] < x:
            low = mid + 1
 
        # If x is smaller, ignore right half
        elif arr[mid] > x:
            high = mid - 1
 
        # means x is present at mid
        else:
            return mid
 
    # If we reach here, then the element was not present
    return -1
 