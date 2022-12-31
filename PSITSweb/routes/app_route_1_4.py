from __main__ import app
from flask import render_template, session, redirect, url_for, request, json
from Database import getAccountByID
from Models import Account
from Util import isAdmin, hashData, directoryExist, createDir
from webApp_utility import save_redirection, checkImageExist, is_blocked_route, getListOfFiles, loadJSONFromFile, getFileDaysFromModified


@app.route('/PSITS/Administration')
def psits_admin_page():
    save_redirection('landing_page')
    if 'username' not in session:
        return redirect(url_for('cant_find_link'))
    if not isAdmin(session['username']):
        return render_template("404Page.html", logout="none", login="none",
                                   message="Sorry but this page is only for authorized personnel")
    return render_template(
        "app_templates_1_4/AdminPage.html",
        title="PSITS ADMIN",
        login="none",
        logout="block",
        account=session['username'],
        admin="block",
        account_data=getAccountByID(session['username'])
    )

@app.route('/PSITS@QuizAdmin')
def psits_admin_exam_page():
    save_redirection('landing_page')
    if 'username' not in session:
        return render_template("404Page.html", logout="none", login="none",
                                   message="Sorry but this page is only for authorized personnel")
    if not isAdmin(session['username']):
        return render_template("404Page.html", logout="none", login="none",
                                   message="Sorry but this page is only for authorized personnel")

    # Grab the Quiz Data
    QUIZ_DATA: list = []
    for quiz_data_file in getListOfFiles(app.config['UPLOAD_FOLDER']+'Quiz\\'):
        if '.json' not in quiz_data_file:
            continue
        quiz_json_data = loadJSONFromFile(app.config['UPLOAD_FOLDER']+f"Quiz\\{quiz_data_file}")
        QUIZ_DATA.append({'UID':hashData(quiz_json_data['QuizTopic']), 'Quiz': quiz_json_data})
    
    # makedr the quizzer data
    directory = app.config['UPLOAD_FOLDER']+f"\\Quiz\\Quizzer\\"
    if not directoryExist(directory):
        createDir(directory)
    
    QUIZZER: dict = {}
    for quiz_data_file in getListOfFiles(app.config['UPLOAD_FOLDER']+'Quiz\\Quizzer\\'):
        if '.json' not in quiz_data_file:
            continue
        quiz_json_data = loadJSONFromFile(app.config['UPLOAD_FOLDER']+f"Quiz\\Quizzer\\{quiz_data_file}")
        QuizID = quiz_json_data['quizID']
        if QuizID in QUIZZER:
            QUIZZER[QuizID] = QUIZZER[QuizID] + 1
        else:
            QUIZZER[QuizID] = 1
    return render_template(
        "app_templates_1_4/QuizAdmin.html",
        title="PSITS QUIZ ADMIN",
        login="none",
        logout="block",
        account=session['username'],
        admin="block",
        QUIZ_DATA=QUIZ_DATA,
        QUIZZER=QUIZZER,
        account_data=getAccountByID(session['username']),
        access_key = str("API_SECRET-"+hashData(str((int(session['username'])*250)))).strip()
    )


@app.route('/PSITS@QuizAdmin/Create')
def psits_admin_create_exam_page():
    save_redirection('psits_admin_create_exam_page')
    if 'username' not in session:
        return render_template("404Page.html", logout="none", login="none",
                                   message="Sorry but this page is only for authorized personnel")
    if not isAdmin(session['username']):
        return render_template("404Page.html", logout="none", login="none",
                                   message="Sorry but this page is only for authorized personnel")
    

    return render_template(
        "app_templates_1_4/QuizCreator.html",
        title="PSITS QUIZ CREATE",
        login="none",
        logout="block",
        account=session['username'],
        admin="block",
        account_data=getAccountByID(session['username']),
        access_key = str("API_SECRET-"+hashData(str((int(session['username'])*250)))).strip()
    )

@app.route('/PSITS@QuizAdmin/<uid>')
def psits_admin_view_exam_page(uid):
    if 'username' not in session:
        return render_template("404Page.html", logout="none", login="none",
                                   message="Sorry but this page is only for authorized personnel")
    if not isAdmin(session['username']):
        return render_template("404Page.html", logout="none", login="none",
                                   message="Sorry but this page is only for authorized personnel")
    # Grab the Quiz Data
    QUIZ_DATA = ''
    for quiz_data_file in getListOfFiles(app.config['UPLOAD_FOLDER']+'Quiz\\'):
        if '.json' not in quiz_data_file:
            continue
        quiz_json_data = loadJSONFromFile(app.config['UPLOAD_FOLDER']+f"Quiz\\{quiz_data_file}")
        if hashData(quiz_json_data['QuizTopic']) == str(uid):
            QUIZ_DATA = quiz_json_data
            break
    if not QUIZ_DATA:
        return redirect(url_for('cant_find_link'))

    return render_template(
        "app_templates_1_4/QuizCreator.html",
        title="PSITS QUIZ CREATE",
        login="none",
        logout="block",
        account=session['username'],
        admin="block",
        account_data=getAccountByID(session['username']),
        access_key = str("API_SECRET-"+hashData(str((int(session['username'])*250)))).strip(),
        data=json.dumps(QUIZ_DATA)
    )

@app.route('/PSITS/Quiz/<uid>')
def quiz_session(uid):
    save_redirection('quiz_session', uid)
    
    # Grab the Quiz Data
    QUIZ_DATA = ''
    for quiz_data_file in getListOfFiles(app.config['UPLOAD_FOLDER']+'Quiz\\'):
        if '.json' not in quiz_data_file:
            continue
        quiz_json_data = loadJSONFromFile(app.config['UPLOAD_FOLDER']+f"Quiz\\{quiz_data_file}")
        if hashData(quiz_json_data['QuizTopic']) == str(uid):
            QUIZ_DATA = quiz_json_data
            for quiz in QUIZ_DATA['Quiz']:
                quiz['QuizAnswer'] = hashData(quiz['QuizAnswer']+str(uid))
            break
    if not QUIZ_DATA:
        return redirect(url_for('cant_find_link'))
    QUIZ_DATA['QuizID'] = uid
    
    if 'username' not in session:
        return render_template(
            'app_templates_1_4/QuizSession.html',
            title=f'{str(quiz_json_data["QuizTopic"])} Quiz',
            login="block",
            logout="none",
            admin="none",
            QUIZ_DATA=json.dumps(QUIZ_DATA)
        )

    # Check if user already took the test
    try:
        result = loadJSONFromFile(app.config['UPLOAD_FOLDER']+f"Quiz\\Quizzer\\{session['username']}_{QUIZ_DATA['QuizTopic']}.json")
        result['RetakeDays'] = 15 - int(getFileDaysFromModified(app.config['UPLOAD_FOLDER']+f"Quiz\\Quizzer\\{session['username']}_{QUIZ_DATA['QuizTopic']}.json"))
    except:
        print(f'Student [{session["username"]}] viewed {QUIZ_DATA["QuizTopic"]} Quiz')
        result = ''
    return render_template(
        'app_templates_1_4/QuizSession.html',
        title=f'{str(quiz_json_data["QuizTopic"])} Quiz',
        login="none",
        logout="block",
        account=session['username'],
        admin="block",
        QUIZ_DATA=json.dumps(QUIZ_DATA),
        account_data=getAccountByID(session['username']),
        result = result
    )

@app.route('/PSITS@QuizAdmin/<uid>/Quizzers')
def psits_admin_view_exam_participants_page(uid):
    if 'username' not in session:
        return render_template("404Page.html", logout="none", login="none",
                                   message="Sorry but this page is only for authorized personnel")
    if not isAdmin(session['username']):
        return render_template("404Page.html", logout="none", login="none",
                                   message="Sorry but this page is only for authorized personnel")

    QUIZ_DATA = ''
    for quiz_data_file in getListOfFiles(app.config['UPLOAD_FOLDER']+'Quiz\\'):
        if '.json' not in quiz_data_file:
            continue
        quiz_json_data = loadJSONFromFile(app.config['UPLOAD_FOLDER']+f"Quiz\\{quiz_data_file}")
        if hashData(quiz_json_data['QuizTopic']) == str(uid):
            QUIZ_DATA = quiz_json_data
            break

    if not QUIZ_DATA:
        return redirect(url_for('cant_find_link'))

    QUIZZER: list = []
    for quiz_data_file in getListOfFiles(app.config['UPLOAD_FOLDER']+'Quiz\\Quizzer\\'):
        if '.json' not in quiz_data_file:
            continue
        quiz_json_data = loadJSONFromFile(app.config['UPLOAD_FOLDER']+f"Quiz\\Quizzer\\{quiz_data_file}")
        
        QuizID = quiz_json_data['quizID']
        if QuizID in str(uid):
            try:
                # get the user
                student_id = quiz_data_file.replace(f'_{QUIZ_DATA["QuizTopic"]}.json', '')
                student: Account = getAccountByID(int(student_id))
                quiz_json_data['IdNo'] = str(student_id)
                quiz_json_data['FullName'] = str(student.firstname) + " " + str(student.lastname)
                quiz_json_data['CourseYear'] = str(student.course) + " " + str(student.year)
                quiz_json_data['StudentPhoto'] = student.img
            except Exception as e:
                print(e)
                continue
            QUIZZER.append(quiz_json_data)
        

    return render_template(
        "app_templates_1_4/QuizParticipants.html",
        title="PSITS QUIZ ADMIN",
        login="none",
        logout="block",
        account=session['username'],
        admin="block",
        QUIZ_DATA=QUIZ_DATA,
        QUIZZER=QUIZZER,
        account_data=getAccountByID(session['username']),
        access_key = str("API_SECRET-"+hashData(str((int(session['username'])*250)))).strip()
    )


@app.route('/PSITS/PublicQuizzes')
def psits_admin_exam_topics():
    save_redirection('landing_page')
    

    # Grab the Quiz Data
    QUIZ_DATA: list = []
    for quiz_data_file in getListOfFiles(app.config['UPLOAD_FOLDER']+'Quiz\\'):
        if '.json' not in quiz_data_file:
            continue
        quiz_json_data = loadJSONFromFile(app.config['UPLOAD_FOLDER']+f"Quiz\\{quiz_data_file}")
        QUIZ_DATA.append({'UID':hashData(quiz_json_data['QuizTopic']), 'Quiz': quiz_json_data})
    
    # makedr the quizzer data
    directory = app.config['UPLOAD_FOLDER']+f"\\Quiz\\Quizzer\\"
    if not directoryExist(directory):
        createDir(directory)

    if 'username' not in session:
        return render_template(
            "app_templates_1_4/QuizTopics.html",
            title="PSITS QUIZZES",
            login="block",
            logout="none",
            QUIZ_DATA=QUIZ_DATA,
        )
    return render_template(
        "app_templates_1_4/QuizTopics.html",
        title="PSITS QUIZZES",
        login="none",
        logout="block",
        account=session['username'],
        admin="block",
        QUIZ_DATA=QUIZ_DATA,
        account_data=getAccountByID(session['username'])
    )