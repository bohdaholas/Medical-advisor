import json
from dataclasses import dataclass
from pprint import pprint
from datastructures import LinkedStack

@dataclass
class Answers:
    default_value: int
    choices: dict = None
    min_value: int = None
    max_value: int = None


@dataclass
class Question:
    category: str
    question_sentence: str
    answers: Answers


@dataclass
class Symptom:
    symptom_name: str
    question: Question


@dataclass
class Patient:
    was_analyzed: bool = False
    patient_symptoms = LinkedStack()


class SymptomBD:
    def __init__(self):
        self.basic_data = LinkedStack()
        self.symptoms_data = LinkedStack()
        self.fill_in_data()

    def fill_in_data(self, file_path="examples/SymptomsOutput.json"):
        with open(file_path) as file:
            symptoms_data = json.load(file)
        for symptom_data in symptoms_data:

            if "choices" in symptom_data:
                choices = {choice["laytext"]: choice["value"] for choice in symptom_data["choices"]}
                answers = Answers(default_value=symptom_data["default"], choices=choices)
            else:
                answers = Answers(default_value=symptom_data["default"], choices={},
                                  min_value=symptom_data["min"], max_value=symptom_data["max"])
            question = Question(category=symptom_data["category"], question_sentence=symptom_data["laytext"], answers=answers)
            symptom = Symptom(symptom_name=symptom_data["name"], question=question)

            if symptom_data["category"] == "Constitutional and vital signs physical examination":
                self.basic_data.push(symptom)
            else:
                self.symptoms_data.push(symptom)
