/* ============================================
   API Calls
============================================ */
console.log("✅ api.js loaded");
const APIService = {

    async generateProfile(formData){

        const response = await fetch(

            API.BASE_URL +
            API.ENDPOINTS.GENERATE_PROFILE,

            {

                method:"POST",

                body:formData

            }

        );

        return response;

    },

    async generateRoadmap(missingSkills){

        const response = await fetch(

            API.BASE_URL +
            API.ENDPOINTS.GENERATE_ROADMAP,

            {

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({

                    missing_skills:
                        missingSkills

                })

            }

        );

        return response;

    },

    async generateInterviewPreparation(data){

        const response = await fetch(

            API.BASE_URL +
            API.ENDPOINTS.GENERATE_INTERVIEW_PREPARATION,

            {

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify(data)

            }

        );

        return response;

    },

    async downloadInterviewPreparation(data){

        const response = await fetch(

            API.BASE_URL +
            API.ENDPOINTS.DOWNLOAD_INTERVIEW_PREPARATION,

            {

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify(data)

            }

        );

        return response;

    },

    async generateInterview(data){

        const response = await fetch(

            API.BASE_URL +
            API.ENDPOINTS.GENERATE_INTERVIEW,

            {

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify(data)

            }

        );

        return response;

    },

    async evaluateInterview(data){

        const response = await fetch(

            API.BASE_URL +
            API.ENDPOINTS.EVALUATE_INTERVIEW,

            {

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify(data)

            }

        );

        return response;

    }

};