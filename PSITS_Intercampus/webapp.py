from flask import Flask, render_template, request, redirect, url_for, session
from mysql import connector
import hashlib

# DUE TO LACK TO TIME, I MADE IT A SINGLE FILE
app = Flask(__name__)
app.secret_key = 'PSITS2023BYABEJAR'

# database manipulation
db_name = 'psitswebapp'
db_username = 'root'
db_password = ''
db_host = '127.0.0.1'

temp_data = []

@app.route('/')
def loginPage():
    if 'username' in session:
        return redirect(url_for('adminHome'))
    return render_template('index.html') 


@app.route('/login/<uid>')
def loginPage_(uid):
    if uid in temp_data:
        session['username'] = uid
        temp_data.remove(uid)
        return redirect(url_for('adminHome'))
    return redirect(url_for('loginPage'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('loginPage'))

@app.route('/admin')
def adminHome():
    if 'username' not in session:
        return redirect(url_for('loginPage'))
    return render_template('home.html', data=session['data'])


# PSITS API
@app.route('/api/getacc', methods=['GET'])
def api_getAcc():
    global temp_data
    try:
        idnum = request.headers.get('idno')
        pasw = request.headers.get('pass')
        if getUserAdmin(int(idnum), hashData(pasw)):
            temp_data.append(hashData(pasw+ str(idnum)))
            return {"status":"ok", "message":"permitted","access_key":hashData(pasw+ str(idnum))}
        return {"status":"access-denied", "message":"denied"}
    except Exception as e:
        return {"status":"error", "message":str(e)}
    

@app.route('/api/getalladmins')
def api_getAllAdmins():
    if 'username' not in session:
        return {"admins": [], "message":"access-denied"}
    admins: dict = getAllAdmins()
    
    return {"admins":admins}

@app.route('/api/events', methods=['POST', 'GET', 'DELETE'])
def api_events():
    if 'username' not in session:
        return {"message":"access-denied"}
    
    if request.method.lower() == 'get':
        return {"message":"success", "events":executeQueryReturn('SELECT * FROM `psits_intercampus_events`')}
    elif request.method.lower() == 'delete':
        try:
            eventID = request.headers.get('eventId')
            executeQueryCommit(f'DELETE FROM `psits_intercampus_events` where id={eventID}')
            return {"message":"success"}
        except:
            return {"message":"error"}
        
    event_data: dict = request.json
    addRegisterEvent(event_data)
    return {"message":"success", "inserted_data":event_data}


@app.route('/api/registry', methods=['POST', 'GET'])
def api_registry():
    if 'username' not in session:
        return {"message":"access-denied"}
    if request.method.lower() == 'get':
        h_ = request.headers.get('eventId')
        eventID = h_ if h_ is not None else 0
        return {"message":"success", "data":executeQueryReturn(f'SELECT * FROM psits_intercampus_registry where event_id={eventID}')}
    registry_data: dict = request.json
    if len(executeQueryReturn(f'SELECT * FROM `psits_intercampus_admin` where idno={registry_data["idno"]}')) == 0:
        # CREATE THE ACCOUNT IF NOT FOUND
        user: dict = {
            "idno": registry_data['idno'],
            "firstname": registry_data['firstname'].upper(),
            "lastname": registry_data['lastname'].upper(),
            "course": '',
            "year": '',
            "campus": registry_data['campus'],
            "email": registry_data['email'],
            "password": '',
            "isadmin": 'FALSE',
        }
        registerUser(user)

    
    if(len(executeQueryReturn(f'SELECT * FROM `psits_intercampus_events` where id={registry_data["eventID"]}'))==0):
        return {"message":"failed, eventID not found"}
    
    USER_DATA = executeQueryReturn(f'SELECT * FROM `psits_intercampus_admin` where idno={registry_data["idno"]}')[0]
    EVENT_DATA = executeQueryReturn(f'SELECT * FROM `psits_intercampus_events` where id={registry_data["eventID"]}')[0]

    print(USER_DATA)
    print(registry_data)
    query: str = f"""
        INSERT INTO psits_intercampus_registry(
            `idno`,  
            `event_id`,
            `payment`,
            `shirt_size`,
            `attended`,
            `claimed`,
            `meta_data`
        )
        values (
            {registry_data['idno']},
            {registry_data['eventID']},
            "{registry_data['payment']}",
            "{registry_data['shirtsize']}",
            "FALSE",
            "FALSE",
            "{USER_DATA['lastname']}, {USER_DATA['firstname']}|{EVENT_DATA['event_name']}|{USER_DATA['campus']}"
        )
    """
    executeQueryCommit(query)

    return {"message":"success"}



# MYSQL DATABASE

def ConnectDB():
    return connector.connect(
        host=db_host,
        user=db_username,
        password=db_password,
        database=db_name
    )

def executeQueryReturn(query: str) -> dict:
    db = ConnectDB()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query)
    data: dict = cursor.fetchall()
    cursor.close()
    db.close()
    return data


def executeQueryReturnParam(query: str, param: tuple):
    db = ConnectDB()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, param)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data


def executeQueryCommit(query: str):
    db = ConnectDB()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query)
    db.commit()
    cursor.close()
    db.close()
    return None

def getUserAdmin(uid, password):
    query: str = 'SELECT * FROM `psits_intercampus_admin` where idno=%s and password=%s'
    data: dict = executeQueryReturnParam(query, (uid, password))
    if len(data) > 0:
        if str(data[0]['isadmin']).lower() == 'true':
            session['data'] = data[0]
            return True
    return False

def getAllAdmins():
    query: str = 'SELECT * FROM `psits_intercampus_admin` where isadmin="TRUE"'
    return executeQueryReturn(query)

def getUsersAdmin():
    query: str = 'SELECT * FROM `psits_intercampus_admin` where isadmin="TRUE"'
    data: dict = executeQueryReturn(query)
    users: list = []
    if len(data) > 0:
        for u in data:
            users.append(u)
    return users

def addRegisterEvent(event: dict):
    query: str = 'INSERT INTO `psits_intercampus_events`(`event_name`, `venue`, `attendees`, `host`, `registration_price`, `tshirt_price`, `deleted`) '
    values: str = f'values ("{event["eventName"]}","{event["venue"]}","{event["attendees"]}","{event["host"]}",{event["regFee"]},{event["shirt"]},"FALSE");'
    executeQueryCommit(query=query+values)

def registerUser(user: dict):
    query: str = 'INSERT INTO `psits_intercampus_admin`(`idno`,`firstname`,`lastname`,`course`,`year`,`campus`,`email`,`password`,`isadmin`)'
    values: str = f'values ("{user["idno"]}","{user["firstname"]}","{user["lastname"]}","{user["course"]}","{user["year"]}","{user["campus"]}","{user["email"]}","{user["password"]}","{user["isadmin"]}");'
    executeQueryCommit(query=query+values)

def hashData(data: str) -> str:
    result = hashlib.md5(data.encode()).hexdigest()
    return str(result)

# Avoid going back after logout
@app.after_request
def after_request(response):
    response.headers.add('Cache-Control', 'no-store,no-cache,must-revalidate,post-check=0,pre-check=0')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)