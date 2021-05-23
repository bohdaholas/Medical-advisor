"""Module for ADT realization"""

import json
from dataclasses import dataclass
from datastructures import LinkedStack


@dataclass
class Answers:
    """This class contains possible user answers to the Question.question_sentence"""
    default_value: int
    choices: dict = None
    min_value: int = None
    max_value: int = None


@dataclass
class Question:
    """Category of question, question and answers to it"""
    category: str
    question_sentence: str
    answers: Answers


@dataclass
class Symptom:
    """Symptom and the question that confirms or refutes this symptom"""
    symptom_name: str
    question: Question


@dataclass
class Patient:
    """Contains patient symptoms and whether he was analyzed before"""
    was_analyzed: bool = False
    patient_symptoms = LinkedStack()


class SymptomBD:
    """
    basic_data - questions to find out basic human health level (BMI, age, heart rate ...)
    symptoms_data - stack[Symptom]
    """
    def __init__(self):
        self.basic_data = LinkedStack()
        self.symptoms_data = LinkedStack()
        self.fill_in_data()

    def fill_in_data(self, file_path="SymptomsOutput.json"):
        """Read json file and fill in basic_data and symptoms_data fields"""
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
