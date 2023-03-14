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


@app.route('/api/getacc', methods=['GET'])
def getAcc():
    global temp_data
    try:
        idnum = request.headers.get('idno')
        pasw = request.headers.get('pass')
        print(idnum)
        if getUserAdmin(int(idnum), hashData(pasw)):
            temp_data.append(hashData(pasw+ str(idnum)))
            return {"status":"ok", "message":"permitted","access_key":hashData(pasw+ str(idnum))}
        return {"status":"access-denied", "message":"denied"}
    except Exception as e:
        return {"status":"error", "message":str(e)}

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

def getUsersAdmin():
    query: str = 'SELECT * FROM `psits_intercampus_admin` where isadmin="TRUE"'
    data: dict = executeQueryReturn(query)
    users: list = []
    if len(data) > 0:
        for u in data:
            users.append(u)
    return users


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