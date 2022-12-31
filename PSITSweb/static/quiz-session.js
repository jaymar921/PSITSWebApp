'use strict';
let data = document.getElementById('quiz-data').value;
data = JSON.parse(data);
let proceed_quiz = true;
let timer_cancel_id = 0;
let timeout_cancel_id = 0;
document.getElementById('quiz-data').remove();
const dataHolder = new Array();
let warning_shown = false;
const waring_sfx = document.getElementById('warning-sfx');

let session_time = 0;
let session_timer_cancel_id = 0;

function* QuestionsGenerator(){
    let i = 0;
    while(data.Quiz[i])
        yield data.Quiz[i++];
}

function cancelQuiz(){
    proceed_quiz = false;
}

const QuestionGenerator = QuestionsGenerator();

const modal_info = document.getElementById('modal-info');

let duration = 0;
data.Quiz.forEach(quiz => {
    duration+=quiz.QuestionTimer;
})
modal_info.innerHTML = `Topic: '${data.QuizTopic}'<br>Items: ${data.Quiz.length}<br>Mode: ${data.Quiz[0].QuestionTimer==-1? '(no time limit)': '(each question has a timer)'}<br>Duration: ${duration}s`;

const modal_instruction = document.getElementById('instruction-info');
modal_instruction.innerHTML = `
    You will be taking a quiz about ${data.QuizTopic}, there will be ${data.Quiz.length} items ${data.Quiz[0].QuestionTimer==-1? 'with no time limit. ': 'and each questions will have a timer. '}
    Don't worry, it will be fun 😊 once you're ready, you can click the start button.<br><br><a style='color: #FF0000;font-weight:900;'>Note: There will be no 'back' button once you answered a question.</a>
    `;

function stopTimer(){
    clearInterval(timer_cancel_id);
    clearTimeout(timeout_cancel_id);
}

function StartSessionTimer(){
    session_timer_cancel_id = setInterval(()=>{
        session_time++;
        if (!document.hasFocus()){
            if(!warning_shown){
                FadeInElement(document.getElementById('warning-modal'));
                waring_sfx.play();
                waring_sfx.volume = 0.2;
                warning_shown = true;
            }else{
                waring_sfx.play();
            }
        }
    }, 1000);
}

function CloseWarning(){
    openFullscreen();
    FadeOutElement(document.getElementById('warning-modal'));
    warning_shown=false;
    waring_sfx.pause();
}

function GetSessionTime(){
    clearInterval(session_timer_cancel_id);
    return session_time;
}

function runTimer(time, callback){
    let i = 100;
    function move() {
        if (i == 100) {
            i = 0;
            let elem = document.getElementById("myBar");
            let width = 100;
            timer_cancel_id = setInterval(frame, time*10);
            function frame() {
            if (width == 0) {
                clearInterval(timer_cancel_id);
                i = 100;
            } else {
                width--;
                elem.style.width = width + "%";
                if(width > 60){
                    elem.style.backgroundColor = 'green';
                }else if(width > 30){
                    elem.style.backgroundColor = 'rgb(204, 101, 6)';
                }else{
                    elem.style.backgroundColor = 'rgb(251, 16, 16)';
                }
            }
            }
        }
    }
    move();
    timeout_cancel_id = setTimeout(()=>{callback()}, 1000*time);
}

function delay(time) {
    return new Promise(resolve => setTimeout(resolve, time));
}
function playMusic(){
    var music = document.getElementById('quiz-music');
    music.play();
    music.volume = 0.5;
    setInterval(playMusic, 122000);
}

async function proceed(){
    FadeOutElement(document.getElementById('welcome-modal'))
    for(let i = -50; i > -230; i-=1){
        document.getElementById('welcome-modal').style.transform = `translate(${i}%,-50%)`
        await delay(2);
    }
    document.getElementById('welcome-modal').style.display = 'none';
    if(!proceed_quiz)
        return;
    document.getElementById('instruction-modal').style.display = 'block';
    for(let i = 0.0; i < 1; i+=0.05){
        document.getElementById('instruction-modal').style.opacity = i;
        await delay(50);
    }
}

async function gameStart(){
    openFullscreen();
    FadeOutElement(document.getElementById('instruction-modal'))
    
    document.getElementById('quiz-session').style.display = 'block';
    document.getElementById('instruction-modal').style.display = 'none';
    loadQuestion();
    StartSessionTimer();
}


function loadQuestion(){
    const Quiz = QuestionGenerator.next().value;
    if(!Quiz){
        EndQuiz();
        return;
    }
    const QUESTION_ELEMENT = document.getElementById('question');
    const CODEBLOCK_ELEMENT = document.getElementById('code-block');
    SpanCodeBlock(Quiz.QuizQuestion, QUESTION_ELEMENT, CODEBLOCK_ELEMENT);
    const ANSWER_DIV = document.getElementById('option-group');
    for(let index = 0; index <= 100; index++){
        const childNode = document.getElementById(`div_child${index}`);
        if(childNode){
            ANSWER_DIV.removeChild(childNode);
        }
    }
    const childNode = document.getElementById(`div_child`);
    if(childNode){
        ANSWER_DIV.removeChild(childNode);
    }

    if(Quiz.Type === 'MULTIPLE'){
        
        let id = 0;
        for(const OPTION of Quiz.QuizAnswers){
            const OPTION_ELEMENT = document.createElement('input');
            OPTION_ELEMENT.name = 'option';
            OPTION_ELEMENT.type = 'radio'
            OPTION_ELEMENT.id = `option${id}`;
            OPTION_ELEMENT.value = OPTION;

            const OPTION_LABEL_ELEMENT = document.createElement('label');
            OPTION_LABEL_ELEMENT.innerHTML = OPTION;
            OPTION_LABEL_ELEMENT.htmlFor = `option${id}`;
            OPTION_LABEL_ELEMENT.style.paddingLeft = '10px';

            const GROUP = document.createElement('div');
            GROUP.classList.add('option-div');
            GROUP.id = `div_child${id}`;
            GROUP.appendChild(OPTION_ELEMENT);
            GROUP.appendChild(OPTION_LABEL_ELEMENT);

            ANSWER_DIV.appendChild(GROUP);
            id++;
        }
    }else if(Quiz.Type === 'SHORTANSWER'){
        const ANSWER_ELEMENT = document.createElement('input');
        ANSWER_ELEMENT.type = 'text';
        ANSWER_ELEMENT.id = `answer`;
        ANSWER_ELEMENT.style.width = '100%';
        ANSWER_ELEMENT.style.padding = '3px';
        ANSWER_ELEMENT.style.textAlign = 'center';
        ANSWER_ELEMENT.placeholder = 'Answer...';

        const GROUP = document.createElement('div');
        GROUP.classList.add('option-div');
        GROUP.id = `div_child`;
        GROUP.appendChild(ANSWER_ELEMENT);
    
        ANSWER_DIV.appendChild(GROUP);
    }
    if(Quiz.QuestionTimer != -1){
        runTimer(Quiz.QuestionTimer, nextQuestion)
    }
}

function nextQuestion(){
    let answer = '';
    if(document.querySelector('input[name="option"]:checked')){
        answer = document.querySelector('input[name="option"]:checked').value;
    }
    if(!answer){
        if(document.getElementById('answer'))
            answer = document.getElementById('answer').value;
    };
    if(!answer){
        answer = '';
    }
    dataHolder.push(answer);
    stopTimer();
    loadQuestion();
}

async function EndQuiz(){
    closeFullscreen();
    stopTimer();
    const UserSessionTime = GetSessionTime();
    await FadeOutElement(document.getElementById('quiz-session'));
    FadeInElement(document.getElementById('endgame-modal'));
    document.getElementById('endgame-header').innerHTML =
    `Yay you did it!`;
    document.getElementById('endgame-info').innerHTML =
    `Please wait while the server is processing...`;
    const proceed_btn = document.getElementById('endgame-btn');
    proceed_btn.innerHTML = 'Processing';
    proceed_btn.removeEventListener("click", gameStart);
    document.getElementById('endgame-info-last').innerHTML = 'I hope you found it fun 😎';
    proceed_btn.addEventListener('click', EndQuiz);
    const ANSWERS = {
        'Quizzer': document.getElementById('quizzer-id').value,
        'Answers': JSON.stringify(dataHolder),
        'SessionTime': UserSessionTime
    }
    setTimeout(()=>{
        fetch(`/PSITS/api/quiz/record?quizId=${data.QuizID}`, {
            method: `POST`,
            headers: {"Content-type": "application/json; charset=UTF-8"},
            body: JSON.stringify(ANSWERS)
        })
        .then(r => r.json())
        .then(async r => {
            await FadeOutElement(document.getElementById('endgame-modal'))
            ShowScore(r);
        });
    }, 5000);
    
}

function ShowScore({score, sessionTime}, overall = 0){
    score = Number.parseInt(score);
    document.getElementById('welcome-modal').style.display = 'none';

    if(overall == 0)
        overall = dataHolder.length;
    if((score/overall) >= 0.7){
        var sfx = document.getElementById('yay-sfx');
        sfx.play();
        sfx.volume = 0.5;
    }
    FadeInElement(document.getElementById('result-modal'));
    document.getElementById('result-info').innerHTML =
    `You scored ${score} out of ${overall} on this quiz. <br>Session Time: ${sessionTime}s`
    document.getElementById('result-btn').innerHTML = `${score}/${overall}`
    document.getElementById('result-info-last').innerHTML = `This quiz is recorded in the server's database`
}

function SpanCodeBlock(TEXT, OUTPUT_ELEMENT, CODEBLOCK_ELEMENT){
    const FRAGMENT_TEXT = TEXT.split('\n');
    let isCodeBlock = false;
    let code_block = ``;
    let text = ``;
    
    for(let child of OUTPUT_ELEMENT.childNodes){
        OUTPUT_ELEMENT.removeChild(child)
    }
    for(let child of CODEBLOCK_ELEMENT.childNodes){
        CODEBLOCK_ELEMENT.removeChild(child)
    }
    for(const FT of FRAGMENT_TEXT){
        if((FT.includes('```') || FT === '```') && !isCodeBlock){
            isCodeBlock = true;
            continue;
        }
        if((FT.includes('```') || FT === '```') && isCodeBlock){
            isCodeBlock = false;
            continue;
        }
        
        if(isCodeBlock){
            code_block += FT + "\n";
        }else{
            text += FT + "\n";
            OUTPUT_ELEMENT.innerHTML = text;
        }
    }
    if(code_block){
        const OUTPUT_CHILD_NODE = document.createElement('span');
        OUTPUT_CHILD_NODE.innerHTML = code_block;
        OUTPUT_CHILD_NODE.classList.add('unselectable');
        OUTPUT_CHILD_NODE.classList.add('code-block');
        CODEBLOCK_ELEMENT.appendChild(OUTPUT_CHILD_NODE);
    }
}

async function FadeOutElement(e){
    e.style.opacity = 1;
    for(let i = 1.0; i > 0; i-=0.05){
        e.style.opacity = i;
        await delay(50);
    }
    e.style.display = 'none';
}

async function FadeInElement(e){
    e.style.opacity = 0;
    e.style.display = 'block';
    for(let i = 0; i <= 1 ; i+=0.05){
        e.style.opacity = i;
        await delay(50);
    }
}