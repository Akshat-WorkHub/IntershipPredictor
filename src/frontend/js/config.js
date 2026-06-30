/* ============================================
   API Configuration
============================================ */
console.log("✅ config.js loaded");
const API = {

    BASE_URL:
        window.location.origin.startsWith("http")
            ? window.location.origin
            : "http://127.0.0.1:8000",

    ENDPOINTS: {

        GENERATE_PROFILE:
            "/profile/generate",

        GENERATE_ROADMAP:
            "/roadmap/generate",

        GENERATE_INTERVIEW_PREPARATION:
            "/interview-preparation/generate",

        DOWNLOAD_INTERVIEW_PREPARATION:
            "/interview-preparation/download",

        GENERATE_INTERVIEW:
            "/interview/generate",

        EVALUATE_INTERVIEW:
            "/interview/evaluate"

    }

};
