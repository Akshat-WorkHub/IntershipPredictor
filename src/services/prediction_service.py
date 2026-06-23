import os, pickle
import pandas as pd

class PredictionService:
    def __init__(self):
        root_dir = os.path.abspath(os.path.join( os.path.dirname(__file__), "..", ".." ))
        models_dir = os.path.join(root_dir,"final_models")

        preprocessor_path = os.path.join(
            models_dir,
            "preprocessor.pkl"
        )

        model_path = os.path.join(
            models_dir,
            "model.pkl"
        )

        self.validate_model_files(preprocessor_path, model_path)
        self.preprocessor = self.load_preprocessor(preprocessor_path)
        self.model = self.load_model(model_path)

    def validate_model_files(self, preprocessor_path, model_path):
        missing_files = []

        if not os.path.exists(preprocessor_path):
            missing_files.append("preprocessor.pkl")

        if not os.path.exists(model_path):
            missing_files.append("model.pkl")

        if missing_files:
            raise FileNotFoundError(
                f"Missing model artifacts: {', '.join(missing_files)}"
            )

    def load_preprocessor(self, preprocessor_path):

        with open(preprocessor_path, "rb") as file:
            return pickle.load(file)

    def load_model(self, model_path):

        with open(model_path, "rb") as file:
            return pickle.load(file)

    
    def predict(self, features: dict):
        df = pd.DataFrame([features])
        transformed_df =  self.preprocessor.transform(df)

        probabilities = self.model.predict_proba(transformed_df)
        prediction = self.model.predict(transformed_df)

        selected_probability = (
            probabilities[0][1] * 100
        )

        return {
            "prediction": int(prediction[0]),
            "probability": round(selected_probability,2)
        }