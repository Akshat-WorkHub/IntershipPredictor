class UserProfileService:
    def generate_user_profile(self, profile_result, form_result):
        return {
            **profile_result,
            **form_result
        }


