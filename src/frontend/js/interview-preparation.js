/* ============================================
   Elements
============================================ */

const generateBtn = document.getElementById("generateBtn");
const loadingSection = document.getElementById("loadingSection");
const questionsContainer = document.getElementById("questionsContainer");
const downloadSection = document.getElementById("downloadSection");
let generatedQuestions = [];



/* ============================================
   Generate Button
============================================ */

generateBtn.addEventListener(

    "click",

    async () => {

        questionsContainer.innerHTML = "";

        questionsContainer.classList.add("hidden");

        downloadSection.classList.add("hidden");

        loadingSection.classList.remove("hidden");

        generateBtn.disabled = true;

        generateBtn.innerHTML =
            `<i class="fa-solid fa-spinner fa-spin"></i> Generating...`;

        try{

            const profile =
                StorageService.loadProfile();

            if(!profile){

                alert(
                    "Please generate your candidate profile first."
                );

                return;

            }

            const request = {

                interview_mode:
                    document.getElementById("interviewMode").value,

                difficulty:
                    document.getElementById("difficulty").value,

                number_of_questions:
                    Number(
                        document.getElementById("questionCount").value
                    ),

                resume_data:
                    profile.resume_data,

                jd_data:
                    profile.jd_data,

                missing_skills:
                    profile.missing_skills

            };

            const response =
                await APIService.generateInterviewPreparation(request);

            if(!response.ok){

                throw new Error(
                    "Failed to generate interview preparation."
                );

            }

            const result =
                await response.json();

            loadingSection.classList.add("hidden");

            generatedQuestions = result.questions;

            renderQuestions(
                generatedQuestions
            );

            questionsContainer.classList.remove("hidden");

            downloadSection.classList.remove("hidden");

        }

        catch(error){

            console.error(error);

            loadingSection.classList.add("hidden");

            alert(error.message);

        }

        finally{

            generateBtn.disabled = false;

            generateBtn.innerHTML =
                `<i class="fa-solid fa-wand-magic-sparkles"></i>
                Generate Preparation Material`;

        }

    }

);


/* ============================================
   Render Questions
============================================ */

function renderQuestions(interviewQuestions) {

    interviewQuestions.forEach((item, index) => {

        const card = document.createElement("div");

        card.className = "question-card";

        card.innerHTML = `

            <div class="question-header">

                <span class="badge">

                    ${item.category}

                </span>

                <span class="difficulty">

                    ${item.difficulty}

                </span>

            </div>

            <h3>

                Q${index + 1}. ${item.question}

            </h3>

            <button class="toggle-answer">

                Show Answer

            </button>

            <div class="answer hidden">

                <h4>🎯 Interviewer's Intent</h4>
                <p>${item.interviewer_intent}</p>

                <h4>💬 Candidate Answer</h4>
                <p>${item.candidate_answer}</p>

                <h4> Key Points </h4>

                <ul>

                    ${item.key_points
                        .map(point => `<li>${point}</li>`)
                        .join("")}

                </ul>

            </div>

        `;

        questionsContainer.appendChild(card);

    });

}


/* ============================================
   Show / Hide Answer
============================================ */

document.addEventListener("click", function(event){

    if(event.target.classList.contains("toggle-answer")){

        const answer =
            event.target.nextElementSibling;

        answer.classList.toggle("hidden");

        if(answer.classList.contains("hidden")){

            event.target.innerHTML =
                "Show Answer";

        }

        else{

            event.target.innerHTML =
                "Hide Answer";

        }

    }

});


/* ============================================
   Download Button
============================================ */

document.querySelector(".download-btn").addEventListener(

    "click",

    async () => {

        try{

            const payload = {

                interview_mode:
                    document.getElementById("interviewMode").value,

                difficulty:
                    document.getElementById("difficulty").value,

                questions:
                    generatedQuestions

            };

            const response =
                await APIService.downloadInterviewPreparation(
                    payload
                );

            if(!response.ok){

                throw new Error(
                    "Unable to download PDF."
                );

            }

            const blob =
                await response.blob();

            const url =
                window.URL.createObjectURL(
                    blob
                );

            const link =
                document.createElement("a");

            link.href = url;

            link.download =
                "Interview_Preparation_Guide.pdf";

            document.body.appendChild(link);

            link.click();

            link.remove();

            window.URL.revokeObjectURL(url);

        }

        catch(error){

            console.error(error);

            alert(error.message);

        }

    }

);