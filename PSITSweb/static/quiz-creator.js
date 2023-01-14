'use strict';
// attributes
let title_input = document.getElementById('quiz-title');
let title_output = document.getElementById('output-quiz-title');
let questions_create =  document.getElementById('output-quiz-questions-create');
let questions_output =  document.getElementById('output-quiz-questions');
let data = []
let incremented_indicator = 0;

const BREAKLINE = document.createElement('p');
BREAKLINE.innerHTML = '<br>&nbsp;';

// Listener for the title
title_input.addEventListener('input', (e) => {
    if(e.target.value != ''){
        title_output.innerHTML = e.target.value;
    }else{
        title_output.innerHTML = 'Quiz Preview';
    }
});

function QuizLoader(JSON_DATA){
   const DATA = JSON.parse(JSON_DATA);
   // set the title
   title_input.value = DATA.QuizTopic;
   title_output.innerHTML = DATA.QuizTopic;

   // load if there is a timer
   if(DATA.Quiz.length > 0){
        if(DATA.Quiz[0].QuestionTimer != -1){
            document.getElementById('quiz-type').value = 'timed';
        }
   }
   for(let Quiz of DATA.Quiz){
        const ENTRY = {
            ...Quiz
        }
        if(ENTRY.Type === 'MULTIPLE')
            addNewMultipleChoiceQuestion(ENTRY);
        else if(ENTRY.Type === 'SHORTANSWER')
            addNewShortAnswerQuestion(ENTRY);
   }
}

// function for creating new Multiple Choice Question
function addNewMultipleChoiceQuestion(ENTRY=null){
    
    const ID = `QUESTION_MULTIPLE_${Math.random()*Math.random()}`;
    let indicator = incremented_indicator;
    // add the ID in the DATA
    data.push(`${ID}`);
    HandleQuizTypeCheckbox();
    const [TIMER_LABEL, TIMER_INPUT] = GetQuizTimeInput(ID);
    if(ENTRY && TIMER_INPUT){
        TIMER_INPUT.value = ENTRY.QuestionTimer;
    }

    // create quiz window
    const QUESTION_DIV = document.createElement('div');
    QUESTION_DIV.classList.add('question');
    QUESTION_DIV.id = `${ID}question`;

    const REMOVE_QUESTION_BUTTON = document.createElement('button');
    REMOVE_QUESTION_BUTTON.id = `${ID}question_remove`;
    REMOVE_QUESTION_BUTTON.innerHTML = 'Remove Question';
    REMOVE_QUESTION_BUTTON.addEventListener('click', (e) => {
        document.getElementById(`${ID}question`).remove();
        data.splice(data.indexOf(`${ID}`),1);
        document.getElementById(`${ID}question_output`).remove() // remove the outputs
        HandleQuizTypeCheckbox();
    })

    const QUESTION_TITLE_LABEL = document.createElement('label');
    QUESTION_TITLE_LABEL.innerHTML = 'Question:';
    QUESTION_TITLE_LABEL.style.fontSize = '20px';

    const QUESTION_TITLE_INPUT = document.createElement('textarea');
    QUESTION_TITLE_INPUT.id = `${ID}title`;
    // check if ENTRY is not null
    if(ENTRY){
        QUESTION_TITLE_INPUT.value = ENTRY.QuizQuestion;
        setTimeout(()=>{
            if(!TIMER_LABEL){
                document.getElementById(`${ID}question_output_title`).innerHTML = QUESTION_TITLE_INPUT.value;
            }else{
                document.getElementById(`${ID}question_output_title`).innerHTML = 
                `${QUESTION_TITLE_INPUT.value} Limit: (${TIMER_INPUT.value}s)`;
            }
            SpanCodeBlock(document.getElementById(`${ID}question_output_title`).innerHTML, document.getElementById(`${ID}question_output_title`));
        }, 20);
    }
    QUESTION_TITLE_INPUT.addEventListener('input', (e) =>{
        if(!TIMER_LABEL){
            document.getElementById(`${ID}question_output_title`).innerHTML = e.target.value;
        }else{
            document.getElementById(`${ID}question_output_title`).innerHTML = 
            `${e.target.value} Limit: (${TIMER_INPUT.value}s)`;
        }

        // get the last input
        {
            let lastInput = e.target.value;
            if(lastInput.slice(-3) === '```'){
                e.target.value = e.target.value + ' \n';
            }else if(lastInput.slice(-4) === '``` '){
                e.target.value = e.target.value.slice(0,-4) 
            }
        }
        SpanCodeBlock(e.target.value, document.getElementById(`${ID}question_output_title`));
    });

    const [QUESTION_OPTION_RADIO, QUESTION_OPTION_LABEL, QUESTION_OPTION_REMOVE] = CreateOptions(ID, indicator);
    
    const QUESTION_OPTION_ADD = document.createElement('button');
    QUESTION_OPTION_ADD.id = `${ID}option_add${indicator}`;
    QUESTION_OPTION_ADD.innerHTML = 'Add choices';
    QUESTION_OPTION_ADD.classList.add('normalButton');

    const GROUP = document.createElement('div');
    GROUP.style.display = 'block';
    // append all objects
    GROUP.appendChild(REMOVE_QUESTION_BUTTON);
    if(TIMER_LABEL){
        GROUP.appendChild(TIMER_LABEL);
        GROUP.appendChild(TIMER_INPUT);
    }
    QUESTION_DIV.appendChild(GROUP);
    QUESTION_DIV.appendChild(QUESTION_TITLE_LABEL);
    QUESTION_DIV.appendChild(QUESTION_TITLE_INPUT);
    let indicator_reducer = 0;
    if(ENTRY){
        for(let ANSWER of ENTRY.QuizAnswers){
            indicator++;
            indicator_reducer++;
            incremented_indicator = indicator;
            const [QUESTION_OPTION_RADIO, QUESTION_OPTION_LABEL, QUESTION_OPTION_REMOVE] = CreateOptions(ID, indicator);
            if(ANSWER === ENTRY.QuizAnswer){
                QUESTION_OPTION_RADIO.checked = true;
            }

            QUESTION_OPTION_LABEL.value = ANSWER;
            QUESTION_DIV.appendChild(QUESTION_OPTION_RADIO);
            QUESTION_DIV.appendChild(QUESTION_OPTION_LABEL);
            QUESTION_DIV.appendChild(QUESTION_OPTION_REMOVE);
        }
    }else{
        QUESTION_DIV.appendChild(QUESTION_OPTION_RADIO);
        QUESTION_DIV.appendChild(QUESTION_OPTION_LABEL);
        QUESTION_DIV.appendChild(QUESTION_OPTION_REMOVE);
    }
    QUESTION_DIV.appendChild(QUESTION_OPTION_ADD);
    questions_create.appendChild(QUESTION_DIV);

    // OUTPUT WINDOW
    const QUESTION_DIV_OUTPUT = document.createElement('div');
    QUESTION_DIV_OUTPUT.classList.add('question');
    QUESTION_DIV_OUTPUT.id = `${ID}question_output`;
    const QUESTION_TITLE_OUTPUT = document.createElement('h2');
    QUESTION_TITLE_OUTPUT.id = `${ID}question_output_title`;
    
    

    // append all objects
    QUESTION_DIV_OUTPUT.appendChild(QUESTION_TITLE_OUTPUT);
    if(ENTRY){
        
        indicator-=indicator_reducer;
        for(let ANSWER of ENTRY.QuizAnswers){
            indicator++;
            incremented_indicator = indicator;
            const QUESTION_RADIO_OUTPUT = document.createElement('input');
            QUESTION_RADIO_OUTPUT.type = 'radio';
            QUESTION_RADIO_OUTPUT.id = `${ID}option_output${indicator}`;
            if(ANSWER === ENTRY.QuizAnswer){
                QUESTION_RADIO_OUTPUT.checked = true;
            }

            const QUESTION_RADIO_LABEL_OUTPUT = document.createElement('label');
            QUESTION_RADIO_LABEL_OUTPUT.id = `${ID}option_label_output${indicator}`;
            QUESTION_RADIO_LABEL_OUTPUT.innerHTML = ANSWER;

            const GROUP = document.createElement('div');
            GROUP.style.display = 'block';
            GROUP.appendChild(QUESTION_RADIO_OUTPUT);
            GROUP.appendChild(QUESTION_RADIO_LABEL_OUTPUT);
            QUESTION_DIV_OUTPUT.appendChild(GROUP)
            questions_output.appendChild(QUESTION_DIV_OUTPUT);

            
        }
        
        // ADD EVENT LISTENER TO ADDING OF OPTIONS
        QUESTION_OPTION_ADD.addEventListener('click', (e)=>{
            indicator++;
            incremented_indicator = indicator;
            const [QUESTION_OPTION_RADIO, QUESTION_OPTION_LABEL, QUESTION_OPTION_REMOVE] = CreateOptions(ID, indicator);
            QUESTION_DIV.appendChild(QUESTION_OPTION_RADIO);
            QUESTION_DIV.appendChild(QUESTION_OPTION_LABEL);
            QUESTION_DIV.appendChild(QUESTION_OPTION_REMOVE);
            QUESTION_DIV.appendChild(QUESTION_OPTION_ADD);

            const GROUP_OUTPUT = document.createElement('div');
            GROUP_OUTPUT.style.display = 'block';
            
            const QUESTION_TITLE_OUTPUT = document.createElement('h2');
            QUESTION_TITLE_OUTPUT.id = `${ID}question_output_title`;
            
            const QUESTION_RADIO_OUTPUT = document.createElement('input');
            QUESTION_RADIO_OUTPUT.type = 'radio';
            QUESTION_RADIO_OUTPUT.id = `${ID}option_output${indicator}`;

            const QUESTION_RADIO_LABEL_OUTPUT = document.createElement('label');
            QUESTION_RADIO_LABEL_OUTPUT.id = `${ID}option_label_output${indicator}`;


            // append all objects
            GROUP_OUTPUT.appendChild(QUESTION_RADIO_OUTPUT);
            GROUP_OUTPUT.appendChild(QUESTION_RADIO_LABEL_OUTPUT);
            QUESTION_DIV_OUTPUT.appendChild(GROUP_OUTPUT);
        });
        
    }else{
        
        const QUESTION_RADIO_OUTPUT = document.createElement('input');
        QUESTION_RADIO_OUTPUT.type = 'radio';
        QUESTION_RADIO_OUTPUT.id = `${ID}option_output${indicator}`;

        const QUESTION_RADIO_LABEL_OUTPUT = document.createElement('label');
        QUESTION_RADIO_LABEL_OUTPUT.id = `${ID}option_label_output${indicator}`;
        QUESTION_DIV_OUTPUT.appendChild(QUESTION_RADIO_OUTPUT);
        QUESTION_DIV_OUTPUT.appendChild(QUESTION_RADIO_LABEL_OUTPUT);

        questions_output.appendChild(QUESTION_DIV_OUTPUT);

        // ADD EVENT LISTENER TO ADDING OF OPTIONS
        QUESTION_OPTION_ADD.addEventListener('click', (e)=>{
            indicator++;
            incremented_indicator = indicator;
            const [QUESTION_OPTION_RADIO, QUESTION_OPTION_LABEL, QUESTION_OPTION_REMOVE] = CreateOptions(ID, indicator);
            QUESTION_DIV.appendChild(QUESTION_OPTION_RADIO);
            QUESTION_DIV.appendChild(QUESTION_OPTION_LABEL);
            QUESTION_DIV.appendChild(QUESTION_OPTION_REMOVE);
            QUESTION_DIV.appendChild(QUESTION_OPTION_ADD);

            const GROUP_OUTPUT = document.createElement('div');
            GROUP_OUTPUT.style.display = 'block';
            
            const QUESTION_TITLE_OUTPUT = document.createElement('h2');
            QUESTION_TITLE_OUTPUT.id = `${ID}question_output_title`;
            
            const QUESTION_RADIO_OUTPUT = document.createElement('input');
            QUESTION_RADIO_OUTPUT.type = 'radio';
            QUESTION_RADIO_OUTPUT.id = `${ID}option_output${indicator}`;

            const QUESTION_RADIO_LABEL_OUTPUT = document.createElement('label');
            QUESTION_RADIO_LABEL_OUTPUT.id = `${ID}option_label_output${indicator}`;


            // append all objects
            GROUP_OUTPUT.appendChild(QUESTION_RADIO_OUTPUT);
            GROUP_OUTPUT.appendChild(QUESTION_RADIO_LABEL_OUTPUT);
            QUESTION_DIV_OUTPUT.appendChild(GROUP_OUTPUT);
        });
    }
}

// Utility method for Multiple choice question
function CreateOptions(ID, indicator){
    const QUESTION_OPTION_RADIO = document.createElement('input');
    QUESTION_OPTION_RADIO.type = 'radio';
    QUESTION_OPTION_RADIO.name = `${ID}option`;
    QUESTION_OPTION_RADIO.id = `${ID}option${indicator}`;
    QUESTION_OPTION_RADIO.addEventListener('click', (e)=>{
        for(let i = 0; i <= incremented_indicator; i++){
            try{
                if(document.getElementById(`${ID}option${i}`) && document.getElementById(`${ID}option_label_output${i}`) )
                if(document.getElementById(`${ID}option${i}`).checked){
                    document.getElementById(`${ID}option_label_output${i}`).innerHTML = `<b>&nbsp;&nbsp;&nbsp;${document.getElementById(`${ID}option_label${i}`).value}</b> [<i>ANSWER</i>]`;
                    document.getElementById(`${ID}option_output${i}`).checked = true;
                }else{
                    document.getElementById(`${ID}option_output${i}`).checked = false;
                    document.getElementById(`${ID}option_label_output${i}`).innerHTML = '&nbsp;&nbsp;&nbsp;'+document.getElementById(`${ID}option_label${i}`).value;
                }
            }catch(er){console.log(er)}
        }
    })

    const QUESTION_OPTION_LABEL = document.createElement('input');
    QUESTION_OPTION_LABEL.type = 'text';
    QUESTION_OPTION_LABEL.name = `${ID}option_label`;
    QUESTION_OPTION_LABEL.id = `${ID}option_label${indicator}`;
    QUESTION_OPTION_LABEL.placeholder = 'Answer...';
    QUESTION_OPTION_LABEL.addEventListener('input', (e)=> {
        if(document.getElementById(`${ID}option${indicator}`) === null)
            return;
        if(document.getElementById(`${ID}option${indicator}`).checked)
            document.getElementById(`${ID}option_label_output${indicator}`).innerHTML = `<b>&nbsp;&nbsp;&nbsp;${e.target.value}</b> [<i>ANSWER</i>]`;
        else document.getElementById(`${ID}option_label_output${indicator}`).innerHTML = '&nbsp;&nbsp;&nbsp;'+e.target.value;
    })

    const QUESTION_OPTION_REMOVE = document.createElement('button');
    QUESTION_OPTION_REMOVE.id = `${ID}option_remove${indicator}`;
    QUESTION_OPTION_REMOVE.classList.add('normalButton');
    QUESTION_OPTION_REMOVE.innerHTML = '-';
    QUESTION_OPTION_REMOVE.addEventListener('click',(e)=>{
        document.getElementById(`${ID}option${indicator}`).remove(); // remove the option
        document.getElementById(`${ID}option_label${indicator}`).remove(); // remove the label
        document.getElementById(`${ID}option_remove${indicator}`).remove(); // remove the label
        document.getElementById(`${ID}option_output${indicator}`).remove() // remove the outputs
        document.getElementById(`${ID}option_label_output${indicator}`).remove() // remove the outputs
        
    });
    return [QUESTION_OPTION_RADIO, QUESTION_OPTION_LABEL, QUESTION_OPTION_REMOVE];
}

// a function to create a short answer question
function addNewShortAnswerQuestion(ENTRY=null){
    const ID = `QUESTION_SHORTANSWER_${Math.random()*Math.random()}`;

    // add the ID in the DATA
    data.push(`${ID}`);
    HandleQuizTypeCheckbox();
    const [TIMER_LABEL, TIMER_INPUT] = GetQuizTimeInput(ID);
    if(ENTRY && TIMER_INPUT){
        TIMER_INPUT.value = ENTRY.QuestionTimer;
    }
    // create quiz window
    const QUESTION_DIV = document.createElement('div');
    QUESTION_DIV.classList.add('question');
    QUESTION_DIV.id = `${ID}question`;

    const REMOVE_QUESTION_BUTTON = document.createElement('button');
    REMOVE_QUESTION_BUTTON.id = `${ID}question_remove`;
    REMOVE_QUESTION_BUTTON.innerHTML = 'Remove Question';
    REMOVE_QUESTION_BUTTON.addEventListener('click', (e) => {
        document.getElementById(`${ID}question`).remove();
        data.splice(data.indexOf(`${ID}`),1);
        document.getElementById(`${ID}question_output`).remove() // remove the outputs
        HandleQuizTypeCheckbox();
    })

    const QUESTION_TITLE_LABEL = document.createElement('label');
    QUESTION_TITLE_LABEL.innerHTML = 'Question:';
    QUESTION_TITLE_LABEL.style.fontSize = '20px';

    const QUESTION_TITLE_INPUT = document.createElement('textarea');
    QUESTION_TITLE_INPUT.id = `${ID}title`;
    QUESTION_TITLE_INPUT.addEventListener('input', (e) =>{
        if(!TIMER_LABEL){
            document.getElementById(`${ID}question_output_title`).innerHTML = e.target.value;
        }else{
            document.getElementById(`${ID}question_output_title`).innerHTML = 
            `${e.target.value} Limit: (${TIMER_INPUT.value}s)`;
        }
        
    });
    const QUESTION_ANSWER_LABEL = document.createElement('label');
    QUESTION_ANSWER_LABEL.innerHTML = 'ANSWER';

    const QUESTION_ANSWER_INPUT = document.createElement('input');
    QUESTION_ANSWER_INPUT.placeholder = 'Answer...';
    QUESTION_ANSWER_INPUT.id = `${ID}answer`;
    QUESTION_ANSWER_INPUT.addEventListener('input', (e) => {
        document.getElementById(`${ID}answer_output`).value = e.target.value;
    })

    if(ENTRY){
        QUESTION_TITLE_INPUT.value = ENTRY.QuizQuestion;
        QUESTION_ANSWER_INPUT.value = ENTRY.QuizAnswer;
        setTimeout(()=>{
            if(TIMER_LABEL){
                document.getElementById(`${ID}question_output_title`).innerHTML = 
                `${QUESTION_TITLE_INPUT.value} Limit: (${TIMER_INPUT.value}s)`;
            }
        }, 20);
    }
    
    const QUESTION_PARAGRAPH = document.createElement('p');
    QUESTION_PARAGRAPH.innerHTML = 
    `The system will convert the answer into lowercase to compare it to the answer value from the user.`;
    QUESTION_PARAGRAPH.style.fontSize = '12px';
    QUESTION_PARAGRAPH.style.color = 'grey';
    QUESTION_PARAGRAPH.style.padding = '5px';
    // append all objects
    const GROUP = document.createElement('div');
    GROUP.style.display = 'block';
    // append all objects
    GROUP.appendChild(REMOVE_QUESTION_BUTTON);
    if(TIMER_LABEL){
        GROUP.appendChild(TIMER_LABEL);
        GROUP.appendChild(TIMER_INPUT);
    }
    QUESTION_DIV.appendChild(GROUP);
    QUESTION_DIV.appendChild(QUESTION_TITLE_LABEL);
    QUESTION_DIV.appendChild(QUESTION_TITLE_INPUT);
    QUESTION_DIV.appendChild(QUESTION_ANSWER_LABEL);
    QUESTION_DIV.appendChild(QUESTION_ANSWER_INPUT);
    QUESTION_DIV.appendChild(QUESTION_PARAGRAPH);
    

    questions_create.appendChild(QUESTION_DIV);

    // OUTPUT WINDOW
    const QUESTION_DIV_OUTPUT = document.createElement('div');
    QUESTION_DIV_OUTPUT.classList.add('question');
    QUESTION_DIV_OUTPUT.id = `${ID}question_output`;
    const QUESTION_TITLE_OUTPUT = document.createElement('h2');
    QUESTION_TITLE_OUTPUT.id = `${ID}question_output_title`;

    const QUESTION_ANSWER_LABEL_OUTPUT = document.createElement('label');
    QUESTION_ANSWER_LABEL_OUTPUT.innerHTML = 'ANSWER ->&nbsp;';
    const QUESTION_ANSWER_OUTPUT = document.createElement('input');
    QUESTION_ANSWER_OUTPUT.type = 'text';
    QUESTION_ANSWER_OUTPUT.id = `${ID}answer_output`;
    QUESTION_ANSWER_OUTPUT.disabled = true;

    if(ENTRY){
        QUESTION_TITLE_OUTPUT.innerHTML = ENTRY.QuizQuestion;
        QUESTION_ANSWER_OUTPUT.value = ENTRY.QuizAnswer;
    }

    // append all objects
    QUESTION_DIV_OUTPUT.appendChild(QUESTION_TITLE_OUTPUT);
    QUESTION_DIV_OUTPUT.appendChild(BREAKLINE);
    QUESTION_DIV_OUTPUT.appendChild(QUESTION_ANSWER_LABEL_OUTPUT);
    QUESTION_DIV_OUTPUT.appendChild(QUESTION_ANSWER_OUTPUT);

    questions_output.appendChild(QUESTION_DIV_OUTPUT);
}

// save the quiz and parse it into a json format then send it to the server
function saveQuiz(){
    const API_KEY = document.getElementById('api-key').value;
    let QUIZZES = []
    let QUIZ_ID = 0
    for(const ID of data){
        // grab the quiz title
        let quiz_question = document.getElementById(`${ID}title`).value;
        let quiz_answer = '';
        let quiz_answers = [];
        // grab the quiz options
        for(let i = 0; i <= incremented_indicator; i++){
            if(document.getElementById(`${ID}option_label${i}`)){
                quiz_answers.push(document.getElementById(`${ID}option_label${i}`).value);
                if(document.getElementById(`${ID}option${i}`).checked)
                    quiz_answer = document.getElementById(`${ID}option_label${i}`).value;
            }
        }
        if (document.getElementById(`${ID}answer`)){
            quiz_answer = document.getElementById(`${ID}answer`).value;
        }
        QUIZZES.push({
            'QuizID':(QUIZ_ID++),
            'QuizQuestion':quiz_question,
            'QuizAnswers':quiz_answers,
            'QuizAnswer':quiz_answer,
            'QuestionTimer': document.getElementById(`${ID}_time`)?Number.parseInt(document.getElementById(`${ID}_time`).value): -1,
            'Type': `${ID}`.split('_')[1]
        })
    }

    const DATA = {
        'QuizTopic':document.getElementById('quiz-title').value,
        'Quiz':QUIZZES,
        'QuizOwner':document.getElementById('quiz_owner').value,
        'CreationDate': new Date().toLocaleDateString(),
        'CreationTime': new Date().toLocaleTimeString()
    }
    

    fetch(`/PSITS/api/quiz?key=${API_KEY}`,{
        method: 'POST',
        body: JSON.stringify(DATA),
        headers: {"Content-type": "application/json; charset=UTF-8"}
    }).then(r => {
        document.getElementById('save-message').innerHTML = 'Saved!';
        document.getElementById('save-message').style.color = 'green';
        setTimeout(()=> {
            window.location.href = '/PSITS@QuizAdmin';
        }, 1000);
    }).catch(e => {
        document.getElementById('save-message').innerHTML = 'Error! '+e;
        document.getElementById('save-message').style.color = 'red';
    });
}

function HandleQuizTypeCheckbox(){
    if(data.length > 0){
        document.getElementById('quiz-type').disabled = true;
    }else{
        document.getElementById('quiz-type').disabled = false;
    }
}

function GetQuizTimeInput(ID){
    const type_element = document.getElementById('quiz-type');

    if(type_element.value === 'timed'){

        const TIMER_LABEL = document.createElement('label');
        TIMER_LABEL.innerHTML = 'Time limit (in seconds)';

        const TIMER_INPUT = document.createElement('input');
        TIMER_INPUT.id = `${ID}_time`;
        TIMER_INPUT.type = 'number';
        TIMER_INPUT.value = 10;

        TIMER_INPUT.addEventListener('input', (e) => {
            document.getElementById(`${ID}question_output_title`).innerHTML = 
            `${document.getElementById(`${ID}title`).value} Limit: (${e.target.value}s)`;
            
        });

        return [TIMER_LABEL, TIMER_INPUT];
    }
    return [null, null];
}

function SpanCodeBlock(TEXT, OUTPUT_ELEMENT){
    const FRAGMENT_TEXT = TEXT.split('\n');
    let isCodeBlock = false;
    let code_block = ``;
    let text = ``;
    
    for(let child of OUTPUT_ELEMENT.childNodes){
        OUTPUT_ELEMENT.removeChild(child)
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
            let word = [...FT]
            if(word.length > 1){
                if(word[0] === '<')
                    word.splice(1,0,'‎')
            }

            let syntax = ``;
            for(let char of word)
                syntax += char;
            
            code_block+= ColorCode(syntax) + "\n";
        }else{
            text += FT + "\n";
            OUTPUT_ELEMENT.innerHTML = text;
        }
    }
    if(code_block){
        const OUTPUT_CHILD_NODE = document.createElement('span');
        OUTPUT_CHILD_NODE.innerHTML = code_block;
        OUTPUT_ELEMENT.appendChild(OUTPUT_CHILD_NODE);
    }
}

function ColorCode(line){
    let new_line = ``
    for(let word of line.split(/ /)){

        if(word.includes('function') || word.includes('def')){
            new_line += `<a style='color: purple;'>${word}</a> `
        }else if(hasDataType(word)){
            new_line += `<a style='color: blue;'>${word}</a> `
        }else if(callFunction(word)){
            new_line += `<a style='color: orange;'>${word}</a> `
        }else{
            new_line +=`${word} `
        }
    }
    return new_line
}

function callFunction(word){
    return /^\w+\((([A-Za-z]+)?)\)(;)?$/.test(word)
}

function hasDataType(word){
    if(!word)
        return false
    if(
        word === 'let' ||
        word === 'var' ||
        word === 'int' ||
        word === 'string' ||
        word.toLowerCase() === 'double' ||
        word.toLowerCase() === 'float' ||
        word === 'Object' || word === 'Number' || word === 'String'
        || word === 'System'){
        return true
    }
    return false
}