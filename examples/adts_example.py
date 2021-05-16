import json
from dataclasses import dataclass
from pprint import pprint


@dataclass
class Answers:
    default: int
    choices: dict = None
    min: int = None
    max: int = None


@dataclass
class Question:
    category: str
    question: str
    answers: Answers


@dataclass
class Symptom:
    symptom_name: str
    question: Question


@dataclass
class Disease:
    disease_name: str
    possible_symptoms: list


class Patient:
    def __init__(self):
        self.basic_data = []
        self.symptoms_data = []


if __name__ == '__main__':
    with open("SymptomsOutput.json") as file:
        symptoms_data = json.load(file)
    patient = Patient()
    for symptom_data in symptoms_data:

        if "choices" in symptom_data:
            choices = {choice["laytext"]: choice["value"] for choice in symptom_data["choices"]}
            answers = Answers(symptom_data["default"], choices)
        else:
            answers = Answers(symptom_data["default"], {}, symptom_data["min"], symptom_data["max"])
        question = Question(symptom_data["category"], symptom_data["laytext"], answers)
        symptom = Symptom(symptom_data["name"], question)

        if symptom_data["category"] == "Constitutional and vital signs physical examination":
            patient.basic_data.append(symptom)
        else:
            patient.symptoms_data.append(symptom)
    pprint(patient.symptoms_data)
