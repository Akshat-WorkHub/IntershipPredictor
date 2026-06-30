/* ==========================================================
                    INTERVIEW PAGE
========================================================== */

let interviewData = null;
let currentQuestion = 0;
let answers = [];

/* ==========================================================
                    DOM ELEMENTS
========================================================== */

const setupCard = document.getElementById("setupCard");
const interviewCard = document.getElementById("interviewCard");

const startBtn = document.getElementById("startInterview");

const previousBtn = document.getElementById("previousBtn");
const nextBtn = document.getElementById("nextBtn");
const submitBtn = document.getElementById("submitInterview");

const questionCounter = document.getElementById("questionCounter");
const questionText = document.getElementById("questionText");

const answerInput = document.getElementById("answerInput");
const dontKnowInput = document.getElementById("dontKnowInput");

const progressBar = document.getElementById("progressBar");

const categoryBadge = document.getElementById("categoryBadge");


const difficulty = document.getElementById("difficulty");
const interviewMode = document.getElementById("interviewMode");
const questionCount = document.getElementById("questionCount");

/* ==========================================================
                START INTERVIEW
========================================================== */

startBtn.addEventListener(
    "click",
    generateInterview
);

/* ==========================================================
                GENERATE QUESTIONS
========================================================== */

async function generateInterview(){

    const profile =
        StorageService.loadProfile();

    if(!profile){

        alert(
            "Generate Candidate Profile first."
        );

        window.location.href = "index.html";

        return;

    }

    const payload = {

        interview_mode:
            interviewMode.value,

        difficulty:
            difficulty.value,

        number_of_questions:
            Number(questionCount.value),

        resume_data:
            profile.resume_data,

        jd_data:
            profile.jd_data,

        missing_skills:
            profile.missing_skills

    };

    try{

        startBtn.disabled = true;

        startBtn.innerHTML =
            '<i class="fa-solid fa-spinner fa-spin"></i> Generating...';

        const response =
            await APIService.generateInterview(
                payload
            );
        console.log(payload);

        if(!response.ok){

            throw new Error(
                "Unable to generate interview."
            );

        }

        interviewData =
            await response.json();

        answers =
            new Array(
                interviewData.questions.length
            )
            .fill(null)
            .map(() => ({
                answer: "",
                dont_know: false
            }));

        setupCard.style.display = "none";

        interviewCard.style.display = "block";

        currentQuestion = 0;

        renderQuestion();

    }

    catch(error){

        console.error(error);

        alert(error.message);

    }

    finally{

        startBtn.disabled = false;

        startBtn.innerHTML =
            '<i class="fa-solid fa-play"></i> Start Interview';

    }

}

/* ==========================================================
                RENDER QUESTION
========================================================== */

function renderQuestion(){

    const question =
        interviewData.questions[currentQuestion];

    questionCounter.innerText =
        `Question ${currentQuestion+1} / ${interviewData.questions.length}`;

    questionText.innerText =
        question.question;

    categoryBadge.innerText =
        question.category || "Interview";

    const savedAnswer =
        answers[currentQuestion] || {
            answer: "",
            dont_know: false
        };

    answerInput.value =
        savedAnswer.answer;

    dontKnowInput.checked =
        savedAnswer.dont_know;

    answerInput.disabled =
        savedAnswer.dont_know;

    progressBar.style.width =
        `${((currentQuestion+1)/interviewData.questions.length)*100}%`;

    previousBtn.style.display =
        currentQuestion===0
        ? "none"
        : "inline-flex";

    nextBtn.style.display =
        currentQuestion===interviewData.questions.length-1
        ? "none"
        : "inline-flex";

    submitBtn.style.display =
        currentQuestion===interviewData.questions.length-1
        ? "inline-flex"
        : "none";

}

/* ==========================================================
                SAVE ANSWER
========================================================== */

function saveCurrentAnswer(){

    answers[currentQuestion] = {
        answer:
            dontKnowInput.checked
            ? ""
            : answerInput.value.trim(),

        dont_know:
            dontKnowInput.checked
    };

}

function hasCurrentAnswer(){

    return (
        answerInput.value.trim().length > 0 ||
        dontKnowInput.checked
    );

}

function showAnswerRequired(){

    alert(
        "Please provide an answer or select 'I don't know the answer'."
    );

}

dontKnowInput.addEventListener(
    "change",
    function(){

        answerInput.disabled =
            this.checked;

        if(this.checked){

            answerInput.value = "";

        }

    }
);

/* ==========================================================
                NEXT
========================================================== */

nextBtn.addEventListener(
    "click",
    function(){

        if(!hasCurrentAnswer()){

            showAnswerRequired();

            return;

        }

        saveCurrentAnswer();

        if(
            currentQuestion <
            interviewData.questions.length-1
        ){

            currentQuestion++;

            renderQuestion();

        }

    }
);

/* ==========================================================
                PREVIOUS
========================================================== */

previousBtn.addEventListener(
    "click",
    function(){

        saveCurrentAnswer();

        if(currentQuestion>0){

            currentQuestion--;

            renderQuestion();

        }

    }
);

/* ==========================================================
            SUBMIT INTERVIEW
========================================================== */

submitBtn.addEventListener(
    "click",
    submitInterview
);

async function submitInterview(){

    if(!hasCurrentAnswer()){

        showAnswerRequired();

        return;

    }

    saveCurrentAnswer();

    const submittedAnswers = {};

    interviewData.questions.forEach(

        (question,index)=>{

            const savedAnswer =
                answers[index] || {
                    answer: "",
                    dont_know: false
                };

            submittedAnswers[index] = {

                question:
                    question.question,

                category:
                    question.category,

                answer:
                    savedAnswer.dont_know
                    ? "I don't know"
                    : savedAnswer.answer,

                dont_know:
                    savedAnswer.dont_know

            };

        }

    );

    const payload = {

        answers:
            submittedAnswers

    };

    try{

        submitBtn.disabled = true;

        submitBtn.innerHTML =
            '<i class="fa-solid fa-spinner fa-spin"></i> Evaluating...';

        const response =
            await APIService.evaluateInterview(
                payload
            );

        if(!response.ok){

            throw new Error(
                "Interview evaluation failed."
            );

        }

        const result =
            await response.json();

        StorageService.saveEvaluation(
            result
        );

        window.location.href =
            "/analysis.html";

    }

    catch(error){

        console.error(error);

        alert(error.message);

    }

    finally{

        submitBtn.disabled = false;

        submitBtn.innerHTML =
            '<i class="fa-solid fa-paper-plane"></i> Submit Interview';

    }

}
