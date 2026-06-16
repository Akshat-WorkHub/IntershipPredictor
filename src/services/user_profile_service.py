import os, json

class UserProfileService:
    def __init__(self):
        project_root = os.path.abspath(os.path.join( os.path.dirname(__file__), "..", ".." ))
        self.dirpath = os.path.join(project_root,"new_data","raw_features")

    def generate_user_profile(self, profile_result, form_result):
        os.makedirs(self.dirpath, exist_ok=True)
        
        profile_filepath = os.path.join(self.dirpath,"profile.json")
        form_filepath = os.path.join(self.dirpath, "form.json")
        raw_data_filepath = os.path.join(self.dirpath, "raw_data.json")
        
        with open(profile_filepath,"w") as file:
            json.dump(profile_result, file, indent=4)

        with open(form_filepath,"w") as file:
            json.dump(form_result, file, indent=4)

        result = {
            **profile_result,
            **form_result
        }

        with open(raw_data_filepath,"w") as file:
            json.dump(result, file, indent=4)

        return result


