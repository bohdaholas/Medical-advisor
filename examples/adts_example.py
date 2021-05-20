import json
from dataclasses import dataclass
from pprint import pprint


@dataclass
class Answers:
    default_value: int
    choices: dict = None
    min_value: int = None
    max_value: int = None


@dataclass
class Question:
    category: str
    question: str
    answers: Answers


@dataclass
class Symptom:
    symptom_name: str
    question: Question


class SymptomBD:
    def __init__(self):
        self.basic_data = []
        self.symptoms_data = []


if __name__ == '__main__':
    with open("SymptomsOutput.json") as file:
        symptoms_data = json.load(file)
    symptom_bd = SymptomBD()
    for symptom_data in symptoms_data:

        if "choices" in symptom_data:
            choices = {choice["laytext"]: choice["value"] for choice in symptom_data["choices"]}
            answers = Answers(default_value=symptom_data["default"], choices=choices)
        else:
            answers = Answers(default_value=symptom_data["default"], choices={},
                              min_value=symptom_data["min"], max_value=symptom_data["max"])
        question = Question(category=symptom_data["category"], question=symptom_data["laytext"], answers=answers)
        symptom = Symptom(symptom_name=symptom_data["name"], question=question)

        if symptom_data["category"] == "Constitutional and vital signs physical examination":
            symptom_bd.basic_data.append(symptom)
        else:
            symptom_bd.symptoms_data.append(symptom)
    pprint(symptom_bd.basic_data)
    print("*" * 50)
    pprint(symptom_bd.symptoms_data)
