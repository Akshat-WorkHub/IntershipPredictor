/* ==========================================================
   HOME PAGE
========================================================== */

/* ==========================================================
   DOM ELEMENTS
========================================================== */
console.log("✅ home.js loaded");

const resumeInput =
    document.getElementById("resume");

const jdInput =
    document.getElementById("jobDescription");

const githubInput =
    document.getElementById("github");

const communicationSlider =
    document.getElementById("communication");

const codingSlider =
    document.getElementById("coding");

const aptitudeSlider =
    document.getElementById("aptitude");

const softSkillSlider =
    document.getElementById("softSkills");

const backlogsInput =
    document.getElementById("backlogs");

const collegeTier =
    document.getElementById("collegeTier");

const placementTraining =
    document.getElementById("placementTraining");

const generateProfileBtn =
    document.getElementById("generateProfile");

const roadmapBtn =
    document.getElementById("roadmapBtn");

const preparationBtn =
    document.getElementById("preparationBtn");

/* ==========================================================
   SLIDER VALUES
========================================================== */

const communicationValue =
    document.getElementById("communicationValue");

const codingValue =
    document.getElementById("codingValue");

const aptitudeValue =
    document.getElementById("aptitudeValue");

const softSkillValue =
    document.getElementById("softSkillsValue");

/* ==========================================================
   RESULT ELEMENTS
========================================================== */

const loaderSection =
    document.getElementById("loaderSection");

const resultSection =
    document.getElementById("resultSection");

const predictionBar =
    document.getElementById("predictionBar");

const predictionPercentage =
    document.getElementById("predictionPercentage");

const predictionMessage =
    document.getElementById("predictionMessage");

const matchBar =
    document.getElementById("matchBar");

const matchPercentage =
    document.getElementById("matchPercentage");

const matchMessage =
    document.getElementById("matchMessage");

/* ==========================================================
   GLOBAL VARIABLES
========================================================== */

let profileData = null;

/* ==========================================================
   UPDATE SLIDER VALUE
========================================================== */

function updateSliderValue(slider, label){

    label.textContent = slider.value;

}

communicationSlider.addEventListener(
    "input",
    () =>
        updateSliderValue(
            communicationSlider,
            communicationValue
        )
);

codingSlider.addEventListener(
    "input",
    () =>
        updateSliderValue(
            codingSlider,
            codingValue
        )
);

aptitudeSlider.addEventListener(
    "input",
    () =>
        updateSliderValue(
            aptitudeSlider,
            aptitudeValue
        )
);

softSkillSlider.addEventListener(
    "input",
    () =>
        updateSliderValue(
            softSkillSlider,
            softSkillValue
        )
);

/* ==========================================================
   FILE VALIDATION
========================================================== */

function validatePDF(file){

    if(!file){

        return false;

    }

    return file.type ===
        "application/pdf";

}

/* ==========================================================
   SHOW LOADER
========================================================== */

function showLoader(){

    loaderSection.style.display = "block";

    resultSection.style.display = "none";

}

/* ==========================================================
   HIDE LOADER
========================================================== */

function hideLoader(){

    loaderSection.style.display = "none";

}

/* ==========================================================
   SHOW RESULT
========================================================== */

function showResult(){

    resultSection.style.display = "block";

}

/* ==========================================================
   SIMPLE ALERT
========================================================== */

function showError(message){

    alert(message);

}

/* ==========================================================
   INITIALIZE
========================================================== */

window.onload = () => {

    updateSliderValue(
        communicationSlider,
        communicationValue
    );

    updateSliderValue(
        codingSlider,
        codingValue
    );

    updateSliderValue(
        aptitudeSlider,
        aptitudeValue
    );

    updateSliderValue(
        softSkillSlider,
        softSkillValue
    );

    const storedProfile =
        StorageService.loadProfile();

    if(storedProfile){

        profileData = storedProfile;

        renderPrediction(
            storedProfile
        );

        renderCompatibility(
            storedProfile.skill_gap
        );

        showResult();

    }

};

/* ==========================================================
   GENERATE PROFILE
========================================================== */

generateProfileBtn.addEventListener(

    "click",

    async function (event) {

        event.preventDefault();

        const resumeFile =
            resumeInput.files[0];

        const jdFile =
            jdInput.files[0];

        /* -----------------------------
           Validation
        ------------------------------ */

        if (!resumeFile) {

            showError(
                "Please upload your Resume."
            );

            return;

        }

        if (!jdFile) {

            showError(
                "Please upload Job Description."
            );

            return;

        }

        if (!validatePDF(resumeFile)) {

            showError(
                "Resume must be a PDF."
            );

            return;

        }

        if (!validatePDF(jdFile)) {

            showError(
                "Job Description must be a PDF."
            );

            return;

        }

        /* -----------------------------
           Create FormData
        ------------------------------ */

        const formData =
            new FormData();

        formData.append(
            "resume",
            resumeFile
        );

        formData.append(
            "job_description",
            jdFile
        );

        formData.append(
            "github_url",
            githubInput.value
        );

        formData.append(
            "communication_score",
            communicationSlider.value
        );

        formData.append(
            "coding_score",
            codingSlider.value
        );

        formData.append(
            "aptitude_score",
            aptitudeSlider.value
        );

        formData.append(
            "soft_skills_score",
            softSkillSlider.value
        );

        formData.append(
            "backlogs",
            backlogsInput.value
        );

        formData.append(
            "college_tier",
            collegeTier.value
        );

        formData.append(
            "placement_training",
            placementTraining.value
        );

        /* -----------------------------
           Loader
        ------------------------------ */

        showLoader();

        generateProfileBtn.disabled = true;

        generateProfileBtn.innerHTML =
            '<i class="fa-solid fa-spinner fa-spin"></i> Generating...';

        try {

            const response =
                await APIService.generateProfile(
                    formData
                );

            if (!response.ok) {

                throw new Error(
                    "Failed to generate profile."
                );

            }

            profileData =
                await response.json();

            StorageService.saveProfile(
                profileData
            );

            renderPrediction(
                profileData
            );

            renderCompatibility(
                profileData.skill_gap
            );

            showResult();

        }

        catch (error) {

            console.error(error);

            showError(
                error.message
            );

        }

        finally {

            hideLoader();

            generateProfileBtn.disabled = false;

            generateProfileBtn.innerHTML =
                '<i class="fa-solid fa-rocket"></i> Generate Candidate Profile';

        }

    }

);

/* ==========================================================
   RENDER SCREENING CONFIDENCE
========================================================== */

function renderPrediction(data){

    const probability =
        Number(data.prediction_probability);

    predictionBar.style.width =
        probability + "%";

    predictionPercentage.textContent =
        probability + "%";

    let title = "";
    let message = "";
    let cssClass = "";

    if(probability >= 80){

        title = "🎉 Strong Match Detected";

        message =
            "Your profile shows a high likelihood of passing the initial screening stage.";

        cssClass = "success";

    }

    else if(probability >= 60){

        title = "⚡ Moderate Match";

        message =
            "Your profile aligns reasonably well, but improving missing skills could increase your chances.";

        cssClass = "warning";

    }

    else{

        title = "⚠ Improvement Needed";

        message =
            "There are noticeable gaps between your profile and the target role.";

        cssClass = "danger";

    }

    predictionMessage.className =
        "status-card " + cssClass;

    predictionMessage.innerHTML = `

        <h3>${title}</h3>

        <p>${message}</p>

    `;

}

/* ==========================================================
   RENDER RESUME-JD MATCH
========================================================== */

function renderCompatibility(skillGap){

    if (!skillGap) {

        throw new Error(
            "skill_gap missing in API response"
        );

    }

    const match =
        skillGap.match_percentage;

    matchBar.style.width =
        match + "%";

    matchPercentage.textContent =
        match.toFixed(2) + "%";

    let title = "";
    let cssClass = "";

    if(match >= 80){

        title =
            "Excellent Match 🟢";

        cssClass =
            "success";

    }

    else if(match >= 60){

        title =
            "Good Match 🟡";

        cssClass =
            "warning";

    }

    else if(match >= 40){

        title =
            "Average Match 🟠";

        cssClass =
            "warning";

    }

    else{

        title =
            "Weak Match 🔴";

        cssClass =
            "danger";

    }

    matchMessage.className =
        "status-card " + cssClass;

    matchMessage.innerHTML = `

        <h3>${title}</h3>

        <p>

            Resume and Job Description compatibility:
            <strong>${match.toFixed(2)}%</strong>

        </p>

    `;

}

/* ==========================================================
   GENERATE ROADMAP
========================================================== */

roadmapBtn.addEventListener(

    "click",

    async function(){

        if(profileData == null){

            showError(
                "Generate profile first."
            );

            return;

        }

        roadmapBtn.disabled = true;

        roadmapBtn.innerHTML =
            '<i class="fa-solid fa-spinner fa-spin"></i> Generating...';

        try{

            const response =
                await APIService.generateRoadmap(

                    profileData.skill_gap.missing_skills

                );

            if(!response.ok){

                throw new Error(
                    "Failed to generate roadmap."
                );

            }

            const roadmap =
                await response.json();

            const roadmapData = {
                ...roadmap,
                missing_skills:
                    roadmap.missing_skills ||
                    profileData.skill_gap.missing_skills
            };

            StorageService.saveRoadmap(
                roadmapData
            );

            if (!StorageService.loadRoadmap()) {

                throw new Error(
                    "Roadmap data could not be saved for this browser session."
                );

            }

            window.location.href =
                "/roadmap.html";

        }

        catch(error){

            console.error(error);

            showError(
                error.message
            );

        }

        finally{

            roadmapBtn.disabled = false;

            roadmapBtn.innerHTML =

                '<i class="fa-solid fa-map"></i> Generate Personalized Roadmap';

        }

    }

);

/* ==========================================================
   GENERATE INTERVIEW PREPARATION
========================================================== */

preparationBtn.addEventListener(
    "click",
    ()=>{

        window.location.href =
            "interview-preparation.html";

    }
);

/* ==========================================================
   SHOW SELECTED FILE NAME
========================================================== */

resumeInput.addEventListener(

    "change",

    function(){

        if(this.files.length){

            this.parentElement.querySelector("span").textContent =
                this.files[0].name;

        }

    }

);

jdInput.addEventListener(

    "change",

    function(){

        if(this.files.length){

            this.parentElement.querySelector("span").textContent =
                this.files[0].name;

        }

    }

);

/* ==========================================================
   END OF FILE
========================================================== */
