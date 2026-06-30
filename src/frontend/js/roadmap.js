/* ==========================================================
                ROADMAP PAGE
========================================================== */

/* =========================
        DOM ELEMENTS
========================= */

const skillsContainer =
    document.getElementById(
        "skillsContainer"
    );

const roadmapContainer =
    document.getElementById(
        "roadmapContainer"
    );

const backButton =
    document.getElementById(
        "backButton"
    );

const interviewButton =
    document.getElementById(
        "interviewButton"
    );

/* ==========================================================
        LOAD ROADMAP
========================================================== */

const roadmapData =
    StorageService.loadRoadmap();

if (!roadmapData) {

    alert(
        "Please generate a roadmap first."
    );

    window.location.href =
        "index.html";

}

/* ==========================================================
        RENDER SKILLS
========================================================== */

function renderSkills() {

    skillsContainer.innerHTML = "";

    roadmapData.missing_skills.forEach(

        skill => {

            const chip =
                document.createElement("div");

            chip.className =
                "skill-chip";

            chip.textContent =
                skill;

            skillsContainer.appendChild(
                chip
            );

        }

    );

}

/* ==========================================================
        CREATE TOPIC LIST
========================================================== */

function createTopicList(topics) {

    const ul =
        document.createElement("ul");

    ul.className =
        "topic-list";

    topics.forEach(topic => {

        const li =
            document.createElement("li");

        li.textContent =
            topic;

        ul.appendChild(li);

    });

    return ul;

}

/* ==========================================================
        CREATE RESOURCE LIST
========================================================== */

function createResources(resources) {

    const wrapper =
        document.createElement("div");

    wrapper.className =
        "resource-list";

    resources.forEach(resource => {

        const card =
            document.createElement("div");

        card.className =
            "resource-card";

        card.innerHTML =

            `<i class="fa-solid fa-book"></i>
             ${resource}`;

        wrapper.appendChild(card);

    });

    return wrapper;

}

/* ==========================================================
        CREATE PROJECT CARD
========================================================== */

function createProject(project) {

    const card =
        document.createElement("div");

    card.className =
        "project-card";

    card.innerHTML =

        `
        <h4>

            <i class="fa-solid fa-code"></i>

            Mini Project

        </h4>

        <p>

            ${project}

        </p>
        `;

    return card;

}

/* ==========================================================
        RENDER ROADMAP
========================================================== */

function renderRoadmap() {

    roadmapContainer.innerHTML = "";

    roadmapData.roadmap.forEach(

        week => {

            const card =
                document.createElement("div");

            card.className =
                "week-card";

            card.innerHTML =

            `
            <div class="week-header">

                <div class="week-title">

                    Week ${week.week}

                </div>

                <div class="week-focus">

                    ${week.focus}

                </div>

            </div>

            <h3 class="section-title">

                Topics

            </h3>
            `;

            card.appendChild(

                createTopicList(
                    week.topics
                )

            );

            const resourceTitle =
                document.createElement("h3");

            resourceTitle.className =
                "section-title";

            resourceTitle.textContent =
                "Resources";

            card.appendChild(
                resourceTitle
            );

            card.appendChild(

                createResources(
                    week.resources
                )

            );

            const projectTitle =
                document.createElement("h3");

            projectTitle.className =
                "section-title";

            projectTitle.textContent =
                "Project";

            card.appendChild(
                projectTitle
            );

            card.appendChild(

                createProject(
                    week.project
                )

            );

            roadmapContainer.appendChild(
                card
            );

        }

    );

}

/* ==========================================================
        BUTTONS
========================================================== */

backButton.addEventListener(

    "click",

    function () {

        window.location.href =
            "index.html";

    }

);

interviewButton.addEventListener(

    "click",

    function () {

        window.location.href =
            "/interview.html";

    }

);

/* ==========================================================
        INITIALIZE
========================================================== */

renderSkills();

renderRoadmap();
