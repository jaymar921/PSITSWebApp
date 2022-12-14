from __main__ import app
import os

from flask import request, redirect, url_for, session, render_template
import json
import threading, time
import pandas as pd
import datetime


from Database import updateAnnouncement, SEARCHMerchOrder, SEARCHMerchandise, getAccountByID, UPDATEMerchOrder, getAccount, DELETEMerchOrder, updateAccount, databaseLog, GETAllMerchandise\
    ,getAllAccounts, getAccountWithPassword, GetAllPromo, getAnnouncement
# from EmailAPI import pushEmail
from Models import Quiz, Questionaires, Announcement
from Util import GetReference, isAdmin, ifKeyPermitted, hashData, GetPriceRef, contentVerifier,directoryExist, createDir
from webApp_utility import save_redirection, is_blocked_route, checkImageExist, renameFile, saveToFile, loadJSONFromFile, getListOfFiles, deleteFile


@app.route('/PSITS/api/announcement', methods=['PUT'])
def api_update_announcement():
    request_key = request.args.get('key')

    if not request_key:
        databaseLog(
            f'API[PUT] - Remote {request.remote_addr} - Tried to update announcement with no key')
        return {
            "status": 403,
            "message": "ACCESS DENIED: key must be provided at query string."
        }

    if not ifKeyPermitted(request_key):
        databaseLog(
            f'API[PUT] - Remote {request.remote_addr} - Tried to update announcement with invalid key')
        return {
            "status": 403,
            "message": f"ACCESS DENIED: invalid key -- {request_key}"
        }

    try:
        uid = request.get_json()['uid']
        title = request.get_json()['title']
        content = request.get_json()['content']
        user = request.get_json()['user']
        content = f"""{content.strip()} 

Updated by: {user} ({datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
            """

        # Before we update the announcements, we should also link the images
        # from the old announcement title
        announcement_old: Announcement = getAnnouncement(uid)
        print(announcement_old.title)
        # Load the Photos if exist
        if checkImageExist(str(announcement_old.uid) + announcement_old.title + ".jpg"):
            renameFile(f"{str(announcement_old.uid) + announcement_old.title}.jpg", f"{str(announcement_old.uid) + title}.jpg")
        if checkImageExist(str(announcement_old.uid) + announcement_old.title + ".png"):
            renameFile(f"{str(announcement_old.uid) + announcement_old.title}.png", f"{str(announcement_old.uid) + title}.png")
        for num in range(1,100):
            if checkImageExist(f"{str(announcement_old.uid) + announcement_old.title + str(num)}.png"):
                renameFile(f"{str(announcement_old.uid) + announcement_old.title + str(num)}.png", f"{str(announcement_old.uid) + title + str(num)}.png")
        for num in range(1,100):
            if checkImageExist(f"{str(announcement_old.uid) + announcement_old.title + str(num)}.jpg"):
                renameFile(f"{str(announcement_old.uid) + announcement_old.title + str(num)}.jpg", f"{str(announcement_old.uid) + title + str(num)}.jpg")
        updateAnnouncement(uid, title,datetime.datetime.now().strftime("%Y-%m-%d"),contentVerifier(content))
        databaseLog(f'API[PUT] - Remote {request.remote_addr} - Announcement [{title}] was updated by {user}')
    except Exception as e:
        print(e)
        return {
            "status": 500,
            "message": f"The server does not understand the request content provided"
        }
    
    response = app.response_class(
        response=json.dumps({"status":204}, indent=4,
                            sort_keys=False, default=str),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/PSITS/api/quiz', methods=['POST', 'PUT', 'DELETE'])
def psits_api_quiz_edit():
    """{
            QuizTopic: '',
            Quiz: [
                {
                    QuizID: 0,
                    QuizQuestion:"",
                    QuizAnswers:[],
                    QuizAnswer:'',
                    QuestionTimer:-1,
                    Type:'' 
                }
            ],
            QuizOwner: '',
            CreationDate: MM/DD/YYYY,
            CreationTime: HH:MM:SS
        }
    """
    request_key = request.args.get('key')

    if not request_key:
        databaseLog(
            f'API[POST/PUT] - Remote {request.remote_addr} - Tried to access quiz data with no key')
        return {
            "status": 403,
            "message": "ACCESS DENIED: key must be provided at query string."
        }

    if not ifKeyPermitted(request_key):
        databaseLog(
            f'API[POST/PUT] - Remote {request.remote_addr} - Tried to access quiz data with invalid key')
        return {
            "status": 403,
            "message": f"ACCESS DENIED: invalid key -- {request_key}"
        }
    
    if request.method.lower() == 'delete':
        try:
            topic = request.get_json()['QuizTopic']
            deleteFile(app.config['UPLOAD_FOLDER']+f"Quiz\\Quiz_{topic}.json")
        except Exception as e:
            print(f'Error: {e}')
            return {
                "status": 500,
                "message": f"The server does not understand the request content provided"
            }
    else:
        try:
            topic = request.get_json()['QuizTopic']
            quiz = request.get_json()['Quiz']
            quizOwner = request.get_json()['QuizOwner']
            creationDate = request.get_json()['CreationDate']
            creationTime = request.get_json()['CreationTime']
            try:
                showProfile = request.get_json()['ShowProfile']
            except:
                showProfile = 'no'

            questionaires: list = []
            for item in quiz:
                questionaire = Questionaires(
                    item['QuizID'],
                    item['QuizQuestion'],
                    item['QuizAnswers'],
                    item['QuizAnswer'],
                    item['QuestionTimer'],
                    item['Type']
                )
                questionaires.append(questionaire)
            
            quiz_obj: Quiz = Quiz(topic, questionaires, quizOwner, creationDate, creationTime)
            quiz_obj.ShowProfile = 'yes' if showProfile else 'no'
            data = json.dumps(quiz_obj.toJSON(), indent=4,
                                sort_keys=False, default=str)

            directory = app.config['UPLOAD_FOLDER']+f"\\Quiz\\"
            if not directoryExist(directory):
                createDir(directory)
            saveToFile(app.config['UPLOAD_FOLDER']+f"Quiz\\Quiz_{topic}.json",data)
        
        except Exception as e:
            print(f'error: {e}')
            return {
                "status": 500,
                "message": f"The server does not understand the request content provided"
            }

    
    response = app.response_class(
        response=json.dumps({"status":204}, indent=4,
                            sort_keys=False, default=str),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/PSITS/api/quiz/record', methods=['POST'])
def psits_api_quiz_record():
    quiz_id = request.args.get('quizId')

    if not quiz_id:
        databaseLog(
            f'API[POST/PUT] - Remote {request.remote_addr} - Tried to access quiz record with no quiz id')
        return {
            "status": 403,
            "message": "ACCESS DENIED: quiz id must be provided at query string."
        }
    try:
        quizzer = request.get_json()['Quizzer']
        answers = request.get_json()['Answers']
        sessionTime = request.get_json()['SessionTime']
        answers = json.loads(answers)
        # Grab the Quiz Data
        QUIZ_DATA = ''
        for quiz_data_file in getListOfFiles(app.config['UPLOAD_FOLDER']+'Quiz\\'):
            if '.json' not in quiz_data_file:
                continue
            quiz_json_data = loadJSONFromFile(app.config['UPLOAD_FOLDER']+f"Quiz\\{quiz_data_file}")
            if hashData(quiz_json_data['QuizTopic']).lower() == str(quiz_id).lower():
                QUIZ_DATA = quiz_json_data
                break
        
        # count the score
        score = 0
        for index in range(0, len(QUIZ_DATA['Quiz'])):
            quiz = QUIZ_DATA['Quiz'][index]
            answer = answers[index]
            if str(quiz['QuizAnswer']) == str(answer):
                score = score + 1

        saveToFile(app.config['UPLOAD_FOLDER']+f"\\Quiz\\Quizzer\\{quizzer}_{QUIZ_DATA['QuizTopic']}.json", 
            json.dumps({
                "quizID": quiz_id,
                "score": score,
                "sessionTime": sessionTime,
                "answers": answers
            }, indent=4, sort_keys=False, default=str))
        
        databaseLog(
            f'API[POST/PUT] - Remote {request.remote_addr} - Student {getAccountByID(quizzer).lastname} took {QUIZ_DATA["QuizTopic"]} quiz: [{score}/{len(answers)}]')

        return {
            "status": 200,
            "message": f"Score Recorded",
            "score": score,
            "sessionTime": sessionTime
        }
    except Exception as e:
        #print(e)
        print('error')
        return {
            "status": 500,
            "message": f"The server does not understand the request content provided"
        }


@app.route('/PSITS/api/quiz', methods=['GET'])
def psits_api_quiz_get():
    student_id = request.args.get('studentId')

    if not student_id:
        databaseLog(
            f'API[POST/PUT] - Remote {request.remote_addr} - Tried to access quiz records with no student id')
        return {
            "status": 403,
            "message": "ACCESS DENIED: studentId must be provided at query string."
        }
    try:
       
        # Grab the Quiz Data
        QUIZZER: list = []
        for quiz_data_file in getListOfFiles(app.config['UPLOAD_FOLDER']+'Quiz\\'):
            if '.json' not in quiz_data_file:
                continue
            quiz_json_data = loadJSONFromFile(app.config['UPLOAD_FOLDER']+f"Quiz\\{quiz_data_file}")
            QUIZ_DATA = quiz_json_data

            try:
                student_json_data = loadJSONFromFile(app.config['UPLOAD_FOLDER']+f"Quiz\\Quizzer\\{student_id}_{QUIZ_DATA['QuizTopic']}.json")
                # get the user
                student = getAccountByID(int(student_id))
                student_json_data['FullName'] = str(student.firstname) + " " + str(student.lastname)
                student_json_data['QuizTopic'] = QUIZ_DATA['QuizTopic']
            except Exception as e:
                continue
            if 'yes' in QUIZ_DATA['ShowProfile']:
                QUIZZER.append({
                    "QuizID": student_json_data['quizID'],
                    "QuizTopic": QUIZ_DATA['QuizTopic'],
                    "FullName": student_json_data['FullName'],
                    "Score": student_json_data['score'],
                    "TotalScore": len(QUIZ_DATA['Quiz']),
                })
        

        return {
            "status": 200,
            "message": "Retrieved Data",
            "UserData": QUIZZER
        }
    except Exception as e:
        print(e)
        print('error')
        return {
            "status": 500,
            "message": f"The server does not understand the request content provided"
        }
