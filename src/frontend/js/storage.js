/* ============================================
   Session Storage Helper
============================================ */
console.log("✅ storage.js loaded");

const STORAGE_KEYS = [
    "profile_result",
    "roadmap",
    "evaluation_report"
];

STORAGE_KEYS.forEach((key) => {
    localStorage.removeItem(key);
});

const StorageService = {

    saveProfile(data){

        sessionStorage.setItem(
            "profile_result",
            JSON.stringify(data)
        );

    },

    loadProfile(){

        const data =
            sessionStorage.getItem(
                "profile_result"
            );

        return data
            ? JSON.parse(data)
            : null;

    },

    saveRoadmap(data){

        sessionStorage.setItem(
            "roadmap",
            JSON.stringify(data)
        );

    },

    loadRoadmap(){

        const data =
            sessionStorage.getItem(
                "roadmap"
            );

        return data
            ? JSON.parse(data)
            : null;

    },

    saveEvaluation(data){

        sessionStorage.setItem(
            "evaluation_report",
            JSON.stringify(data)
        );

    },

    loadEvaluation(){

        const data =
            sessionStorage.getItem(
                "evaluation_report"
            );

        return data
            ? JSON.parse(data)
            : null;

    },

    clear(){

        sessionStorage.clear();

    }

};

window.StorageService = StorageService;