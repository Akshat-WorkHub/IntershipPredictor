/* ==========================================================
                    ANALYSIS PAGE
========================================================== */

const analysis =
    StorageService.loadEvaluation();

/* ==========================================================
                    DOM
========================================================== */

const overallScore =
    document.getElementById("overallScore");

const attemptedQuestions =
    document.getElementById("attemptedQuestions");

const unattemptedQuestions =
    document.getElementById("unattemptedQuestions");

const summaryTitle =
    document.getElementById("summaryTitle");

const summaryText =
    document.getElementById("summaryText");

const strengthList =
    document.getElementById("strengthList");

const improvementList =
    document.getElementById("improvementList");

const revisionList =
    document.getElementById("revisionList");

const questionAnalysis =
    document.getElementById("questionAnalysis");

const roadmapBtn =
    document.getElementById("roadmapBtn");

const restartBtn =
    document.getElementById("restartBtn");

/* ==========================================================
                    INIT
========================================================== */

document.addEventListener(
    "DOMContentLoaded",
    init
);

function init(){

    if(!analysis){

        alert(
            "Interview analysis not found."
        );

        window.location.href =
            "interview.html";

        return;

    }

    renderDashboard();

}

/* ==========================================================
                DASHBOARD
========================================================== */

function renderDashboard(){

    overallScore.innerText =
        analysis.overall_score.toFixed(1);

    attemptedQuestions.innerText =
        analysis.attempted_questions;

    unattemptedQuestions.innerText =
        analysis.unattempted_questions;

    renderSummary();

    renderList(
        strengthList,
        analysis.strengths
    );

    renderList(
        improvementList,
        analysis.improvements
    );

    renderList(
        revisionList,
        analysis.questions_to_revise
    );

    renderQuestionAnalysis();

}

/* ==========================================================
                    SUMMARY
========================================================== */

function renderSummary(){

    const score =
        analysis.overall_score;

    if(score>=9){

        summaryTitle.innerText =
            "🌟 Excellent Performance";

        summaryText.innerText =
            "Outstanding interview performance. Continue refining your communication and technical depth.";

    }

    else if(score>=7){

        summaryTitle.innerText =
            "✅ Good Performance";

        summaryText.innerText =
            "You performed well. Focus on the suggested improvements to reach an excellent level.";

    }

    else if(score>=5){

        summaryTitle.innerText =
            "⚡ Average Performance";

        summaryText.innerText =
            "You have a solid foundation, but more practice is needed before interviews.";

    }

    else{

        summaryTitle.innerText =
            "📚 Needs Improvement";

        summaryText.innerText =
            "Spend more time revising technical concepts and practicing mock interviews.";

    }

}

/* ==========================================================
                SIMPLE LIST
========================================================== */

function renderList(
    element,
    items
){

    element.innerHTML = "";

    items.forEach(item=>{

        const li =
            document.createElement("li");

        li.innerHTML =
            `<i class="fa-solid fa-check"></i> ${item}`;

        element.appendChild(li);

    });

}

/* ==========================================================
            QUESTION ANALYSIS
========================================================== */

function renderQuestionAnalysis(){

    questionAnalysis.innerHTML = "";

    analysis.question_analysis.forEach(
        (question,index)=>{

            const card =
                document.createElement("div");

            card.className =
                "question-item";

            let badgeClass = "";

            if(question.score>=9){

                badgeClass =
                    "score-excellent";

            }

            else if(question.score>=7){

                badgeClass =
                    "score-good";

            }

            else if(question.score>=5){

                badgeClass =
                    "score-average";

            }

            else{

                badgeClass =
                    "score-poor";

            }

            card.innerHTML =

            `
            <div class="question-header">

                <div>

                    <div class="question-title">

                        Q${index+1}. ${question.question}

                    </div>

                    <small>

                        ${question.category}

                    </small>

                </div>

                <div class="score-badge ${badgeClass}">

                    ${question.score}/10

                </div>

            </div>

            <div class="question-content">

                <h4>Status</h4>

                <p>

                    ${question.status}

                </p>

                <h4>Your Answer</h4>

                <p>

                    ${question.candidate_answer}

                </p>

                <h4>Feedback</h4>

                <p>

                    ${question.feedback}

                </p>

                <h4>Strengths</h4>

                <ul>

                    ${question.strengths.map(
                        s=>`<li>${s}</li>`
                    ).join("")}

                </ul>

                <h4>Improvements</h4>

                <ul>

                    ${question.improvements.map(
                        s=>`<li>${s}</li>`
                    ).join("")}

                </ul>

                <h4>Ideal Answer</h4>

                <p>

                    ${question.ideal_answer}

                </p>

            </div>

            `;

            const header =
                card.querySelector(
                    ".question-header"
                );

            const content =
                card.querySelector(
                    ".question-content"
                );

            header.addEventListener(
                "click",
                ()=>{

                    if(
                        content.style.display==="block"
                    ){

                        content.style.display="none";

                    }

                    else{

                        content.style.display="block";

                    }

                }
            );

            questionAnalysis.appendChild(
                card
            );

        }

    );

}

/* ==========================================================
                BUTTONS
========================================================== */

roadmapBtn.addEventListener(
    "click",
    ()=>{

        window.location.href =
            "roadmap.html";

    }
);

restartBtn.addEventListener(
    "click",
    ()=>{

        localStorage.removeItem(
            "interviewAnalysis"
        );

        window.location.href =
            "interview.html";

    }
);