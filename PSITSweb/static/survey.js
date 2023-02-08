// Script created by Jayharron Mar Abejar

const question_holder = document.getElementById('survey_content');
let question_id = 1;
let lastQuestion = 0;
let Survey = null;
let SurveyAnswers = null;

function addQuestion(){
    const qId = question_id;

    let survey_content = document.createElement('div');
    survey_content.classList.add('survey_content');
    survey_content.id = "QUESTION_"+qId;

    let survey_input_1 = document.createElement('div');
    survey_input_1.classList.add('survey_inputs');
    let label_question = document.createElement('label');
    let question = document.createElement('input');
    question.id = qId + "_question";
    question.type = "text";
    question.placeholder = "Question";
    label_question.innerHTML = "Question: ";
    label_question.appendChild(question);
    survey_input_1.appendChild(label_question);

    let survey_input_2 = document.createElement('div');
    survey_input_2.classList.add('survey_inputs');
    let label_option = document.createElement('label');
    let option = document.createElement('input');
    option.id = qId + "_option";
    option.type = "text";
    option.placeholder = "Option1, Option2, Option3";
    label_option.innerHTML = "Option: ";
    label_option.appendChild(option);
    survey_input_2.appendChild(label_option);

    let survey_input_3 = document.createElement('div');
    survey_input_3.classList.add('survey_inputs');
    let button_remove = document.createElement('button');
    button_remove.innerHTML = "Remove Question";
    button_remove.addEventListener('click', (e) => {
        document.getElementById("QUESTION_"+qId).remove();
    })

    survey_input_3.appendChild(button_remove);

    survey_content.appendChild(survey_input_1);
    survey_content.appendChild(survey_input_2);
    survey_content.appendChild(survey_input_3);

    document.getElementById('survey_content').appendChild(survey_content);
    
    question_id++;
}

function saveQuestion(){
    const allowAnonymous = document.getElementById('allowAnonymous').checked;
    const surveyTitle = document.getElementById('surveyTitle').value;
    const surveyDescription = document.getElementById('surveyDescription').value;
    const surveyQuestions = new Array();

    for(let index = 1; index <= question_id; index++){
        try{
            surveyQuestions.push({
                "Question" : document.getElementById(`${index}_question`).value,
                "Option": document.getElementById(`${index}_option`).value,
                "QuestionNumber" : index
            });
        }catch(error){}
    };
    
    const SurveyObj = {
        allowAnonymous,
        surveyTitle,
        surveyDescription,
        surveyQuestions
    }
    fetch(`/PSITS/api/survey`,{
        method: 'POST',
        body: JSON.stringify({"Survey":SurveyObj}),
        headers: {"Content-type": "application/json; charset=UTF-8"}
    }).then(r => {
        window.location = '/PSITS@Survey'
    }).catch(e => {
        
    });
}

async function loadSurvey(surveyObj){
    const SurveyObject = JSON.parse(surveyObj)
    
    document.getElementById('title').innerHTML = SurveyObject.surveyTitle;
    document.getElementById('question').innerHTML = SurveyObject.surveyDescription;
    lastQuestion = SurveyObject.surveyQuestions.length;
    question_id = 0;
    Survey = SurveyObject;
    SurveyAnswers = new Array();
    document.getElementById('session-button').hidden = false;
}

async function nextQuestion(){
    if(lastQuestion == 0 && Survey == null){
        return;
    }

    if(question_id < 0){
        return;
    }
    if(question_id != 0 && question_id != lastQuestion+1){
        document.getElementById('survey_session').classList.add('hidden');
        SaveResult();
    }
    if(question_id == lastQuestion){

        fetch(`/PSITS/api/survey_response`,{
            method: 'POST',
            body: JSON.stringify({"Survey":{
                "SurveyTitle":Survey.surveyTitle,
                SurveyAnswers,
                "User":document.getElementById('user').value
            }}),
            headers: {"Content-type": "application/json; charset=UTF-8"}
        }).then(r => {
            setTimeout(()=>{
                document.getElementById('survey_session').classList.remove('hidden');
                document.getElementById('title').innerHTML = "Form was submitted!";
                document.getElementById('question').innerHTML = "Your response has been sent, thank you for your spare time! You may close this tab now.";
                document.getElementById('answer').hidden = true;
                document.getElementById('answer-selection').hidden = true;
                document.getElementById('session-button').hidden = true;
                setTimeout(()=>{window.location = '/PSITS'},5000);
            }, 1000);
            
        }).catch(e => {
            
        });
        
        
        return;
    }
    
    document.getElementById('survey_session').classList.add('hidden');
    await setTimeout(()=>{
        document.getElementById('session-button').innerHTML = (question_id==lastQuestion-1)?"Submit":"Next";
        loadQuestion(question_id++, false);
        
    }, 500);
    
    
}

async function backQuestion(){
    
    if(lastQuestion == 0 && Survey == null)
        return;
    SaveResult();
    --question_id;
    if(question_id < 0){
        console.log(question_id)
        question_id = 0;
        return;
    }
    
    document.getElementById('survey_session').classList.add('hidden');
    await setTimeout(()=>{
        document.getElementById('session-button').innerHTML = (question_id==lastQuestion)?"Submit":"Next";
        

        console.log('position prev',question_id)
        loadQuestion(question_id, true);
        
    }, 500);
    
}


function loadQuestion(question_id, back=false){
    document.getElementById('survey_session').classList.remove('hidden');
    document.getElementById('title').innerHTML = "";
    document.getElementById('question').innerHTML = Survey.surveyQuestions[question_id].Question;
    document.getElementById('answer').hidden = Survey.surveyQuestions[question_id].Option?true:false;
    
    document.getElementById('answer-selection').hidden = Survey.surveyQuestions[question_id].Option?false:true;
    if(Survey.surveyQuestions[question_id].Option){
        document.getElementById('answer-selection').innerHTML = "";
        for(let option of Survey.surveyQuestions[question_id].Option.split(",")){
            let _surveyOption = document.createElement('option');
            _surveyOption.value = option.trim();
            _surveyOption.innerHTML = option.trim();
            document.getElementById('answer-selection').appendChild(_surveyOption);
        }
    }
    document.getElementById('answer').value = back?(SurveyAnswers[question_id]?SurveyAnswers[question_id]:""): "";
}


function SaveResult(){
    SurveyAnswers[question_id-1] = document.getElementById('answer').value!=""?document.getElementById('answer').value:Survey.surveyQuestions[question_id-1].Option?document.getElementById('answer-selection').value:"";
}