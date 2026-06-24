import os
import json

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

TEMP_DIR = os.path.join(
    PROJECT_ROOT,
    "new_data",
    "temp"
)

os.makedirs(TEMP_DIR, exist_ok=True)


def save_profile(profile_result):

    filepath = os.path.join(
        TEMP_DIR,
        "profile.json"
    )

    with open(filepath, "w") as file:
        json.dump(
            profile_result,
            file,
            indent=4
        )


def load_profile():

    filepath = os.path.join(
        TEMP_DIR,
        "profile.json"
    )

    if not os.path.exists(filepath):
        return None

    with open(filepath, "r") as file:
        return json.load(file)


def save_evaluation(evaluation_report):

    filepath = os.path.join(
        TEMP_DIR,
        "evaluation_report.json"
    )

    with open(filepath, "w") as file:
        json.dump(
            evaluation_report,
            file,
            indent=4
        )


def load_evaluation():

    filepath = os.path.join(
        TEMP_DIR,
        "evaluation_report.json"
    )

    if not os.path.exists(filepath):
        return None

    with open(filepath, "r") as file:
        return json.load(file)